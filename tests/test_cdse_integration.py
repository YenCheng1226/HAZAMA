import pytest
import os
from dotenv import load_dotenv
from src.search.fetch_CDSE import process_event_for_cdse

# 確保測試前有讀取金鑰
load_dotenv()

def test_real_cdse_connection():
    # 使用一個已知有資料的區域（例如台北）
    test_bbox = [121.5, 25.0, 121.6, 25.1]
    test_date = "2024-01-01/2024-01-10"
    event_id = "TEST_001"
    
    # 執行實際的 Function
    result = process_event_for_cdse(event_id, test_bbox, test_date)
    
    # 狀態應該是 SUCCESS 或 NO_IMAGE (取決於當時雲量或資料)
    # 但絕對不應該是 API_ERROR (除非沒設定好金鑰)
    assert result["status"] in ["SUCCESS", "NO_IMAGE"]
    assert result["event_id"] == event_id
    
    if result["status"] == "SUCCESS":
        assert result["path"] is not None
        assert "http" in result["path"]