from dimo.constants import dimo_constants


class TokenExchange:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def exchange(
        self, token: str, privileges: list, token_id: str, env="Production"
    ) -> dict:
        if not isinstance(token, str):
            raise TypeError("token must be a string.")
        if not isinstance(privileges, list):
            raise TypeError("priviliges must be provided as a list, e.g. [1, 3, 4]")
        if not isinstance(token_id, str):
            raise TypeError("token_id must be a string.")
        body = {
            "nftContractAddress": dimo_constants[env]["NFT_address"],
            "privileges": privileges,
            "tokenId": token_id,
        }
        response = self._request(
            "POST",
            "TokenExchange",
            "/v1/tokens/exchange",
            headers=self._get_auth_headers(token),
            data=body,
        )
        return response
