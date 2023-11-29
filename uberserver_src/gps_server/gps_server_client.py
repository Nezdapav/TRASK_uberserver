from urllib.parse import urljoin
import aiohttp as aiohttp

from uberserver_src.models.models import CurrentPositionResponse


class GPSServerClient:
    def __init__(self):
        self.address = "localhost:8088/v1/"
        self.timeout = aiohttp.ClientTimeout(total=1)

    def _get(self, path: str):
        with aiohttp.ClientSession(timeout=self.timeout) as session:
            with session.get(urljoin(self.address, path)) as resp:
                if resp.status == 200:
                    print(200)
                else:
                    print(500)
                return resp.json()

    def vip_position(self, point_in_time: int) -> CurrentPositionResponse:
        response = self._get(f"coord/{point_in_time}")
        return CurrentPositionResponse.model_validate_json(response)
