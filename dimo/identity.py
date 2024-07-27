class Identity:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance

    # Primary query method
    async def query(self, query):
        return await self.dimo.query('Identity', query)

    # Sample query - count DIMO vehicles
    async def count_dimo_vehicles(self):
        query = """
        {
            vehicles (first:10) {
                totalCount,
            }
        }
        """
        return await self.dimo.query('Identity', query)

    # Sample query - list vehicle definitions per address
    async def list_vehicle_definitions_per_address(self, address, limit):
        query = """
        query ListVehicleDefinitionsPerAddress($owner: Address!, $first: Int!) {
          vehicles(filterBy: {owner: $owner}, first: $first) {
            nodes {
              aftermarketDevice {
                tokenId
                address
              } 
              syntheticDevice {
                address
                tokenId
              }
              definition {
                make
                model
                year
              }
            }
          }
        }
        """
        variables = {
            "owner": address,
            "first": limit
        }

        return await self.dimo.query('Identity', query, variables=variables)