import json
from http import client

from uberserver_src.errors.gps_server_client_errors import (
    UberServerVIPNotFound,
    UberServerUnexpectedStatus,
    UberServerTimeOut,
)
from uberserver_src.models.models import VIPGPSCoordsResponse


class GPSServerClient:
    def __init__(self):
        self.address = "localhost"
        self.timeout_sec = 4.5

    def _get(self, url):
        connection = client.HTTPConnection(self.address, 8088, timeout=self.timeout_sec)
        try:
            connection.request("GET", url, headers={"Host": self.address})
            response = connection.getresponse()
        except TimeoutError:
            raise UberServerTimeOut()
        if response.status == 200:
            response_data = json.loads(response.read().decode("utf-8"))
            return response_data
        if response.status == 404:
            raise UberServerVIPNotFound()
        else:
            raise UberServerUnexpectedStatus(f"Unexpected status code {response.status}.")

    def vip_position(self, point_in_time: int) -> VIPGPSCoordsResponse:
        response = self._get(f"/v1/coords/{point_in_time}")
        return VIPGPSCoordsResponse.parse_obj(response)
