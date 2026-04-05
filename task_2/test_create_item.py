import pytest
from api_models import ErrorResponse


class TestCreateItemPositive:

    @pytest.mark.tc_id("TC-001")
    @pytest.mark.positive
    def test_TC_001_create_with_valid_data(self, client, valid_create_payload):
        payload = valid_create_payload(name="name", price=1)

        resp = client.create_item(data=payload)

        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "status" in data, "В ответе должно быть поле 'status'"
        assert "Сохранили объявление" in data["status"], "Статус должен содержать сообщение об успехе"
        assert "-" in data["status"], "В статусе должен быть UUID объявления"

    @pytest.mark.tc_id("TC-003")
    @pytest.mark.positive
    @pytest.mark.parametrize("price,name_len,desc", [
        (1, 1, "минимальные значения"),
        (2147483647, 255, "максимальные значения"),
    ], ids=["min", "max"])
    def test_TC_003_boundary_values(self, client, valid_create_payload, price, name_len, desc):
        payload = valid_create_payload(
            name="x" * name_len,
            price=price
        )

        resp = client.create_item(data=payload)

        assert resp.status_code == 200, f"Ожидался 200 ({desc}), получен {resp.status_code}: {resp.text}"
        assert "Сохранили объявление" in resp.json()["status"]

    @pytest.mark.tc_id("TC-004")
    @pytest.mark.positive
    def test_TC_004_multiple_creation_same_seller(self, client, valid_create_payload):
        created_ids = []
        expected_seller_id = client.seller_id

        for i in range(3):
            payload = valid_create_payload(name=f"Multi-Test-{i}")
            resp = client.create_item(data=payload)
            assert resp.status_code == 200, f"Не удалось создать объявление #{i + 1}"

            # Извлекаем ID из ответа
            status_msg = resp.json()["status"]
            item_id = status_msg.split(' - ')[-1].strip()
            created_ids.append(item_id)

        for item_id in created_ids:
            get_resp = client.get_item_by_id(item_id)
            assert get_resp.status_code == 200, f"Не удалось получить объявление {item_id}"

            json_data = get_resp.json()
            item_data = json_data[0] if isinstance(json_data, list) else json_data

            # Проверяем, что объявление принадлежит нужному продавцу
            assert item_data["sellerId"] == expected_seller_id, \
                f"Объявление {item_id} принадлежит sellerId={item_data['sellerId']}, а ожидалось {expected_seller_id}"

        # Проверяем уникальность всех ID
        assert len(set(created_ids)) == 3, "Все созданные объявления должны иметь уникальные ID"

        for item_id in created_ids:
            client.delete_item_by_id(item_id)


class TestCreateItemNegative:

    @pytest.mark.tc_id("TC-010")
    @pytest.mark.negative
    def test_TC_010_empty_body(self, client):
        resp = client.create_item(data={})

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status == "400", f"Статус ошибки должен быть '400', получен: {error.status}"
        assert error.message and "name обязательно" in error.message, \
            f"Сообщение должно содержать 'name обязательно', получено: {error.message}"

    @pytest.mark.tc_id("TC-011")
    @pytest.mark.negative
    def test_TC_011_missing_seller_id(self, client, valid_create_payload):
        """TC-011: Отсутствие sellerID в теле запроса"""
        payload = valid_create_payload()
        del payload['sellerID']  # Убираем обязательное поле

        resp = client.create_item(data=payload)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status in ("400", "не передано тело объявления"), \
            f"Неверный статус ошибки: {error.status}"

    @pytest.mark.tc_id("TC-012")
    @pytest.mark.negative
    def test_TC_012_price_as_string(self, client, valid_create_payload):
        """TC-012: Некорректный тип: price как строка вместо числа"""
        payload = valid_create_payload()
        payload['price'] = "1000"

        resp = client.create_item(data=payload)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
        error = ErrorResponse(**resp.json())
        assert error.status in ("400", "не передано тело объявления")

    @pytest.mark.tc_id("TC-013")
    @pytest.mark.negative
    def test_TC_013_negative_price(self, client):
        """TC-013: Отрицательная цена — сервер должен отклонить"""

        # Создаём payload вручную, минуя Pydantic-валидацию
        payload = {
            "sellerID": 9876543,
            "name": f"Test Item ",
            "price": -100,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }

        resp = client.create_item(data=payload)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"

    @pytest.mark.tc_id("TC-014")
    @pytest.mark.negative
    def test_TC_014_negative_statistics(self, client):
        """TC-014: Отрицательная цена — сервер должен отклонить"""
        # Создаём payload вручную, минуя Pydantic-валидацию
        payload = {
            "sellerID": 9876543,
            "name": f"Test Item ",
            "price": 100,
            "statistics": {"likes": -1, "viewCount": -1, "contacts": -1}
        }

        resp = client.create_item(data=payload)

        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"