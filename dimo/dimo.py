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
        return self.request('POST', 'Auth', '/auth/web3/generate_challenge', data=data, headers=headers)

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

        form_data = {
            'client_id': client_id,
            'domain': domain,
            'state': challenge['state'],
            'signature': sign,
            'grant_type': grant_type
        }
        submit = await self.submit_challenge(form_data, headers)
        return submit
    ######################## DEVICE DATA - SWITCHING TO TELEMETRY ########################
    def get_vehicle_history(self, token_id):
        url = f'/v2/vehicle/{token_id}/history'
        return self.request('GET', 'DeviceData', url)

    def get_vehicle_status(self, token_id, **kwargs):
        return self.request('GET', 'DeviceData', '/v2/vehicle/:tokenId/status')

    def get_v1_vehicle_history(self, token_id, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/history')

    def get_v1_vehicle_status(self, token_id, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/status')

    def get_v1_vehicle_status_raw(self, token_id, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/status-raw')

    def get_user_device_status(self, userDeviceId, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/status')

    def get_user_device_history(self, userDeviceId, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/historical')

    def get_daily_distance(self, userDeviceId, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/daily-distance')

    def get_total_distance(self, userDeviceId, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/distance-driven')

    def send_json_export_email(self, userDeviceId, **kwargs):
        return self.request('POST', 'DeviceData', '/v1/user/device-data/:userDeviceId/export/json/email')

    ######################## DEVICE DEFINITIONS – BEING DEPRICATED ########################

    async def get_by_mmy(self, make, model, year):
        params = {
            'make': make,
            'model': model,
            'year': year
        }
        return self.request('GET', 'DeviceDefinitions', '/device-definitions', params=params)
    async def get_by_id(self, id):
        return self.request('GET', 'DeviceDefinitions', '/device-definitions/:id')
    async def list_device_makes(self):
        return self.request('GET', 'DeviceDefinitions', '/device-makes')
    async def get_device_type_by_id(self, id):
        return self.request('GET', 'DeviceDefinitions', '/device-types/:id')

    ######################## DEVICES ########################
    # create_vehicle - /v1/user/devices [POST]
    async def create_vehicle(self, access_token, country_code, device_definition_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'countryCode': country_code,
            'deviceDefinitionId': device_definition_id
        }
        return self.request('POST','Devices', '/v1/user/devices', headers=headers, params=params)
    # create_vehicle_from_smartcar - /v1/user/devices/fromsmartcar [POST]
    async def create_vehicle_from_smartcar(self, access_token, code, country_code, redirect_uri):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'code': code,
            'countryCode': country_code,
            'redirectURI': redirect_uri
        }
        return self.request('POST', 'Devices', '/v1/user/devices/fromsmartcar', headers=headers, params=params)
    # create_vehicle_from_vin - /v1/user/devices/fromvin [POST]
    async def create_vehicle_from_vin(self, access_token, can_protocol, country_code, vin):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'canProtocol': can_protocol,
            'countryCode': country_code,
            'vin': vin
        }
        return self.request('POST', 'Devices', '/v1/user/devices/fromvin', headers=headers, params=params)
    # update_vehicle_vin - /v1/user/devices/:userDeviceId/vin [PATCH]
    async def update_vehicle_vin(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/vin'
        return self.request('PATCH', 'Devices', url, headers=headers)
    # get_claiming_payload - /v1/aftermarket/device/by-serial/:serial/commands/claim [POST]
    async def get_claiming_payload(self, access_token, serial):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/aftermarket/device/by-serial/{serial}/commands/claim'
        return self.request('POST', 'Devices', url, headers=headers)
    # sign_claiming_payload - /v1/aftermarket/device/by-serial/:serial/commands/claim [POST]
    async def sign_claiming_payload(self, access_token, serial, claim_request):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'claimRequest': claim_request
        }
        url = f'/v1/aftermarket/device/by-serial/{serial}/commands/claim'
        return self.request('POST', 'Devices', url, headers=headers, params=params)
    # get_minting_payload - /v1/user/devices/:userDeviceId/commands/mint [POST]
    async def get_minting_payload(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/commands/mint'
        return self.request('POST', 'Devices', url, headers=headers)
    # sign_minting_payload - /v1/user/devices/:userDeviceId/commands/mint [POST]
    async def sign_minting_payload(self, access_token, user_device_id, mint_request):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'mintRequest': mint_request
        }
        url = f'/v1/user/devices/{user_device_id}/commands/mint'
        return self.request('POST', 'Devices', url, headers=headers, params=params)
    # opt_in_share_data - /v1/user/devices/:userDeviceId/commands/opt-in [POST]
    async def opt_in_share_data(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/commands/opt-in'
        return self.request('POST', 'Devices', url, headers=headers)
    # refresh_smartcar_data - /v1/user/devices/:userDeviceId/commands/refresh [POST]
    async def refresh_smartcar_data(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/commands/refresh'
        return self.request('POST', 'Devices', url, headers=headers)
    # get_pairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/pair [GET]
    async def get_pairing_payload(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/pair'
        return self.request('GET', 'Devices', url, headers=headers)
    # sign_pairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/pair [POST]
    async def sign_pairing_payload(self, access_token, user_device_id, user_signature):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'userSignature': user_signature
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/pair'
        return self.request('POST', 'Devices', url, headers=headers, params=params)
    # get_unpairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/unpair [GET]
    async def get_unpairing_payload(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/unpair'
        return self.request('GET', 'Devices', url, headers=headers)
    # sign_unpairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/unpair [POST]
    async def sign_unpairing_payload(self, access_token, user_device_id, user_signature):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'userSignature': user_signature
        }
        url = f'/v1/user/devices/{user_device_id}/aftermarket/commands/unpair'
        return self.request('POST', 'Devices', url, headers=headers, params=params)
    # lock_doors - /v1/vehicle/:tokenId/commands/doors/lock [POST]
    async def lock_doors(self, privilege_token, token_id):
        headers = {
            'Authorization': f'Bearer {privilege_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/vehicle/{token_id}/commands/doors/lock'
        return self.request('POST', 'Devices', url, headers=headers)
    # unlock_doors - /v1/vehicle/:tokenId/commands/doors/unlock [POST]
    async def unlock_doors(self, privilege_token, token_id):
        headers = {
            'Authorization': f'Bearer {privilege_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/vehicle/{token_id}/commands/doors/unlock'
        return self.request('POST', 'Devices', url, headers=headers)
    # open_frunk - /v1/vehicle/:tokenId/commands/frunk/open [POST]
    async def open_frunk(self, privilege_token, token_id):
        headers = {
            'Authorization': f'Bearer {privilege_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/vehicle/{token_id}/commands/frunk/open'
        return self.request('POST', 'Devices', url, headers=headers)
    # open_trunck - /v1/vehicle/:tokenId/commands/trunk/open [POST]
    async def open_trunk(self, privilege_token, token_id):
        headers = {
            'Authorization': f'Bearer {privilege_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/vehicle/{token_id}/commands/trunk/open'
        return self.request('POST', 'Devices', url, headers=headers)
    # list_error_codes - /v1/user/devices/:userDeviceId/error-codes [GET]
    async def list_error_codes(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/error-codes'
        return self.request('GET', 'Devices', url, headers=headers)
    # submit_error_codes - /v1/user/devices/:userDeviceId/error-codes [POST]
    async def submit_error_codes(self, access_token, user_device_id, query_device_error_codes):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'queryDeviceErrorCodes': query_device_error_codes
        }
        url = f'/v1/user/devices/{user_device_id}/error-codes'
        return self.request('POST', 'Devices', url, headers=headers, params=params)
    # clear_error_codes - /v1/user/devices/:userDeviceId/error-codes/clear [POST]
    async def clear_error_codes(self, access_token, user_device_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = f'/v1/user/devices/{user_device_id}/error-codes/clear'
        return self.request('POST', 'Devices', url, headers=headers)
    # get_aftermarket_device - /v1/aftermarket/device/:tokenId [GET]
    async def get_aftermarket_device(self, token_id):
        url = f'/v1/aftermarket/device/{token_id}'
        self.request('GET', 'Devices', url)
    # get_aftermarket_device_image - /v1/aftermarket/device/:tokenId/image [GET]
    async def get_aftermarket_device_image(self, token_id):
        url = f'/v1/aftermarket/device/{token_id}/image'
        self.request('GET', 'Devices', url)
    # get_aftermarket_device_metadata_by_address - /v1/aftermarket/device/by-address/:address [GET]
    async def get_aftermarket_device_metadata_by_address(self, address):
        url = f'/v1/aftermarket/device/by-address/{address}'
        self.request('GET', 'Devices', url)

    ######################## EVENTS ########################
    # get_events - /v1/events [GET]

    ######################## TOKEN EXCHANGE ########################
    # exchange - /v1/tokens/exchange [POST]
    async def token_exchange(self, access_token, privileges, token_id, env="Production"):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'nftContractAddress':  dimo_constants[env]['NFT_address'],
            'privileges': privileges,
            'tokenId': token_id
        }
        return self.request('POST', 'TokenExchange', '/v1/tokens/exchange', headers=headers, params=params)

    ######################## TRIPS ########################
    # trips - /v1/vehicle/:tokenId/trips [GET]

    ######################## USER ########################
    async def user(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        return self.request('GET', 'User', '/v1/user', headers=headers)

    async def update_user(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        return self.request('PUT', 'User', '/v1/user', headers=headers)

    async def delete_user(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        return self.request('DELETE', 'User', '/v1/user', headers=headers)
    # send_confirmation_email - /v1/user/send-confirmation-email [POST]
    # confirm_email - v1/user/confirm-email [POST]

    ######################## VALUATIONS ########################
    # get_valuations - /v1/user/devices/:userDeviceId/valuations [GET]
    # get_instant_offer - /v1/user/devices/:userDeviceId/instant-offer [GET]
    # get_offers - /v1/user/devices/:userDeviceId/offers

    ######################## VEHICLE SIGNAL DECORDER ########################
    # list_config_urls_by_vin - /v1/device-config/vin/:vin/urls [GET]
    # list_config_urls_by_address - /v1/device-config/eth-addr/:address/urls [GET]
    # get_pid_configs - /v1/device-config/pids/:templateName [GET]
    # get_device_settings - /v1/device-config/settings/:templateName [GET]
    # get_dbc_text - /v1/device-config/dbc/:templateName [GET]
    # get_device_status_by_address - /v1/device-config/eth-addr/:address/status [GET]
    # set_device_status_by_address - /v1/device-config/eth-addr/:address/status [PATCH]
    # get_jobs_by_address - /v1/device-config/eth-addr/:address/jobs [GET]
    # get_pending_jobs_by_address - /v1/device-config/eth-addr/:address/jobs/pending
    # set_job_status_by_address - /v1/device-config/eth-addr/:address/jobs/:jobId/:status
