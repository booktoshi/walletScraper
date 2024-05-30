import requests
from typing import List
from collections import defaultdict
import concurrent.futures

class CollectionController:
    BASE_URL = "https://dogeturbo.ordinalswallet.com"

    def get_inscription_data(self, inscription_id: str) -> dict:
        response = requests.get(f"{self.BASE_URL}/inscription/{inscription_id}")
        if response.ok:
            return response.json()
        return {"error": "Failed to fetch inscription data"}

    def get_collection_inscriptions(self, collection_slug: str, skip: int, limit: int) -> List[str]:
        api_url = f"{self.BASE_URL}/collection/{collection_slug}/inscriptions"
        response = requests.get(api_url)
        if response.ok:
            inscription_ids = [inscription['id'] for inscription in response.json()]
            inscription_ids.sort()
            return inscription_ids[skip:skip+limit]
        return []

    def get_collection_data(self, collection_slug: str, skip: int, limit: int) -> List[dict]:
        inscription_ids = self.get_collection_inscriptions(collection_slug, skip, limit)
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            collection_data = list(executor.map(self.get_inscription_data, inscription_ids))
        collection_dict = defaultdict(list)
        for data in collection_data:
            dict_key = f'{data["address"]}_{data["id"]}'
            collection_dict[dict_key].append(data)
        response = [
            {
                "address": key.split("_")[0],
                "id": key.split("_")[1],
                "names": [v["name"] for v in value],
                "amount": len(value)
            }
            for key, value in collection_dict.items()
        ]
        return response

    def get_wallet_balance(self, address: str) -> dict:
        response = requests.get(f"{self.BASE_URL}/wallet/{address}")
        if response.ok:
            return response.json()
        return {"error": "Failed to fetch wallet balance"}

    def get_collection_stats(self, collection_slug: str) -> dict:
        response = requests.get(f"{self.BASE_URL}/collection/{collection_slug}/stats")
        if response.ok:
            return response.json()
        return {"error": "Failed to fetch collection stats"}

    def get_ordinals_wallet_inscriptions(self, address: str, filter_id: str = None) -> List[dict]:
        """Fetches inscriptions for a given wallet address, optionally filtering by inscription ID."""
        params = {}
        if filter_id:
            params['filter_id'] = filter_id
        response = requests.get(f"{self.BASE_URL}/wallet/{address}/inscriptions", params=params)
        if response.ok:
            return response.json()
        return {"error": "Failed to fetch ordinals wallet inscriptions"}
