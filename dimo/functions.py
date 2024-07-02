from web3 import Web3
from dimo import DIMO
from environments import dimo_environment
from constants import dimo_constants
import asyncio


# SIGN CHALLENGE

# def sign_challenge(object, env="Dev"):
#     web3 = Web3(Web3.HTTPProvider(dimo_constants[env]['RPC_provder']))
#     message = object.message
#     private_key = object.private_key
#     signed_message = web3.eth.account.sign_message(message, private_key=private_key)

#     return signed_message.signature.hex()



#GET_TOKEN

async def get_token(object, env="Dev"):
    sdk = DIMO(env)

    challenge = await sdk.generate_challenge(
        client_id = 'client_id',
        domain = 'domain',
        scope = 'scope',
        response_type = 'response_type',
        address = 'client_id'

    )

    sign = await sdk.sign_challenge(
        message = challenge.challenge,
        private_key= object['private_key']
    )

    submit = await sdk.submit_challenge(
        client_id = object['client_id'],
        domain = object['domain'],
        state = challenge.state,
        signature = sign
    )

    return submit
