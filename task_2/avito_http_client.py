import requests
from typing import Optional
import random


class AvitoHttpClient:

    # Инициализация http клиента. В аргументы принимает base_url - url апишки,
    # и seller_id, если не передан, то генерируется сам
    def __init__(self, base_url: str = "https://qa-internship.avito.com", seller_id: Optional[int] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.base_url = base_url.rstrip('/')
        self.seller_id = seller_id if seller_id else random.randint(111111, 999999)

    # API v1. Ручки по пути /api/1

    # GET /api/1/item/:id
    def get_item_by_id(self, item_id):
        url = f"{self.base_url}/api/1/item/{item_id}"
        return self.session.get(url)

    # GET /api/1/:sellerID/item
    def get_items_by_seller(self, seller_id: int):
        url = f"{self.base_url}/api/1/{seller_id}/item"
        return self.session.get(url)

    # POST /api/1/item
    def create_item(self, data: dict):
        url = f"{self.base_url}/api/1/item"
        return self.session.post(url, json=data)

    # GET /api/1/statistic/:id
    def get_statistics_v1(self, item_id):
        url = f"{self.base_url}/api/1/statistic/{item_id}"
        return self.session.get(url)

    # API v2. Ручки по пути /api/2

    # DELETE /api/2/item/:id (хоть в проверке и не участвует, все равно полезна для тестовых сценариев)
    def delete_item_by_id(self, item_id):
        url = f"{self.base_url}/api/2/item/{item_id}"
        return self.session.delete(url)

    # GET /api/2/statistic/:id
    def get_statistics_v2(self, item_id):
        url = f"{self.base_url}/api/2/statistic/{item_id}"
        return self.session.get(url)
