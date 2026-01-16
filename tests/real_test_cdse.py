import os
from src.search.fetch_CDSE import cdse

# 1. 準備測試事件 (選取一個 2025 年初的日期，確保資料已上雲)
test_events = [
    {
        "id": "TAIPEI_101_TEST",
        "start_date": "2025-01-01",
        "end_date": "2025-01-02",
        "pre_event_days": 1,
        "post_event_days": 1,
        "bbox": [121.51, 25.03, 121.52, 25.04] # 台北 101 周邊小範圍
    }
]

# 2. 設定任務參數
# 建議先測試 Sentinel-2 的 B04 (紅光波段)
config = {
    "collection": "sentinel-2-l2a",
    "bands": ["B04"], 
    "base_dir": "data/real_test_output"
}

if __name__ == "__main__":
    print("🚀 開始執行真實資料下載測試...")
    try:
        cdse(test_events, **config)
        print("\n✅ 測試完成！請檢查 data/real_test_output 資料夾。")
    except Exception as e:
        print(f"\n❌ 執行失敗: {e}")