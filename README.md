# DIMO Python Developer SDK

## Installation

You can install the SDK using `pip`

```bash
pip install dimo-python-sdk
```

## Unit Testing

Coming Soon

## API Documentation

Please visit the DIMO [Developer Documentation](https://docs.dimo.zone/developer-platform) to learn more about building on DIMO and detailed information on the API.

## How to Use the SDK

Importing the SDK:

```python
from dimo import DIMO
```

Initiate the SDK depending on the envionrment of your interest, we currently support both `Production` and `Dev` environments:

```python
dimo = DIMO("Production")
```

or

```python
dimo = DIMO("Dev")
```

### Developer License

As part of the authentication process, you will need to register a set of `client_id` and `redirect_uri` (aka `domain`) on the DIMO Network. The [DIMO Developer License](https://docs.dimo.zone/developer-platform/getting-started/developer-license) is our approach and design to a more secured, decentralized access control. As a developer, you will need to perform the following steps:

1. [Approving the Dev License to use of $DIMO](https://docs.dimo.zone/developer-platform/getting-started/developer-license/licensing-process#step-1-approving-the-dev-license-to-use-of-usddimo)
2. [Issue the Dev License](https://docs.dimo.zone/developer-platform/getting-started/developer-license/licensing-process#step-2-issue-the-dev-license) (Get a `client_id` assigned to you)
3. [Configuring the Dev License](https://docs.dimo.zone/developer-platform/getting-started/developer-license/licensing-process#step-3-configuring-the-dev-license) (Set `redirect_uri` aka `domain`)
4. [Enable Signer(s)](https://docs.dimo.zone/developer-platform/getting-started/developer-license/licensing-process#step-4-enable-signer-s), the `private_key` of this signer will be required for API access

### DIMO Streams

Coming Soon

### Authentication

In order to authenticate and access private API data, you will need to [authenticate with the DIMO Auth Server](https://docs.dimo.zone/developer-platform/getting-started/authentication). The SDK provides you with all the steps needed in the [Wallet-based Authentication Flow](https://docs.dimo.zone/developer-platform/getting-started/authentication/wallet-based-authentication-flow) in case you need it to build a wallet integration around it. We also offer expedited functions to streamline the multiple calls needed.

#### Prerequisites for Authentication

1. A valid Developer License.
2. Access to a signer wallet and its private keys. Best practice is to rotate this frequently for security purposes.

> At its core, a Web3 wallet is a software program that stores private keys, which are necessary for accessing blockchain networks and conducting transactions. Unlike traditional wallets, which store physical currency, Web3 wallets store digital assets such as Bitcoin, Ethereum, and NFTs.

NOTE: The signer wallet here is recommended to be different from the spender or holder wallet for your [DIMO Developer License](https://github.com/DIMO-Network/developer-license-donotus).

#### API Authentication

##### (Option 1) 3-Step Function Calls

The SDK offers 3 basic functions that maps to the steps listed in [Wallet-based Authentication Flow](https://docs.dimo.zone/developer-platform/getting-started/authentication/wallet-based-authentication-flow): `generate_challenge`, `sign_challenge`, and `submit_challenge`. You can use them accordingly depending on how you build your application.

```python
    challenge = await dimo.auth.generate_challenge(
        client_id: '<client_id>',
        domain: '<domain>',
        address: '<address>'
    )

    signature = await dimo.auth.sign_challenge(
        message: challenge['challenge'],
        private_key: '<private_key>'
    )

    tokens = await dimo.auth.submit_challenge(
        client_id: '<client_id>',
        domain: '<domain>',
        state: challenge['state'],
        signature: signature
    )
```

##### (Option 2) Auth Endpoint Shortcut Function

As mentioned earlier, this is the streamlined function call to directly get the `access_token`. The `address` field in challenge generation is omitted since it is essentially the `client_id` of your application per Developer License:

```python
auth_header = await dimo.auth.get_token(
    client_id: '<client_id>',
    domain: '<domain>',
    private_key: '<private_key>'
)

# Store the access_token from the auth_header dictionary
access_token = auth_header["access_token"]
```

##### (Option 3) Credentials.json File

Coming Soon

### Querying the DIMO REST API

The SDK supports async/await syntax using the [asyncio](https://docs.python.org/3/library/asyncio.html) library, and for making HTTP requests using the [requests](https://requests.readthedocs.io/en/latest/) library.

```python
async def main():
    device_makes = await dimo.device_definitions.list_device_makes()
    # Do something with the response

if __name__ == "__main__":
        asyncio.run(main())
```

#### Query Parameters

For query parameters, simply feed in an input that matches with the expected query parameters:

```python
await dimo.device_definitions.get_by_mmy(
    make="<vehicle_make>",
    model="<vehicle_model>",
    year=2024
)
```

#### Path Parameters

Path parameters work similarly - simply feed in an input, such as id.

```python
await dimo.device_definitions.get_by_id(id='26G4j1YDKZhFeCsn12MAlyU3Y2H')
```

#### Body Parameters

#### Privilege Tokens

As the 2nd leg of the API authentication, applications may exchange for short-lived privilege tokens for specific vehicles that granted privileges to the app. This uses the [DIMO Token Exchange API](https://docs.dimo.zone/developer-platform/api-references/dimo-protocol/token-exchange-api/token-exchange-api-endpoints).

For the end users of your application, they will need to share their vehicle permissions via the DIMO Mobile App or through your own implementation of privilege sharing functions - this should be built on the [`setPrivilege` function of the DIMO Vehicle Smart Contract](https://polygonscan.com/address/0xba5738a18d83d41847dffbdc6101d37c69c9b0cf#writeProxyContract).

Typically, any endpoints that uses a NFT `tokenId` in path parameters will require privilege tokens. You can get the privilege token and pipe it through to corresponding endpoints like this:

```python
privilege_token = await dimo.token_exchange.exchange(access_token, privileges=[1,3,4], token_id=<vehicle_token_id>)

await dimo.device_data.get_vehicle_status(token=privilege_token, vehicle_id=<vehicle_token_id>)
```

### Querying the DIMO GraphQL API

The SDK accepts any type of valid custom GraphQL queries, but we've also included a few sample queries to help you understand the DIMO GraphQL APIs.

#### Authentication for GraphQL API

The GraphQL entry points are designed almost identical to the REST API entry points. For any GraphQL API that requires auth headers (Telemetry API for example), you can use the same pattern as you would in the REST protected endpoints.

```python
privilege_token = await dimo.token_exchange.exchange(access_token, privileges=[1,3,4], token_id=<vehicle_token_id>)

telemetry = await dimo.telemetry.query(
    token=privilege_token,
    query=
    """
        query {
            some_valid_GraphQL_query
            }
    """
    )
```

#### Send a custom GraphQL query

```python
my_query =
"""
    {
    vehicles (first:10) {
        totalCount
        }
    }
"""

total_network_vehicles = await dimo.identity.query(query=my_query)
```

## How to Contribute to the SDK

You can read more about contributing [here](https://github.com/DIMO-Network/dimo-python-sdk/blob/dev-barrettk/CONTRIBUTING.md)
