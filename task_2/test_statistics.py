import pytest
import uuid
from api_models import Statistics, ErrorResponse

class TestStatisticsPositive:
    @pytest.mark.tc_id("TC-008")
    @pytest.mark.positive
    def test_TC_008_get_statistics_success_v1(self, created_item_id, client):
        """TC-008: Успешное получение статистики API v1"""
        resp = client.get_statistics_v1(created_item_id)

        assert resp.status_code == 200, f"Ожидался 200 (v1), получен {resp.status_code}: {resp.text}"

        data = resp.json()
        stat_data = data[0] if isinstance(data, list) else data
        stat = Statistics(**stat_data)

        assert stat.likes >= 1, "likes должен быть >= 1"
        assert stat.viewCount >= 1, "viewCount должен быть >= 1"
        assert stat.contacts >= 1, "contacts должен быть >= 1"

    @pytest.mark.tc_id("TC-009")
    @pytest.mark.positive
    def test_TC_009_get_statistics_success_v2(self, created_item_id, client):
        """TC-009: Успешное получение статистики API v2"""
        resp = client.get_statistics_v2(created_item_id)

        assert resp.status_code == 200, f"Ожидался 200 (v2), получен {resp.status_code}: {resp.text}"

        data = resp.json()
        stat_data = data[0] if isinstance(data, list) else data
        stat = Statistics(**stat_data)

        assert stat.likes >= 1, "likes должен быть >= 1"
        assert stat.viewCount >= 1, "viewCount должен быть >= 1"
        assert stat.contacts >= 1, "contacts должен быть >= 1"

class TestStatisticsNegative:


    @pytest.mark.tc_id("TC-020")
    @pytest.mark.negative
    def test_TC_020_statistics_nonexistent_id_v1(self, client):
        """TC-020: Статистика API v1 для несуществующего ID → 404"""
        fake_id = str(uuid.uuid4())

        resp = client.get_statistics_v1(fake_id)

        assert resp.status_code == 404, f"Ожидался 404 (v1), получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "404", f"Статус должен быть '404', получен: {error.status}"
        assert error.message and "statistic" in error.message.lower() and "not found" in error.message.lower(), \
            f"Сообщение должно содержать 'statistic ... not found': {error.message}"

    @pytest.mark.tc_id("TC-022")
    @pytest.mark.negative
    def test_TC_022_statistics_nonexistent_id_v2(self, client):
        """TC-022: Статистика API v2 для несуществующего ID → 404"""
        fake_id = str(uuid.uuid4())

        resp = client.get_statistics_v2(fake_id)

        assert resp.status_code == 404, f"Ожидался 404 (v2), получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "404", f"Статус должен быть '404', получен: {error.status}"
        assert error.message and "statistic" in error.message.lower() and "not found" in error.message.lower(), \
            f"Сообщение должно содержать 'statistic ... not found': {error.message}"

    @pytest.mark.tc_id("TC-021")
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id,fmt_desc", [
        ("1", "число"),
        ("not-uuid", "случайная строка"),
        (" ", "пустая строка"),
    ], ids=["number", "string", "empty"])
    def test_TC_021_statistics_invalid_id_format_v1(self, client, invalid_id, fmt_desc):
        """TC-021: Статистика API v1 для некорректного ID 400"""
        resp = client.get_statistics_v1(invalid_id)

        assert resp.status_code == 400, f"Ожидался 400 (v1, {fmt_desc}), получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "400", f"Статус должен быть '400', получен: {error.status}"
        assert error.message and "некорректный идентификатор" in error.message.lower(), \
            f"Сообщение должно указывать на некорректный ID: {error.message}"

    @pytest.mark.tc_id("TC-023")
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id,fmt_desc", [
        ("1", "число"),
        ("not-uuid", "случайная строка"),
        (" ", "пустая строка"),
    ], ids=["number", "string", "empty"])
    def test_TC_023_statistics_invalid_id_format_v2(self, client, invalid_id, fmt_desc):
        """TC-023: Статистика API v2 для некорректного ID """
        resp = client.get_statistics_v2(invalid_id)

        assert resp.status_code == 400, f"Ожидался 400 (v2, {fmt_desc}), получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "400", f"Статус должен быть '400', получен: {error.status}"
        assert error.message and "некорректный идентификатор" in error.message.lower(), \
            f"Сообщение должно указывать на некорректный ID: {error.message}"