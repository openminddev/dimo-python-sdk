import requests
from request import Request
from endpoint import Endpoint
from environments import dimo_environment

class DIMO:

    def __init__(self, env="Production"):
        self.env = env
        self.urls = dimo_environment[self.env]
        self._session = Request.session

    def _get_full_path(self, service, path):
        base_path = self.urls[service] # Set a base_path for the DIMO service you're using
        return f"{base_path}{path}" # Return the full path of the endpoint you'll make a request to.

    # TODO: Cleanup **kwargs as needed
    def request(self, http_method, service, path, **kwargs):
        full_path = self._get_full_path(service, path) # Get full path to make request
        return Request(http_method, full_path, self._session)(**kwargs)

    def get_devices(self, **kwargs):
        return self.request('GET', 'Devices', '/v1/devices', **kwargs )


    ######################## AUTH - Subject to Change based on web3 library ########################
    # generate_challenge - /auth/web3/generate_challenge
    # sign_challenge - signChallenge [FUNCTION]
    # submit_challenge - /auth/web3/submit_challenge [POST]
    # get_token - getToken [FUNCTION]


    ######################## DEVICE DATA ########################
    def get_vehicle_history(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v2/vehicle/:tokenId/history')

    def get_vehicle_status(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v2/vehicle/:tokenId/status')

    def get_v1_vehicle_history(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/history')

    def get_v1_vehicle_status(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/status')

    def get_v1_vehicle_status_raw(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/vehicle/:tokenId/status-raw')

    def get_user_device_status(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/status')

    def get_user_device_history(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/historical')

    def get_daily_distance(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/daily-distance')

    def get_total_distance(self, **kwargs):
        return self.request('GET', 'DeviceData', '/v1/user/device-data/:userDeviceId/distance-driven')

    def send_json_export_email(self, **kwargs):
        return self.request('POST', 'DeviceData', '/v1/user/device-data/:userDeviceId/export/json/email')

    ######################## DEVICE DEFINITIONS ########################
    # get_by_mmy - /device-definitions [GET]
    def get_by_mmy(self, **kwargs):
        return self.request('GET', 'DeviceDefinitions', '/device-definitions')
    # get_by_id - /device-definitions/:id [GET]
    # list_device_makes - /device-makes [GET]
    def list_device_makes(self):
        return self.request('GET', 'DeviceDefinitions', '/device-makes')
    # get_device_type_by_id - /device-types/:id [GET]

    ######################## DEVICES ########################
    # create_vehicle - /v1/user/devices [POST]
    # create_vehicle_from_smartcar - /v1/user/devices/fromsmartcar [POST]
    # create_vehicle_from_vin - /v1/user/devices/fromvin [POST]
    # update_vehicle_vin - /v1/user/devices/:userDeviceId/vin [PATCH]
    # get_claiming_payload - /v1/aftermarket/device/by-serial/:serial/commands/claim [POST]
    # sign_claiming_payload - /v1/aftermarket/device/by-serial/:serial/commands/claim [POST]
    # get_minting_payload - /v1/user/devices/:userDeviceId/commands/mint [POST]
    # sign_minting_payload - /v1/user/devices/:userDeviceId/commands/mint [POST]
    # opt_in_share_data - /v1/user/devices/:userDeviceId/commands/opt-in [POST]
    # refresh_smartcar_data - /v1/user/devices/:userDeviceId/commands/refresh [POST]
    # get_pairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/pair [GET]
    # sign_pairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/pair [POST]
    # get_unpairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/unpair [GET]
    # sign_unpairing_payload - /v1/user/devices/:userDeviceId/aftermarket/commands/unpair [POST]
    # lock_doors - /v1/vehicle/:tokenId/commands/doors/lock [POST]
    # unlock_doors - /v1/vehicle/:tokenId/commands/doors/unlock [POST]
    # open_frunk - /v1/vehicle/:tokenId/commands/frunk/open [POST]
    # open_trunck - /v1/vehicle/:tokenId/commands/trunk/open [POST]
    # list_error_codes - /v1/user/devices/:userDeviceId/error-codes [GET]
    # submit_error_codes - /v1/user/devices/:userDeviceId/error-codes [POST]
    # clean_error_codes - /v1/user/devices/:userDeviceId/error-codes/clear [POST]
    # get_aftermarket_device - /v1/aftermarket/device/:tokenId [GET]
    # get_aftermarket_device_image - /v1/aftermarket/device/:tokenId/image [GET]
    # get_aftermarket_device_metadata_by_address - /v1/aftermarket/device/by-address/:address [GET]

    ######################## EVENTS ########################
    # get_events - /v1/events [GET]

    ######################## TOKEN EXCHANGE ########################
    # exchange - /v1/tokens/exchange [POST]

    ######################## TRIPS ########################
    # trips - /v1/vehicle/:tokenId/trips [GET]

    ######################## USER ########################
    # get_user - /v1/user [GET]
    # update_user - /v1/user [PUT]
    # delete_user - /v1/user [DELETE]
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

dimo = DIMO("Production")
print(dimo.get_by_mmy(make="Lexus", model="NX", year="2021"))
