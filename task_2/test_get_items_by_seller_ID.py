import pytest


# Покрытые тест-кейсы: TC-006, TC-007, TC-017, TC-018, TC-019

class TestGetItemsBySellerPositive:
    @pytest.mark.tc_id("TC-006")
    @pytest.mark.positive
    def test_TC_006_get_three_items_for_seller(self, client, valid_create_payload):
        """TC-006: Получение списка из 3 объявлений продавца"""
        created_ids = []
        for i in range(3):
            payload = valid_create_payload(name=f"Seller-Test-{i}")
            resp = client.create_item(data=payload)
            assert resp.status_code == 200
            item_id = resp.json()["status"].split(' - ')[-1].strip()
            created_ids.append(item_id)

        try:
            resp = client.get_items_by_seller(client.seller_id)
            assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"

            items = resp.json()
            assert isinstance(items, list), "Ответ должен быть массивом"

            returned_ids = [item['id'] for item in items]
            for item_id in created_ids:
                assert item_id in returned_ids, f"Созданное объявление {item_id} не найдено в списке"

        finally:
            for item_id in created_ids:
                client.delete_item_by_id(item_id)

    @pytest.mark.tc_id("TC-007")
    @pytest.mark.positive
    def test_TC_007_empty_list_for_seller_without_items(self, client):
        """TC-007: Получение пустого списка для продавца без объявлений"""
        # Используем заведомо "чистый" sellerID вне нашего диапазона тестов
        empty_seller_id = 98672

        resp = client.get_items_by_seller(empty_seller_id)

        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        assert resp.json() == [], "Для продавца без объявлений должен вернуться пустой массив"


class TestGetItemsBySellerNegative:
    @pytest.mark.tc_id("TC-017")
    @pytest.mark.negative
    def test_TC_017_nonexistent_seller_id(self, client):
        """TC-017: Несуществующий sellerID — возвращается пустой список (не ошибка)"""
        resp = client.get_items_by_seller(98672)

        assert resp.status_code == 200, f"Ожидался 200 (пустой список), получен {resp.status_code}"
        assert resp.json() == [], "Для несуществующего продавца должен вернуться пустой массив"

    @pytest.mark.tc_id("TC-018")
    @pytest.mark.negative
    def test_TC_018_invalid_seller_id_type_string(self, client):
        """TC-018: Неверный тип sellerID (строка вместо числа)"""
        url = f"{client.base_url}/api/1/abc/item"
        resp = client.session.get(url)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
        error = resp.json()
        result_msg = error.get('result', {}).get('message', '') if isinstance(error, dict) else ""
        assert "некорректный идентификатор продавца" in result_msg.lower(), \
            f"Сообщение должно указывать на некорректный ID: {result_msg}"

    @pytest.mark.tc_id("TC-019")
    @pytest.mark.negative
    def test_TC_019_negative_seller_id(self, client):
        """TC-019: Отрицательный sellerID"""
        url = f"{client.base_url}/api/1/-5/item"
        resp = client.session.get(url)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
