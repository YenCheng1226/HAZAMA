# run_real_test.py
import os
import logging
from src.search.fetch_CDSE import cdse

# 設定測試事件 (針對確定有圖的 2024-12-05)
test_events = [
    {
        "id": "FINAL_SUCCESS_CHECK",
        "start_date": "2024-12-05",
        "end_date": "2024-12-06", 
        "pre_event_days": 4, # 確保涵蓋到 12/01
        "post_event_days": 0,
        "bbox": [121.56, 25.03, 121.57, 25.04] # 台北 101
    }
]

# 任務設定
config = {
    "collection": "sentinel-2-l2a",
    "bands": ["TCI_10m"], # Sentinel-2 的紅光波段
    "base_dir": "data/final_test"
}

if __name__ == "__main__":
    print("🚀 啟動最終下載測試...")
    # 確保參數名稱符合 cdse(event_list, collection, bands, base_dir) 的定義
    cdse(test_events, **config)