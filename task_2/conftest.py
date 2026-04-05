import pytest
import uuid
import random

from avito_http_client import AvitoHttpClient
from api_models import CreateItemRequest


# Конфиг с base_url и seller_id для http клиента
@pytest.fixture(scope='session')
def api_config():
    seller_id = random.randint(111111, 999999)
    base_url = "https://qa-internship.avito.com"

    return {
        'base_url': base_url,
        'seller_id': seller_id,
    }


@pytest.fixture(scope='session')
def client(api_config):
    return AvitoHttpClient(
        base_url=api_config['base_url'],
        seller_id=api_config['seller_id']
    )


@pytest.fixture(scope='session')
def test_seller_id(api_config):
    return api_config['seller_id']


# Фикустура для тест-кейсов с проверкой sellerID
@pytest.fixture()
def created_item_id(client):
    unique_name = f"Test Item {uuid.uuid4()}"
    create_data = CreateItemRequest(
        sellerID=client.seller_id,
        name=unique_name,
        price=100,
        statistics={"likes": 1, "viewCount": 1, "contacts": 1}
    )

    resp = client.create_item(data=create_data.model_dump())
    assert resp.status_code == 200, f"Не удалось создать: {resp.text}"

    response_json = resp.json()
    status_msg = response_json.get('status', '')

    # Извлекаем UUID из сообщения
    if '-' in status_msg:
        item_id = status_msg.split(' - ')[-1].strip()
    else:
        pytest.skip(f"Не удалось извлечь ID из ответа: {status_msg}")

    yield item_id

    client.delete_item_by_id(item_id)


# Фикстура для создания валидных JSON объявлений
@pytest.fixture()
def valid_create_payload(client):
    def _make(name: str = None, price: int = None, seller_id: int = None):
        return CreateItemRequest(
            sellerID=seller_id or client.seller_id,
            name=name or f"Item {uuid.uuid4()}",
            price=price if price is not None else 100,
            statistics={"likes": 1, "viewCount": 1, "contacts": 1}
        ).model_dump()

    return _make
