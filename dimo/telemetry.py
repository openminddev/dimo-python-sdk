class Telemetry:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance
    
    # Primary query method
    async def query(self, query, token):
        return await self.dimo.query('Telemetry', query, token=token)
    
    async def custom_query(self, query, token):
        pass
    
    # Sample query - get signals latest
    async def get_signals_latest(self, token, token_id):
        query = """
        query GetSignalsLatest($tokenId: Int!) {
            signalsLatest(tokenId: $tokenId){
                powertrainTransmissionTravelledDistance{
                    timestamp
                    value
                }
                exteriorAirTemperature{
                    timestamp
                    value
                }
                speed {
                    timestamp
                    value
                }
                powertrainType{
                    timestamp
                    value
                }
            }
        }
        """
        variables = {
            "tokenId": token_id
        }

        return await self.dimo.query('Telemetry', query, token=token, variables=variables)

