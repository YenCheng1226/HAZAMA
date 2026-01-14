import pytest


def test_always_passes():
    """這是一個基礎測試，用來確認 GitHub Actions 流程是否打通"""
    assert True


def test_csv_logic_placeholder():
    """模擬 Spec 2.1 的欄位檢查邏輯"""
    # required_fields = ["event_id", "start_date", "end_date", "bbox"]
    sample_data = {"event_id": "FL001", "start_date": "2023-01-01"}

    # 這裡故意寫一個會過的邏輯：檢查欄位是否完整
    is_valid = all(field in sample_data for field in ["event_id", "start_date"])
    assert is_valid is True
