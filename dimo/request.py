import json
import requests
import re

class Request:

    session = requests.Session()

    def __init__(self, http_method, path, session):
        self.http_method = http_method
        self.path = path
        self.session = session
        self.default_headers = {
            'Content-Type': 'application/json',
        }

    def __call__(self, id=None, queryParams=None, **kwargs):
        obj_id = id
        query_params = queryParams

        selected_path = self._path_selector(self.path, obj_id)
        url = selected_path #The full URL is passed from the DIMO class.

        response = self.session.request (
            method=self.http_method,
            url=url,
            headers=self.default_headers,
            params=kwargs.get('params'),
            data=json.dumps(kwargs.get('data') if kwargs.get('data') else None)
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

    @staticmethod
    def _url_id_setter(url, obj_id):
        return re.sub(r':[a-z]*Id', obj_id, url)

    @staticmethod
    def _clean_params(raw_params):
        if type(raw_params) is str:
            params_arr = raw_params.split(",")
            params_dict = {}
            for parameter in params_arr:
                key, value = parameter.split("=")
                params_dict[key] = value
            return params_dict
        elif type(raw_params) is dict:
            return raw_params
