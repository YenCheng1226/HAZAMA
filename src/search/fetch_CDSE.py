import os
import logging
import boto3
import rasterio
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pystac_client import Client
from rasterio.session import AWSSession
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds

# --- 設定 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CDSE_Fetcher")

load_dotenv()

DEFAULT_BBOX = [121.56, 25.03, 121.57, 25.04] # 確定成功的台北 101 座標

def get_stac_client():
    return Client.open("https://catalogue.dataspace.copernicus.eu/stac")

def save_as_cog(item, bbox_wgs84, event_id, output_dir, band):
    access_key = os.getenv("CDSE_S3_ACCESS_KEY")
    secret_key = os.getenv("CDSE_S3_SECRET_KEY")
    asset = item.assets.get(band)
    if not asset:
        available_assets = list(item.assets.keys())
        logger.warning(f"影像 {item.id} 找不到波段 {band}")
        logger.info(f"該影像可用的波段有: {available_assets}")
        return None
    
    s3_url = asset.href.replace("https://eodata.dataspace.copernicus.eu/", "/vsis3/eodata/")
    date_str = item.datetime.strftime("%Y%m%d")
    unique_filename = f"{event_id}_{item.id}_{date_str}_{band}.tif"
    local_path = os.path.join(output_dir, unique_filename)

    try:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        with rasterio.Env(AWSSession(session),
            AWS_S3_ENDPOINT="eodata.dataspace.copernicus.eu",
            GDAL_S3_ENDPOINT_DIRECT="eodata.dataspace.copernicus.eu",
            AWS_VIRTUAL_HOSTING="FALSE",      
            AWS_HTTPS="YES",
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR" 
        ):
            with rasterio.open(s3_url) as src:
                # 執行座標轉換
                left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
                window = from_bounds(left, bottom, right, top, transform=src.transform)
                
                # 讀取數據
                data = src.read(window=window)
                
                # 設定設定檔
                profile = src.profile.copy()
                profile.update({
                    'driver': 'GTiff',
                    'height': window.height,
                    'width': window.width,
                    'transform': rasterio.windows.transform(window, src.transform),
                    'tiled': True,
                    'compress': 'deflate'
                })
                
                with rasterio.open(local_path, 'w', **profile) as dst:
                    dst.write(data)
                    
        return os.path.abspath(local_path)
    except Exception as e:
        logger.error(f"下載失敗 {band}: {e}")
        return None

def process_event_for_cdse(event_id, bbox, date_range, collection="sentinel-2-l2a", bands=["B04_10m"]):
    base_output_dir = "data/output_images"
    event_folder = os.path.join(base_output_dir, event_id)
    if not os.path.exists(event_folder): os.makedirs(event_folder)

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
        
        # --- 關鍵修正：使用 list(search.items()) 確保抓到資料 ---
        items = list(search.items())

        if not items:
            logger.warning(f"[NO_DATA_FOUND] {event_id} 在 {date_range} 沒圖")
            results["status"] = "NO_IMAGE"
            return results
        
        success_count = 0
        for item in items:
            download_success = False
            for band in bands:
                path = save_as_cog(item, actual_bbox, event_id, event_folder, band)
                if path: download_success = True
            
            if download_success:
                success_count += 1
                results["metadata"].append(item.id)
                cc = item.properties.get("eo:cloud_cover")
                if cc is not None: results["cloud_coverage"].append(cc)

        if success_count > 0:
            results["status"] = "SUCCESS"
            results["metadata"] = ", ".join(results["metadata"])
            results["cloud_coverage"] = round(sum(results["cloud_coverage"])/len(results["cloud_coverage"]), 2) if results["cloud_coverage"] else 0
        else:
            results["status"] = "NO_IMAGE"

    except Exception as e:
        logger.error(f"處理事件 {event_id} 報錯: {e}")
        results["status"] = "API_ERROR"
        
    return results

def cdse(event_list, collection="sentinel-2-l2a", bands=["B04_10m"], base_dir="data/output_images"):
    all_results = []
    for event in event_list:
        # 時間計算邏輯
        start_dt = datetime.strptime(event["start_date"], "%Y-%m-%d")
        end_dt = datetime.strptime(event["end_date"], "%Y-%m-%d")
        full_start = start_dt - timedelta(days=int(event["pre_event_days"]))
        full_end = end_dt + timedelta(days=int(event["post_event_days"]))
        date_range = f"{full_start.strftime('%Y-%m-%d')}/{full_end.strftime('%Y-%m-%d')}"

        res = process_event_for_cdse(event["id"], event.get("bbox"), date_range)
        
        # 合併輸出
        all_results.append({
            **res,
            "pre-event days": event["pre_event_days"],
            "post-event days": event["post_event_days"]
        })
    
    pd.DataFrame(all_results).to_csv("data/results.csv", index=False)
    logger.info("CSV 已更新！")