from web3 import Web3
from eth_account.messages import encode_defunct
from dimo.constants import dimo_constants
from urllib.parse import urlencode
from typing import Dict, Optional


class Auth:

    def __init__(self, request_method, get_auth_headers, env):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        self.env = env

    def generate_challenge(
        self,
        client_id: str,
        domain: str,
        address: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
        scope: str = "openid email",
        response_type: str = "code",
    ) -> Dict:
        if not isinstance(client_id, str):
            raise TypeError("client_id must be a string.")
        if not isinstance(domain, str):
            raise TypeError("domain must be a string.")
        if not isinstance(address, str):
            raise TypeError("address must be a string.")
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )
        body = {
            "client_id": client_id,
            "domain": domain,
            "scope": scope,
            "response_type": response_type,
            "address": address,
        }

        return self._request(
            "POST",
            "Auth",
            "/auth/web3/generate_challenge",
            data=urlencode(body),
            headers=headers,
        )

    def sign_challenge(self, message: str, private_key: str) -> str:
        if not isinstance(message, str):
            raise TypeError("message must be a string.")
        if not isinstance(private_key, str):
            raise TypeError("private_key must be a string.")

        web3 = Web3(Web3.HTTPProvider(dimo_constants[self.env]["RPC_provider"]))
        signed_message = web3.eth.account.sign_message(
            encode_defunct(text=message), private_key=private_key
        )
        return signed_message.signature.hex()

    def submit_challenge(
        self,
        client_id: str,
        domain: str,
        state: str,
        signature: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
    ) -> Dict:
        if not isinstance(client_id, str):
            raise TypeError("client_id must be a string.")
        if not isinstance(domain, str):
            raise TypeError("domain must be a string.")
        if not isinstance(state, str):
            raise TypeError("state must be a string.")
        if not isinstance(signature, str):
            raise TypeError("signature must be a string")
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dictionary.")
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )

        form_data = {
            "client_id": client_id,
            "domain": domain,
            "state": state,
            "signature": signature,
            "grant_type": "authorization_code",
        }

        return self._request(
            "POST",
            "Auth",
            "/auth/web3/submit_challenge",
            data=form_data,
            headers=headers,
        )

    # Requires client_id, domain, and private_key. Address defaults to client_id.
    def get_token(
        self,
        client_id: str,
        domain: str,
        private_key: str,
        address: Optional[str] = None,
        scope="openid email",
        response_type="code",
    ) -> Dict:
        if not isinstance(client_id, str):
            raise TypeError("client_id must be a string.")
        if not isinstance(domain, str):
            raise TypeError("domain must be a string.")
        if not isinstance(private_key, str):
            raise TypeError("private_key must be a string.")
        if not isinstance(address, str) and address is not None:
            raise TypeError(
                "address must be a string or omitted from get_token() to automatically use client_id as address."
            )

        if address is None:
            address = client_id

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        challenge = self.generate_challenge(
            headers=headers,
            client_id=client_id,
            domain=domain,
            scope=scope,
            response_type=response_type,
            address=address,
        )

        sign = self.sign_challenge(
            message=challenge["challenge"],
            private_key=private_key,
        )

        state = challenge["state"]
        signature = sign

        submit = self.submit_challenge(client_id, domain, state, signature, headers)
        return submit
