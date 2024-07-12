import json
import requests
import re
import urllib.parse

class Request:

    session = requests.Session()

    def __init__(self, http_method, path, session):
        self.http_method = http_method
        self.path = path
        self.session = session
        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def __call__(self, id=None, queryParams=None, **kwargs):
        obj_id = id
        query_params = queryParams
        selected_path = self._path_selector(self.path, obj_id)
        url = selected_path # The full URL is passed from the DIMO class.
        headers = {**self.default_headers, **kwargs.get('headers', {})}
        params = {**(queryParams or {}), **(kwargs.get('params') or {})}

        if 'data' in kwargs and headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            data = urllib.parse.urlencode(kwargs['data'])
        else:
            data = json.dumps(kwargs.get('data')) if kwargs.get('data') else None

        response = self.session.request (
            method=self.http_method,
            url=url,
            headers=headers,
            params=kwargs.get('params'),
            data=data
        )

        response.raise_for_status() # Raises an HTTPError for bad responses, TEMPORARY*

        if response.content:
            return response.json()
        return None

    @staticmethod
    def _path_selector(path, _id):
        if type(path) is str:
            return path
        get_url, get_url_by_id = path
        return get_url if not _id else get_url_by_id
