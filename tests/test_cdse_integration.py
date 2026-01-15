from dotenv import load_dotenv

from src.search.fetch_CDSE import process_event_for_cdse

# 確保測試前有讀取金鑰
load_dotenv()


def test_real_cdse_connection():
    test_bbox = [121.5, 25.0, 121.6, 25.1]
    test_date = "2024-01-01/2024-01-10"
    event_id = "TEST_001"

    result = process_event_for_cdse(event_id, test_bbox, test_date)

    # 這裡會強制印出結果，不管成功還是失敗
    print("\n" + "=" * 50)
    print(f"測試事件 ID: {result['event_id']}")
    print(f"最終狀態: {result['status']}")
    print(f"找到的路徑: {result['path']}")
    print(f"雲量資訊: {result['cloud_coverage']}")
    print("=" * 50)

    # 1. 確保沒有 API 錯誤 (金鑰檢查)
    assert result["status"] != "API_ERROR", (
        f"金鑰或連線有問題！錯誤訊息: {result.get('metadata')}"
    )

    # 2. 如果狀態是 SUCCESS，那 path 就絕對不能是 None
    if result["status"] == "SUCCESS":
        assert result["path"] is not None, "狀態是 SUCCESS 但 path 卻是空的，這不合理！"

    # 3. 確保 event_id 沒有被弄丟
    assert result["event_id"] == event_id
