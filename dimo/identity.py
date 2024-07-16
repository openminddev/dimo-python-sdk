from query import query

class Identity:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance

    # Primary query method
    async def query(self, token, query):
        return await self.dimo.query('Identity', query, token=token)

    # Sample query - count DIMO vehicles
    async def count_dimo_vehicles(self, token):
        query = """
        {
            vehicles (first:10) {
                totalCount,
            }
        }
        """
        return await self.dimo.query('Identity', query, token=token)
