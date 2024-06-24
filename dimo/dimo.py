import requests
from request import Request
from endpoint import Endpoint
from environments import dimo_production, dimo_dev

class DIMO:
    _session = requests.Session()

    def __init__(self, env):
        self.env = env


    ### AUTH - Subject to Change based on web3 library ###
    # generate_challenge - /auth/web3/generate_challenge
    # sign_challenge - signChallenge [FUNCTION]
    # submit_challenge - /auth/web3/submit_challenge [POST]
    # get_token - getToken [FUNCTION]

    # vehicleV1 = Endpoint('/v1/vehicle')
    # vehicleV1.history = Request('GET',)
    # vehicleV2 = Endpoint
    ### DEVICE DATA ###
    # get_vehicle_history - /v2/vehicle/:tokenId/history [GET]
    # get_vehicle_status - /v2/vehicle/:tokenId/status [GET]
    # get_v1_vehicle_history - /v1/vehicle/:tokenId/history [GET]
    # get_v1_vehicle_status - /v1/vehicle/:tokenId/status [GET]
    # get_v1_vehicle_status_raw - /v1/vehicle/:tokenId/status-raw [GET]
    # get_user_device_status - /v1/user/device-data/:userDeviceId/status [GET]
    # get_user_device_history - /v1/user/device-data/:userDeviceId/historical [GET]
    # get_daily_distance - /v1/user/device-data/:userDeviceId/daily-distance [GET]
    # get_total_distance - /v1/user/device-data/:userDeviceId/distance-driven [GET]
    # send_json_export_email - /v1/user/device-data/:userDeviceId/export/json/email [POST]

    ### DEVICE DEFINITIONS ###
    # get_by_mmy - /device-definitions [GET]
    # get_by_id - /device-definitions/:id [GET]
    # list_device_makes - /device-makes [GET]
    deviceMakes = Request('GET', 'device-definitions-api.dimo.zone/device-makes', _session)
    # get_device_type_by_id - /device-types/:id [GET]

    ### DEVICES ###
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

    ### EVENTS ###
    # get_events - /v1/events [GET]

    ### TOKEN EXCHANGE ###
    # exchange - /v1/tokens/exchange [POST]

    ### TRIPS ###
    # trips - /v1/vehicle/:tokenId/trips [GET]

    ### USER ###
    # get_user - /v1/user [GET]
    # update_user - /v1/user [PUT]
    # delete_user - /v1/user [DELETE]
    # send_confirmation_email - /v1/user/send-confirmation-email [POST]
    # confirm_email - v1/user/confirm-email [POST]

    ### VALUATIONS ###
    # get_valuations - /v1/user/devices/:userDeviceId/valuations [GET]
    # get_instant_offer - /v1/user/devices/:userDeviceId/instant-offer [GET]
    # get_offers - /v1/user/devices/:userDeviceId/offers

    ### VEHICLE SIGNAL DECORDER ###
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

dimo = DIMO(dimo_production)
response = dimo.deviceMakes()
print(response)
