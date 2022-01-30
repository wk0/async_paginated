import aiohttp

class AsyncAPIClient:
    def __init__(self, logger=None):
        self._url = "https://example.com/api"
        self._client = aiohttp.ClientSession()  # trust_env=True)

        # Auth token management
        self.access_token: str = None
        self.refresh_token: str = None
        self.token_created: int = None
        self.expires: int = None

    def close(self):
        self._client.close()

    def get_initial_auth_token(self) -> None:
        # request.post(....)
        self.access_token = "sample"

    def _refresh_if_needed(self) -> None:
        # TODO: Customize for auth scheme if access token expires
        pass

    def _header(self) -> dict:
        # TODO: Customize for auth scheme
        bearer = "Bearer " + self.access_token
        return {"Accept": "application/json", "Authorization": bearer}

    async def _get(self, endpoint) -> dict:
        self._refresh_if_needed()  # refreshes access token if expired
        async with self._client.get(endpoint, headers=self._header()) as req:

            # TODO: handle errors
            # status_code = req.status
            # if status_code > 299:

            return await req.json()

    async def endpoint(self, item_id: str):
        endpoint = f"{self._url}/item/{item_id}"
        data = await self._get(endpoint=endpoint)
        return data

    async def paginated_endpoint(
        self,
        item_id: str,
        page: int = None,
    ):
        endpoint = f"{self._url}/paginated/{item_id}"

        # TODO: adjust to pagination style if not queryargs
        if page:
            endpoint = endpoint + "&page=" + str(page)

        data = await self._get(endpoint=endpoint)
        return data
