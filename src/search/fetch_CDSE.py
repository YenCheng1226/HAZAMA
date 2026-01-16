import logging
import os
import boto3
from pyproj import Transformer
from rasterio.warp import transform_bounds
import rasterio
from rasterio.session import AWSSession
from rasterio.windows import from_bounds
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from pystac_client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CDSE_Fetcher")

load_dotenv()
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("CDSE_S3_ACCESS_KEY", "")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("CDSE_S3_SECRET_KEY", "")
os.environ["GDAL_S3_ENDPOINT_DIRECT"] = "eodata.dataspace.copernicus.eu"


def get_stac_client():
    """開啟 CDSE STAC"""
    url = "https://catalogue.dataspace.copernicus.eu/stac"
    return Client.open(url)

DEFAULT_BBOX = [121.501, 25.045, 121.515, 25.055] # [西, 南, 東, 北] 台北101

def get_corrected_window(src, bbox_wgs84):
    # bbox_wgs84 是經緯度格式 需要轉換為影像座標系
    left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
    return from_bounds(left, bottom, right, top, transform=src.transform)

def save_as_cog(item, bbox, event_id, output_dir="data/output_cogs", assets_to_download="B04"):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for asset_key in assets_to_download:
        s3_url = item.assets.get(asset_key, {}).get("href")
        if not s3_url: continue

        date_str = item.datetime.strftime("%Y%m%d")
        filename = f"{event_id}_{date_str}_{asset_key}.tif"
        local_path = os.path.join(output_dir, filename)
    
    try:
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        
        with rasterio.Env(AWSSession(session)):
            with rasterio.open(s3_url) as src:
                # 確認 bbox 格式為 [西, 南, 東, 北]
                window = from_bounds(*bbox, transform=src.transform)
                
                # 讀取指定範圍
                data = src.read(window=window)
                
                # COG 轉換設定
                profile = src.profile.copy()
                profile.update({
                    'driver': 'GTiff',
                    'height': window.height,
                    'width': window.width,
                    'transform': rasterio.windows.transform(window, src.transform),
                    'tiled': True,
                    'blockxsize': 256,
                    'blockysize': 256,
                    'compress': 'deflate'
                })
                
                # 寫入本地 COG
                with rasterio.open(local_path, 'w', **profile) as dst:
                    dst.write(data)
                    
        return os.path.abspath(local_path)
    except Exception as e:
        logger.error(f"COG 轉換失敗: {e}")
        return None

def search_satellite_data(bbox, date_range, collection="sentinel-2-l2a"):
    """
    param bbox: [西, 南, 東, 北] 經緯度列表
    param date_range: "YYYY-MM-DD/YYYY-MM-DD"
    param collection: 衛星種類，例如 'sentinel-2-l2a' 或 'sentinel-1-grd'
    param max_cloud: 最大雲覆蓋率 (0-100) 還沒加上
    """
    catalog = get_stac_client()

    # 建立搜尋條件
    search = catalog.search(
        collections=[collection],
        bbox=bbox,
        datetime=date_range,
        # query={"eo:cloud_cover":
        #  {"lt": max_cloud}} if "sentinel-2" in collection else None
    )

    items = search.item_collection()
    print(f"找到 {len(items)} 筆符合條件的影像")

    return items


def process_event_for_cdse(event_id, bbox, date_range,base_output_dir="data/output_images"):

    event_folder = os.path.join(base_output_dir, event_id)
    if not os.path.exists(event_folder):
        os.makedirs(event_folder)
    bbox = bbox or DEFAULT_BBOX
    event_images_results = {
        "event_id": event_id,
        "metadata": [],
        "cloud_coverage": [],
        "path": os.path.abspath(event_folder),
        "status": "PENDING"
    }
        

    try:
        # 執行 STAC 搜尋
        catalog = get_stac_client()
        search = catalog.search(collections=["sentinel-2-l2a"], bbox=bbox, datetime=date_range)
        items = search.item_collection()

        # 填充資料
        if not items:
            logger.warning(f"[NO_DATA_FOUND] Event {event_id} in bbox {bbox} has no imagery.")
            event_images_results["status"] = "NO_IMAGE"
            return event_images_results
        
        success_count = 0
        for item in items:
            local_path = save_as_cog(item, bbox, event_id, output_dir=event_folder)
            if local_path:
                success_count += 1
                event_images_results["metadata"].append(item.id)
                event_images_results["cloud_coverage"].append(item.properties.get("eo:cloud_cover"))
        if success_count > 0:
            event_images_results["status"] = "SUCCESS"
            event_images_results["metadata"] = ", ".join(event_images_results["metadata"])
        else:
            event_images_results["status"] = "NO_IMAGE"
    except Exception as e:
        logger.error(f"搜尋事件 {event_id} 時發生錯誤: {e}")
        event_images_results["status"] = "API_ERROR"
    return event_images_results
        


def cdse(event_list):
    all_results = []  # 將CDSE的尋找結果存在list中

    for event in event_list:
        # event_list 是ingestion.py讀取的事件清單
        event_id = event["id"]
        start_dt = datetime.strptime(event["start_date"], "%Y-%m-%d")
        end_dt = datetime.strptime(event["end_date"], "%Y-%m-%d")
        full_start = start_dt - timedelta(days=int(event["pre_event_days"]))
        full_end = end_dt + timedelta(days=int(event["post_event_days"]))
        pre_days = event["pre_event_days"]
        post_days = event["post_event_days"]
        event_date = full_start.strftime("%Y-%m-%d") + "/" + full_end.strftime("%Y-%m-%d")

        # 執行 CDSE 資料搜尋
        cdse_data = process_event_for_cdse(event_id, event["bbox"], event_date)

        # 最終Output
        full_entry = {
            "event_id": cdse_data["event_id"],
            "metadata": cdse_data["metadata"],
            "pre-event days": event["pre_event_days"],
            "post-event days": event["post_event_days"],
            "cloud_coverage": round(sum(cdse_data["cloud_coverage"])/len(cdse_data["cloud_coverage"]), 2)
              if cdse_data["cloud_coverage"] else 0,
            "path": cdse_data["path"],
            "status": cdse_data["status"]
        }

        all_results.append(full_entry)
    df = pd.DataFrame(all_results)
    df.to_csv("data/results.csv", index=False)
    print("CSV 儲存完畢！")
