import os
import sqlite3

import requests
import urllib.parse
from retrying import retry


class ProPublicaAPI(object):
    """A rudimentary interface to the ProPublica Congress API.
    Implements a few of the endpoints. Requires an API key.
    Also implements exponential backoff retrying.
    """
    API_ROOT = "https://api.propublica.org/congress/v1/"

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key' : self.api_key,
            'cache-control': 'no-cache'
        })

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max = 10000,
        stop_max_attempt_number=5
    )
    def bills_search(self, query_text):
        """
        Query the ProPublica Congress API
        Bills endpoint for bills containing query text.

        Returns JSON unless a non-200 status code is returned,
        then it will retry with exponential backoff up to
        5 times. Raises requests.HTTPError.
        """
        query_url = os.path.join(
            ProPublicaAPI.API_ROOT,
            'bills',
            'search.json'
        )
        params = {
            "query" : "\"" + query_text + "\""
        }

        response = self.session.get(query_url, params=params)
        response.raise_for_status()
        response_json = response.json()
        if response_json['results'][0]['offset'] > 0: raise NotImplementedError("Pagination not enabled. ")
        return response_json['results'][0]['bills']
