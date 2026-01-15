#import pytest
# from src.ingestion import parse_event_csv

# def test_parse_valid_csv(tmp_path):
# create a test CSV file
# d = data/test/"test.csv"
# d.write_text("event_id,start_date,end_date,bbox\nE001,2023-01-01,2023-01-05,
# '[120, 23, 121, 24]'")

# events = parse_event_csv(str(d))
# assert len(events) == 1
# assert events[0]['event_id'] == "E001"

import os
from dotenv import load_dotenv
from pystac_client import Client

# 1. 讀取環境變數
load_dotenv()

def get_stac_client():
    '''開啟 CDSE STAC '''
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
    
    # 建立搜尋過濾條件
    search = catalog.search(
        collections = [collection],
        bbox = bbox,
        datetime = date_range,
        #query={"eo:cloud_cover": {"lt": max_cloud}} if "sentinel-2" in collection else None
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
        "status": "PENDING"
    }
    
    try:
        # 執行 STAC 搜尋
        items = search_satellite_data(bbox, date_range)
        
        if not items:
            results_entry["status"] = "NO_IMAGE"
            return results_entry
            
        # 取第一筆最適合的影像
        best_item = items[0]
        
        # 填充資料
        results_entry["metadata"] = str(best_item.properties) # 轉成字串存入 CSV
        results_entry["cloud_coverage"] = best_item.properties.get("eo:cloud_cover")
        results_entry["status"] = "SUCCESS"
        
        # 這裡的 path 可以是 S3 連結，或你處理後的本地路徑 這裡待處理
        results_entry["path"] = best_item.assets["rendered_preview"]["href"]
        
    except Exception as e:
        results_entry["status"] = "API_ERROR"
        print(f"Error processing {event_id}: {e}")
        
    return results_entry

all_results = [] # 將CDSE的尋找結果存在list中

for event in event_list:
    # event_list 是ingestion.py讀取的事件清單
    event_id = event['id']
    start_date = event['start_date']
    end_date = event['end_date']
    pre_days = event['pre_event_days']
    post_days = event['post_event_days']
    event_date = start_date + "/" + end_date

    # 2. 呼叫 CDSE Function 取得新資料
    cdse_data = process_event_for_cdse(event_id, event['bbox'], event_date)
    
    # 3. 合併 (Merge)
    full_entry = {
        **cdse_data, # event_id, metadata, cloud_coverage, status, path
        "pre-event days": pre_days,
        "post-event days": post_days
    }
    
    all_results.append(full_entry)


# import pandas as pd
# pd.DataFrame(all_results).to_csv("results.csv", index=False)