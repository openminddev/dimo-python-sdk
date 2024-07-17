from auth import Auth
from device_data import DeviceData
from device_definitions import DeviceDefinitions
from devices import Devices
from events import Events
from token_exchange import TokenExchange
from trips import Trips
from user import User
from valuations import Valuations
from vehicle_signal_decoding import VehicleSignalDecoding

from identity import Identity
from telemetry import Telemetry

import requests
from request import Request
from environments import dimo_environment
import asyncio
import re
import urllib.parse


class DIMO:

    def __init__(self, env="Production"):
        self.env = env
        self.urls = dimo_environment[env]
        self.auth = Auth(self.request, self._get_auth_headers)
        self.device_data = DeviceData(self.request, self._get_auth_headers)
        self.device_definitions = DeviceDefinitions(self.request, self._get_auth_headers)
        self.devices = Devices(self.request, self._get_auth_headers)
        self.events = Events(self.request, self._get_auth_headers)
        self.token_exchange = TokenExchange(self.request, self._get_auth_headers)
        self.trips = Trips(self.request, self._get_auth_headers)
        self.user = User(self.request, self._get_auth_headers)
        self.valuations = Valuations(self.request, self._get_auth_headers)
        self.vehicle_signal_decoding = VehicleSignalDecoding(self.request, self._get_auth_headers)
        self.identity = Identity(self)
        self.telemetry = Telemetry(self)
        self._session = Request.session

    def _get_full_path(self, service, path, params=None):
        base_path = self.urls[service] # Set a base_path for the DIMO service you're using
        full_path = f"{base_path}{path}"

        if params:
            for key, value in params.items():
                pattern = f":{key}"
                full_path = re.sub(pattern, str(value), full_path)
        return full_path # Return the full path of the endpoint you'll make a request to.

    def _get_auth_headers(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    # TODO: Cleanup **kwargs as needed
    def request(self, http_method, service, path, **kwargs):
        full_path = self._get_full_path(service, path) # Get full path to make request
        return Request(http_method, full_path, self._session)(**kwargs)

    async def query(self, service, query, variables=None, token=None):
        headers = self._get_auth_headers(token) if token else {}
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = 'dimo-python-sdk'

        data = {
            'query': query,
            'variables': variables or {}
        }

        response = self.request(
            'POST',
            service,
            '',
            headers=headers,
            data=data
        )
        return response
