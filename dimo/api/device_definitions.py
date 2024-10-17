class DeviceDefinitions:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_by_mmy(self, make: str, model: str, year: int) -> dict:
        if not isinstance(make, str):
            raise TypeError("make must be a string.")
        if not isinstance(model, str):
            raise TypeError("model must be a string.")
        if not isinstance(year, int):
            raise TypeError("year must be an int.")
        params = {"make": make, "model": model, "year": year}
        return self._request(
            "GET", "DeviceDefinitions", "/device-definitions", params=params
        )

    def get_by_id(self, id: str) -> dict:
        if not isinstance(id, str):
            raise TypeError("id must be a string.")
        url = f"/device-definitions/{id}"
        return self._request("GET", "DeviceDefinitions", url)

    def list_device_makes(self) -> dict:
        return self._request("GET", "DeviceDefinitions", "/device-makes")

    def get_device_type_by_id(self, id: str):
        if not isinstance(id, str):
            raise TypeError("id must be a string.")
        url = f"/device-types/{id}"
        return self._request("GET", "DeviceDefinitions", url)
