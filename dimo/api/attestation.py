from dimo.errors import check_type


class Attestation:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def create_vin_vc(self, privilege_token: str, token_id: str):
        check_type("privilege_token", privilege_token, str)
        check_type("token_id", token_id, str)
        url = f"/v1/vc/vin/{token_id}"
        return self._request(
            "POST", "Attestation", url, headers=self._get_auth_headers(privilege_token)
        )

    def create_pom_vs(self, privilege_token: str, token_id: str):
        check_type("privilege_token", privilege_token, str)
        check_type("token_id", token_id, str)
        url = f"/v1/vc/pom/{token_id}"
        return self._request(
            "POST", "Attestation", url, headers=self._get_auth_headers(privilege_token)
        )
