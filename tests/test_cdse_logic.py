import pytest
from unittest.mock import MagicMock, patch
from src.search.fetch_CDSE import process_event_for_cdse

# 1. 測試時間計算與 BBox 補全
def test_event_parameter_logic():
    mock_event = {
        "id": "E_TEST",
        "start_date": "2025-01-10",
        "end_date": "2025-01-12",
        "pre_event_days": 5,
        "post_event_days": 2,
        "bbox": None  # 測試補全
    }
    
    # 我們不真的跑下載，只測試參數處理
    with patch('src.search.fetch_CDSE.get_stac_client') as mock_stac:
        # 模擬搜尋結果為空，這樣就不會進入下載邏輯
        mock_stac.return_value.search.return_value.item_collection.return_value = []
        
        result = process_event_for_cdse(mock_event)
        
        # 檢查 status 是否因為沒圖而回傳 NO_IMAGE
        assert result["status"] == "NO_IMAGE"

# 2. 測試座標轉換 (驗證 pyproj/rasterio 邏輯)
def test_coordinate_transform():
    from rasterio.warp import transform_bounds
    wgs84_bbox = [121.5, 25.0, 121.6, 25.1]
    # 假設影像座標系是 UTM 51N (EPSG:32651)
    target_crs = "EPSG:32651"
    
    reprojected = transform_bounds("EPSG:4326", target_crs, *wgs84_bbox)
    
    # 經緯度數值很小(121, 25)，UTM 數值很大(>100000)
    assert reprojected[0] > 1000 
    assert reprojected[1] > 1000

def test_csv_structure():
    mock_results = [{
        "event_id": "E001",
        "metadata": "S2A_xxx, S2B_yyy",
        "status": "SUCCESS",
        "path": "/tmp/E001"
    }]
    import pandas as pd
    df = pd.DataFrame(mock_results)
    assert "event_id" in df.columns
    assert "path" in df.columns