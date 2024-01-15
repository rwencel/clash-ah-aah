import requests
import json
from types import SimpleNamespace

class ClashAPI:
    _api_url = "https://api.clashroyale.com/v1"
    def _api_url_get_player(self, playerTag): return f"{self._api_url}/players/%23{playerTag}"
    def _api_url_get_player_battlelog(self, playerTag): return f"{self._api_url}/players/%23{playerTag}/battlelog"

    _api_key: str

    def __init__(self, api_key):
        self._api_key = api_key

    def get_player(self, playerTag):
        url = self._api_url_get_player(playerTag)
        data = {}
        return self._get(url, data)

    def _get(self, url, data):
        headers = {"Authorization": f"Bearer {self._api_key}"}
        response = requests.get(url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception(response.reason)
        # decode the JSON response into a Python object
        return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))