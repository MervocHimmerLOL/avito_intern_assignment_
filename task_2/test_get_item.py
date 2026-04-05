import pytest
import uuid
from utilities.api_models import ItemResponse, ErrorResponse


# Покрытые тест-кейсы: TC-005, TC-015, TC-016, ТС-27

class TestGetItemByIdPositive:
    @pytest.mark.tc_id("TC-005")
    @pytest.mark.positive
    def test_TC_005_get_existing_item(self, created_item_id, client):
        """TC-005: Успешное получение существующего объявления"""
        resp = client.get_item_by_id(created_item_id)

        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}: {resp.text}"

        json_data = resp.json()
        item_data = json_data[0] if isinstance(json_data, list) else json_data

        item = ItemResponse(**item_data)

        assert item.id == created_item_id, f"ID не совпадает: ожидался {created_item_id}, получен {item.id}"
        assert item.price >= 1, "Цена должна быть неотрицательной"
        assert len(item.name) > 0, "Имя не должно быть пустым"
        assert item.statistics.likes >= 1, "Количество лайков должно быть >= 1"
        assert item.sellerId >= 111111, f"sellerId должен быть в диапазоне, получен: {item.sellerId}"


class TestGetItemByIdNegative:
    @pytest.mark.tc_id("TC-015")
    @pytest.mark.negative
    def test_TC_015_nonexistent_id(self, client):
        """TC-015: Несуществующий UUID (валидный формат, но не существует)"""
        fake_id = str(uuid.uuid4())  # Валидный UUID-формат

        resp = client.get_item_by_id(fake_id)

        assert resp.status_code == 404, f"Ожидался 404, получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "404", f"Статус должен быть '404', получен: {error.status}"
        assert error.message and "not found" in error.message.lower(), \
            f"Сообщение должно содержать 'not found': {error.message}"

    @pytest.mark.tc_id("TC-016")
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id,desc", [
        ("1", "простое число"),
        ("not-uuid", "случайная строка"),
    ], ids=["number", "random_string"])
    def test_TC_016_invalid_id_format(self, client, invalid_id, desc):
        """TC-016: Неверный формат ID (не UUID)"""
        resp = client.get_item_by_id(invalid_id)

        assert resp.status_code == 400, f"Ожидался 400 ({desc}), получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "400", f"Статус должен быть '400', получен: {error.status}"
        assert error.message and ("UUID" in error.message or "некорректный" in error.message.lower()), \
            f"Сообщение должно указывать на некорректный ID: {error.message}"

class TestGetItemByIdCornerCases:
    @pytest.mark.tc_id("TC-027")
    @pytest.mark.corner_case
    def test_TC_027_get_item_idempotency(self, created_item_id, client):
        """TC-027: Идемпотентность запроса"""
        resp_1 = client.get_item_by_id(created_item_id)
        item_1 = self._unpack(resp_1)

        resp_2 = client.get_item_by_id(created_item_id)
        item_2 = self._unpack(resp_2)

        assert item_1 == item_2, "Запрос неидемпотентный"

    @staticmethod
    def _unpack(resp):
        json_data = resp.json()
        item_data = json_data[0] if isinstance(json_data, list) else json_data
        return ItemResponse(**item_data)
