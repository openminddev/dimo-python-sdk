import json
import requests

class Request:
    def __init__(self, http_method, path, session):
        self.http_method = http_method
        self.path = path
        self.session = session
        self.default_headers = {
            'Content-Type': 'application/json',
        }

    def __call__(self, **kwargs):
        url = f"https://{self.path}"

        response = self.session.request (
            method = self.http_method,
            url = url,
            headers = self.default_headers,
            params = kwargs.get('params'),
            data = json.dumps(kwargs.get('data') if kwargs.get('data') else None)
        )

        response.raise_for_status() # Raises an HTTPError for bad responses, TEMPORARY*

        if response.content:
            return response.json()
        return None
