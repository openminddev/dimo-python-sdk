class Devices:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def create_vehicle(
        self, access_token: str, country_code: str, device_definition_id: str
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(country_code, str):
            raise TypeError("country_code must be a string.")
        if not isinstance(device_definition_id, str):
            raise TypeError("device_definition_id must be a string.")
        body = {"countryCode": country_code, "deviceDefinitionId": device_definition_id}
        return self._request(
            "POST",
            "Devices",
            "/v1/user/devices",
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def create_vehicle_from_smartcar(
        self, access_token: str, code: str, country_code: str, redirect_uri: str
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(code, str):
            raise TypeError("code must be a string.")
        if not isinstance(country_code, str):
            raise TypeError("country_code must be a string.")
        if not isinstance(redirect_uri, str):
            raise TypeError("redirect_uri must be a string.")
        body = {"code": code, "countryCode": country_code, "redirectURI": redirect_uri}
        return self._request(
            "POST",
            "Devices",
            "/v1/user/devices/fromsmartcar",
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def create_vehicle_from_vin(
        self, access_token: str, can_protocol: str, country_code: str, vin: str
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(can_protocol, str):
            raise TypeError("can_protocol must be a string.")
        if not isinstance(country_code, str):
            raise TypeError("country code must be a string.")
        if not isinstance(vin, str):
            raise TypeError("vin must be a string.")
        body = {"canProtocol": can_protocol, "countryCode": country_code, "vin": vin}
        return self._request(
            "POST",
            "Devices",
            "/v1/user/devices/fromvin",
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def update_vehicle_vin(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/vin"
        return self._request(
            "PATCH", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def get_claiming_payload(self, access_token: str, serial: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(serial, str):
            raise TypeError("serial must be a string.")
        url = f"/v1/aftermarket/device/by-serial/{serial}/commands/claim"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def sign_claiming_payload(
        self, access_token: str, serial: str, claim_request: dict
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(serial, str):
            raise TypeError("serial must be a string.")
        if not isinstance(claim_request, dict):
            raise TypeError("claim_request must be a string.")
        body = {"claimRequest": claim_request}
        url = f"/v1/aftermarket/device/by-serial/{serial}/commands/claim"
        return self._request(
            "POST",
            "Devices",
            url,
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def get_minting_payload(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/commands/mint"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def sign_minting_payload(
        self, access_token: str, user_device_id: str, mint_request: dict
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        if not isinstance(mint_request, dict):
            raise TypeError("mint_request must be a dict.")
        body = {"mintRequest": mint_request}
        url = f"/v1/user/devices/{user_device_id}/commands/mint"
        return self._request(
            "POST",
            "Devices",
            url,
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def opt_in_share_data(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/commands/opt-in"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def refresh_smartcar_data(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/commands/refresh"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def get_pairing_payload(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/aftermarket/commands/pair"
        return self._request(
            "GET", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def sign_pairing_payload(
        self, access_token: str, user_device_id: str, user_signature: str
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        if not isinstance(user_signature, str):
            raise TypeError("user_signature must be a string.")
        body = {"userSignature": user_signature}
        url = f"/v1/user/devices/{user_device_id}/aftermarket/commands/pair"
        return self._request(
            "POST",
            "Devices",
            url,
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def get_unpairing_payload(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/aftermarket/commands/unpair"
        return self._request(
            "GET", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def sign_unpairing_payload(
        self, access_token: str, user_device_id: str, user_signature: str
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        if not isinstance(user_signature, str):
            raise TypeError("user_signature must be a string.")
        body = {"userSignature": user_signature}
        url = f"/v1/user/devices/{user_device_id}/aftermarket/commands/unpair"
        return self._request(
            "POST",
            "Devices",
            url,
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def lock_doors(self, privilege_token: str, token_id: str):
        if not isinstance(privilege_token, str):
            raise TypeError("privilege_token must be a string.")
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/vehicle/{token_id}/commands/doors/lock"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(privilege_token)
        )

    def unlock_doors(self, privilege_token: str, token_id: str):
        if not isinstance(privilege_token, str):
            raise TypeError("privilege_token must be a string.")
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/vehicle/{token_id}/commands/doors/unlock"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(privilege_token)
        )

    def open_frunk(self, privilege_token: str, token_id: str):
        if not isinstance(privilege_token, str):
            raise TypeError("privilege_token must be a string.")
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/vehicle/{token_id}/commands/frunk/open"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(privilege_token)
        )

    def open_trunk(self, privilege_token: str, token_id: str):
        if not isinstance(privilege_token, str):
            raise TypeError("privilege_token must be a string.")
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/vehicle/{token_id}/commands/trunk/open"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(privilege_token)
        )

    def list_error_codes(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/error-codes"
        return self._request(
            "GET", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def submit_error_codes(
        self, access_token: str, user_device_id: str, query_device_error_codes: dict
    ):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        if not isinstance(query_device_error_codes, dict):
            raise TypeError("query_devce_error_codes must be a dict.")
        body = {"queryDeviceErrorCodes": query_device_error_codes}
        url = f"/v1/user/devices/{user_device_id}/error-codes"
        return self._request(
            "POST",
            "Devices",
            url,
            headers=self._get_auth_headers(access_token),
            data=body,
        )

    def clear_error_codes(self, access_token: str, user_device_id: str):
        if not isinstance(access_token, str):
            raise TypeError("access_token must be a string.")
        if not isinstance(user_device_id, str):
            raise TypeError("user_device_id must be a string.")
        url = f"/v1/user/devices/{user_device_id}/error-codes/clear"
        return self._request(
            "POST", "Devices", url, headers=self._get_auth_headers(access_token)
        )

    def get_aftermarket_device(self, token_id: str):
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/aftermarket/device/{token_id}"
        self._request("GET", "Devices", url)

    def get_aftermarket_device_image(self, token_id: str):
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        url = f"/v1/aftermarket/device/{token_id}/image"
        self._request("GET", "Devices", url)

    def get_aftermarket_device_metadata_by_address(self, address: str):
        if not isinstance(address, str):
            raise TypeError("address must be a string.")
        url = f"/v1/aftermarket/device/by-address/{address}"
        self._request("GET", "Devices", url)
