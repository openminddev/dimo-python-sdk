import requests
from request import Request
from endpoint import Endpoint
from environments import dimo_environment
from constants import dimo_constants
import asyncio
import re
import urllib.parse
from eth_account.messages import encode_defunct
from web3 import Web3


class DIMO:

    def __init__(self, env="Production"):
        self.env = env
        self.urls = dimo_environment[env]
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

    ######################## AUTH ########################

    async def generate_challenge(self,
        client_id,
        domain,
        scope,
        response_type,
        address,
        headers):
        data = {
            'client_id': client_id,
            'domain': domain,
            'scope': scope,
            'response_type': response_type,
            'address': address
        }
        return self.request(
            'POST',
            'Auth',
            '/auth/web3/generate_challenge',
            data=data,
            headers=headers
        )

    async def sign_challenge(self, message, private_key, env="Production"):
        web3 = Web3(Web3.HTTPProvider(dimo_constants[env]['RPC_provider']))
        signed_message = web3.eth.account.sign_message(encode_defunct(text=message), private_key=private_key)
        return signed_message.signature.hex()

    async def submit_challenge(self, form_data, headers):
        return self.request('POST', 'Auth', '/auth/web3/submit_challenge', data=form_data, headers=headers)

    async def get_token(self, client_id, domain, scope, response_type, address, private_key, grant_type="authorization_code", env="Production"):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        challenge = await self.generate_challenge(
            headers=headers,
            client_id=client_id,
            domain=domain,
            scope=scope,
            response_type=response_type,
            address=address
        )

        sign = await self.sign_challenge(
            message=challenge['challenge'],
            private_key=private_key,
            env=env
        )

        body = {
            'client_id': client_id,
            'domain': domain,
            'state': challenge['state'],
            'signature': sign,
            'grant_type': grant_type
        }
        submit = await self.submit_challenge(body, headers)
        return submit
    ######################## DEVICE DATA  ########################
    ######################## LEGACY/DEPRECATED: SEE DOCS:
    # https://docs.dimo.zone/developer-platform/rest-api-references/dimo-protocol/device-data-api/device-data-api-endpoints

    async def get_vehicle_history(self, privileged_token, token_id):
        url = f'/v2/vehicle/{token_id}/history'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(privileged_token)
        )

    async def get_vehicle_status(self, privileged_token, token_id):
        url = f'/v2/vehicle/{token_id}/status'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(privileged_token)
        )

    async def get_v1_vehicle_history(self, privileged_token, token_id):
        url = f'/v1/vehicle/{token_id}/history'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(privileged_token)
        )

    async def get_v1_vehicle_status(self, privileged_token, token_id):
        url = f'/v1/vehicle/{token_id}/status'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(privileged_token)
        )

    async def get_v1_vehicle_status_raw(self, privileged_token, token_id):
        url = f'/v1/vehicle/{token_id}/status-raw'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(privileged_token)
        )

    async def get_user_device_status(self, access_token, user_device_id):
        url = f'/v1/user/device-data/{user_device_id}/status'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_user_device_history(self, access_token, user_device_id, start_date=None, end_date=None):
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        url = f'/v1/user/device-data/{user_device_id}/historical'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def get_daily_distance(self, access_token, user_device_id, time_zone):
        params = {
            'timeZone': time_zone
        }
        url = f'/v1/user/device-data/{user_device_id}/daily-distance'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(access_token),
            params=params)

    async def get_total_distance(self, access_token, user_device_id):
        url = f'/v1/user/device-data/{user_device_id}/distance-driven'
        return self.request(
            'GET',
            'DeviceData',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def send_json_export_email(self, access_token, user_device_id):
        url = f'/v1/user/device-data/{user_device_id}/export/json/email'
        return self.request(
            'POST',
            'DeviceData',
            url,
            headers=self._get_auth_headers(access_token)
        )

    ######################## DEVICE DEFINITIONS ########################
    ######################## LEGACY/DEPRECATED: SEE DOCS:
    # https://docs.dimo.zone/developer-platform/rest-api-references/dimo-protocol/device-definitions-api/device-definitions-api-endpoints

    async def get_by_mmy(self, make, model, year):
        params = {
            'make': make,
            'model': model,
            'year': year
        }
        return self.request(
            'GET',
            'DeviceDefinitions',
            '/device-definitions',
            params=params
        )

    async def get_by_id(self, id):
        url = f'/device-definitions/{id}'
        return self.request(
            'GET',
            'DeviceDefinitions',
            url)

    async def list_device_makes(self):
        return self.request(
            'GET',
            'DeviceDefinitions',
            '/device-makes'
        )

    async def get_device_type_by_id(self, id):
        url = f'/device-types/{id}'
        return self.request(
            'GET',
            'DeviceDefinitions',
            url)

    ######################## DEVICES ########################

    async def create_vehicle(self, access_token, country_code, device_definition_id):
        params = {
            'countryCode': country_code,
            'deviceDefinitionId': device_definition_id
        }
        return self.request(
            'POST',
            'Devices',
            '/v1/user/devices',
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def create_vehicle_from_smartcar(self, access_token, code, country_code, redirect_uri):
        params = {
            'code': code,
            'countryCode': country_code,
            'redirectURI': redirect_uri
        }
        return self.request(
            'POST',
            'Devices',
            '/v1/user/devices/fromsmartcar',
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def create_vehicle_from_vin(self, access_token, can_protocol, country_code, vin):
        params = {
            'canProtocol': can_protocol,
            'countryCode': country_code,
            'vin': vin
        }
        return self.request(
            'POST',
            'Devices',
            '/v1/user/devices/fromvin',
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def update_vehicle_vin(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/vin'
        return self.request(
            'PATCH',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_claiming_payload(self, access_token, serial):
        url = f'/v1/aftermarket/device/by-serial/{serial}/commands/claim'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def sign_claiming_payload(self, access_token, serial, claim_request):
        params = {
            'claimRequest': claim_request
        }
        url = f'/v1/aftermarket/device/by-serial/{serial}/commands/claim'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def get_minting_payload(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/commands/mint'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def sign_minting_payload(self, access_token, user_device_id, mint_request):
        params = {
            'mintRequest': mint_request
        }
        url = f'/v1/user/devices/{user_device_id}/commands/mint'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def opt_in_share_data(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/commands/opt-in'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def refresh_smartcar_data(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/commands/refresh'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_pairing_payload(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/pair'
        return self.request(
            'GET',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def sign_pairing_payload(self, access_token, user_device_id, user_signature):
        params = {
            'userSignature': user_signature
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/pair'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def get_unpairing_payload(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/unpair'
        return self.request(
            'GET',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def sign_unpairing_payload(self, access_token, user_device_id, user_signature):
        params = {
            'userSignature': user_signature
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/unpair'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def lock_doors(self, privilege_token, token_id):
        url = f'/v1/vehicle/{token_id}/commands/doors/lock'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    async def unlock_doors(self, privilege_token, token_id):
        url = f'/v1/vehicle/{token_id}/commands/doors/unlock'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    async def open_frunk(self, privilege_token, token_id):
        url = f'/v1/vehicle/{token_id}/commands/frunk/open'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    async def open_trunk(self, privilege_token, token_id):
        url = f'/v1/vehicle/{token_id}/commands/trunk/open'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    async def list_error_codes(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/error-codes'
        return self.request(
            'GET',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def submit_error_codes(self, access_token, user_device_id, query_device_error_codes):
        params = {
            'queryDeviceErrorCodes': query_device_error_codes
        }
        url = f'/v1/user/devices/{user_device_id}/error-codes'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token),
            params=params
        )

    async def clear_error_codes(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/error-codes/clear'
        return self.request(
            'POST',
            'Devices',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_aftermarket_device(self, token_id):
        url = f'/v1/aftermarket/device/{token_id}'
        self.request(
            'GET',
            'Devices',
            url
        )

    async def get_aftermarket_device_image(self, token_id):
        url = f'/v1/aftermarket/device/{token_id}/image'
        self.request(
            'GET',
            'Devices',
            url
        )

    async def get_aftermarket_device_metadata_by_address(self, address):
        url = f'/v1/aftermarket/device/by-address/{address}'
        self.request(
            'GET',
            'Devices',
            url
        )

    ######################## EVENTS ########################

    # get_events - /v1/events [GET]
    async def get_events(self, access_token):
        return self.request(
            'GET',
            'Events',
            '/v1/events',
            headers=self._get_auth_headers(access_token)
        )

    ######################## TOKEN EXCHANGE ########################

    async def token_exchange(self, access_token, privileges, token_id, env="Production"):
        body = {
                'nftContractAddress':  dimo_constants[env]['NFT_address'],
                'privileges': privileges,
                'tokenId': token_id
            }
        response = self.request(
            'POST',
            'TokenExchange',
            '/v1/tokens/exchange',
            headers=self._get_auth_headers(access_token),
            data=body
        )
        return response

    ######################## TRIPS ########################
    async def trips(self, privilege_token, token_id):
        url = f'/v1/vehicle/{token_id}/trips'
        return self.request(
            'GET',
            'Trips',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    ######################## USER ########################
    async def user(self, access_token):
        return self.request(
            'GET',
            'User',
            '/v1/user',
            headers=self._get_auth_headers(access_token)
        )

    async def update_user(self, access_token):
        return self.request(
            'PUT',
            'User',
            '/v1/user',
            headers=self._get_auth_headers(access_token)
        )

    async def delete_user(self, access_token):
        return self.request(
            'DELETE',
            'User',
            '/v1/user',
            headers=self._get_auth_headers(access_token)
        )

    async def send_confirmation_email(self, access_token):
        return self.request(
            'POST',
            'User',
            '/v1/user/send-confirmation-email',
            headers=self._get_auth_headers(access_token)
        )

    async def confirm_email(self, access_token, confirm_email_request):
        params = {
            'confirmEmailRequest': confirm_email_request
        }
        return self.request(
            'POST',
            'User',
            '/v1/user/confirm-email',
            headers=self._get_auth_headers(access_token)
        )

    ######################## VALUATIONS ########################

    async def get_valuations(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/valuations'
        return self.request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_instant_offer(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/instant-offer'
        return self.request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )

    async def get_offers(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/offers'
        return self.request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )

    ######################## VEHICLE SIGNAL DECORDER ########################

    async def list_config_urls_by_vin(self, vin, protocol=None):
        params = {
            'protocol': protocol
        }
        url = f'/v1/device-config/vin/{vin}/urls'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url,
            params=params
        )

    async def list_config_urls_by_address(self, address, protocol=None):
        params = {
            'protocol': protocol
        }
        url = f'/v1/device-config/eth-addr/{address}/urls'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url,
            params=params
        )

    async def get_pid_configs(self, template_name):
        url = f'/v1/device-config/pids/{template_name}'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def get_device_settings(self, template_name):
        url = f'/v1/device-config/settings/{template_name}'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def get_dbc_text(self, template_name):
        url = f'/v1/device-config/dbc/{template_name}'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def get_device_status_by_address(self, address):
        url = f'/v1/device-config/eth-addr/{address}/status'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def set_device_status_by_address(self, privilege_token, address):
        url = f'/v1/device-config/eth-addr/{address}/status'
        return self.request(
            'PATCH',
            'VehicleSignalDecoding',
            url,
            headers=self._get_auth_headers(privilege_token)
        )

    async def get_jobs_by_address(self, address):
        url = f'/v1/device-config/eth-addr/{address}/jobs'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def get_pending_jobs_by_address(self, address):
        url = f'/v1/device-config/eth-addr/{address}/jobs/pending'
        return self.request(
            'GET',
            'VehicleSignalDecoding',
            url
        )

    async def set_job_status_by_address(self, privilege_token, address, job_id, status):
        url = f'/v1/device-config/eth-addr/{address}/jobs/{job_id}/{status}'
        return self.request(
            'PATCH',
            'VehicleSignalDecoding',
            url,
            headers=self._get_auth_headers(privilege_token)
        )
