import logging
import os

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


def search_satellite_data(bbox, date_range, collection="sentinel-2-l2a"):
    """
    搜尋衛星影像
    :param bbox: [西, 南, 東, 北] 經緯度列表
    :param date_range: "YYYY-MM-DD/YYYY-MM-DD"
    :param collection: 衛星種類，例如 'sentinel-2-l2a' 或 'sentinel-1-grd'
    :param max_cloud: 最大雲覆蓋率 (0-100) 還沒加上
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


def process_event_for_cdse(event_id, bbox, date_range):
    results_entry = {
        "event_id": event_id,
        "metadata": None,
        "cloud_coverage": None,
        "path": None,
        "status": "PENDING",
    }

    try:
        # 執行 STAC 搜尋
        items = search_satellite_data(bbox, date_range)

        if not items:
            logger.warning(
                f"[NO_DATA_FOUND] Event {event_id} in bbox {bbox} has no imagery."
            )
            results_entry["status"] = "NO_IMAGE"
            return results_entry

        # 取第一筆最適合的影像
        best_item = items[0]

        # 填充資料
        results_entry["metadata"] = str(best_item.properties)
        results_entry["cloud_coverage"] = best_item.properties.get("eo:cloud_cover")
        # 處理 Path
        # 取得 S3 上的原始影像連結 ex.B04
        # 可能要選特定波段，這裡可以拿到暫存的 S3 連結
        # 嘗試多種可能的 Asset Key
        asset_keys = ["rendered_preview", "thumbnail", "visual", "B04"]
        for key in asset_keys:
            asset = best_item.assets.get(key)
            if asset and asset.href:
                results_entry["path"] = asset.href
                break

        # 如果還是 None，印出所有可用的 Key 供除錯
        if results_entry["path"] is None:
            print(f"警告：找不到預期資產。可用資產為: {list(best_item.assets.keys())}")

        # 2. [待處理] 呼叫裁切並存成 COG 的 function
        # local_cog_path = save_as_local_cog(s3_url, event_id, bbox)
        # results_entry["path"] = local_cog_path

        # 暫時先放 S3 連結
        results_entry["status"] = "SUCCESS"
    except Exception as e:
        results_entry["status"] = "API_ERROR"
        logger.error(f"處理事件 {event_id} 時發生意外: {e}")

    return results_entry


def cdse(event_list):
    all_results = []  # 將CDSE的尋找結果存在list中

    for event in event_list:
        # event_list 是ingestion.py讀取的事件清單
        event_id = event["id"]
        start_date = event["start_date"]
        end_date = event["end_date"]
        pre_days = event["pre_event_days"]
        post_days = event["post_event_days"]
        event_date = start_date + "/" + end_date

        # 執行 CDSE 資料搜尋
        cdse_data = process_event_for_cdse(event_id, event["bbox"], event_date)

        # 最終Output
        full_entry = {
            **cdse_data,  # event_id, metadata, cloud_coverage, status, path
            "pre-event days": pre_days,
            "post-event days": post_days,
        }

        all_results.append(full_entry)
    df = pd.DataFrame(all_results)
    df.to_csv("data/results.csv", index=False)
    print("CSV 儲存完畢！")
