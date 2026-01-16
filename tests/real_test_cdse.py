# run_real_test.py
from src.search.fetch_CDSE import cdse

# 設定測試事件 (針對確定有圖的 2024-12-05)
# run_real_test.py

test_events = [
    {
        "id": "S2_TEST",
        "start_date": "2024-12-05",
        "end_date": "2024-12-10",
        "pre_event_days": 5,
        "post_event_days": 5,
        "bbox": [121.56, 25.03, 121.57, 25.04],
    }
]

config = {
    "collection": "sentinel-2-l2a",  # 換成雷達 Collection
    "bands": ["B04_10m", "TCI_10m"],  # 雷達常見的雙極化波段
    "base_dir": "data/radar_test",
}

if __name__ == "__main__":
    print("🚀 啟動最終下載測試...")
    # 確保參數名稱符合 cdse(event_list, collection, bands, base_dir) 的定義
    cdse(test_events, **config)
