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

def save_as_cog(item, bbox_wgs84, event_id, output_dir, band):
    """將 STAC Item 的指定波段存為 COG 格式"""
    asset = item.assets.get(band)
    if not asset:
        return None
    
    s3_url = asset.href
    date_str = item.datetime.strftime("%Y%m%d")
    unique_filename = f"{event_id}_{item.id}_{date_str}_{band}.tif"
    local_path = os.path.join(output_dir, unique_filename)

    try:
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        
        with rasterio.Env(AWSSession(session)):
            with rasterio.open(s3_url) as src:
                # 座標轉換
                left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
                window = from_bounds(left, bottom, right, top, transform=src.transform)
                
                data = src.read(window=window)
                
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
                
                with rasterio.open(local_path, 'w', **profile) as dst:
                    dst.write(data)
                    
        return os.path.abspath(local_path)
    except Exception as e:
        logger.error(f"COG 轉換失敗 ({band}): {e}")
        return None

def process_event_for_cdse(event_id, bbox, date_range, collection, bands, base_output_dir):
   
    event_folder = os.path.join(base_output_dir, event_id)
    if not os.path.exists(event_folder):
        os.makedirs(event_folder)

    actual_bbox = bbox if bbox else DEFAULT_BBOX

    results = {
        "event_id": event_id,
        "metadata": [],
        "cloud_coverage": [],
        "path": os.path.abspath(event_folder),
        "status": "PENDING"
    }

    try:
        catalog = get_stac_client()
        search = catalog.search(collections=[collection], bbox=actual_bbox, datetime=date_range)
        items = search.item_collection()

        if not items:
            logger.warning(f"[NO_DATA_FOUND] Event {event_id} has no imagery.")
            results["status"] = "NO_IMAGE"
            return results
        
        success_count = 0
        for item in items:
            # 支援多波段儲存 (Sen-1: VV, VH; Sen-2: B04...)
            band_success = False
            for band in bands:
                local_path = save_as_cog(item, actual_bbox, event_id, event_folder, band)
                if local_path:
                    band_success = True
            
            if band_success:
                success_count += 1
                results["metadata"].append(item.id)
                # Sen-1 沒有雲量，需安全讀取
                cloud = item.properties.get("eo:cloud_cover")
                if cloud is not None:
                    results["cloud_coverage"].append(cloud)

        if success_count > 0:
            results["status"] = "SUCCESS"
            results["metadata"] = ", ".join(results["metadata"])
        else:
            results["status"] = "NO_IMAGE"

    except Exception as e:
        logger.error(f"處理事件 {event_id} 失敗: {e}")
        results["status"] = "API_ERROR"
        
    return results

def cdse(event_list, collection="sentinel-2-l2a", bands=["B04"], base_dir="data/output_images"):
    
    all_results = []

    for event in event_list:
        event_id = event["id"]
        # 時間窗口計算
        start_dt = datetime.strptime(event["start_date"], "%Y-%m-%d")
        end_dt = datetime.strptime(event["end_date"], "%Y-%m-%d")
        full_start = start_dt - timedelta(days=int(event["pre_event_days"]))
        full_end = end_dt + timedelta(days=int(event["post_event_days"]))
        
        event_date_range = f"{full_start.strftime('%Y-%m-%d')}/{full_end.strftime('%Y-%m-%d')}"

        # 執行 CDSE 任務
        cdse_data = process_event_for_cdse(
            event_id, 
            event.get("bbox"), 
            event_date_range, 
            collection, 
            bands, 
            base_dir
        )

        # 整理輸出格式
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

    # 產出 CSV
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(all_results)
    df.to_csv("data/results.csv", index=False)
    logger.info("CSV 已儲存至 data/results.csv")
