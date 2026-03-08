
"""API клиент для Магазина МТС"""

import requests


class MTSApi:
    """Класс для работы с API Магазина МТС"""

    BASE_URL: str = "https://shop.mts.ru"
    API_ENDPOINT: str = "/apigw/api/v3/search/listing"

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        headers: dict | None = None
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        default_headers = {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "x-kl-ajax-request": "Ajax_Request"
        }
        if headers:
            default_headers.update(headers)

        return self.session.request(
            method=method,
            url=url,
            params=params,
            headers=default_headers
        )

    def search_products(
        self,
        query: str,
        sort: str = "ONLY_AVAILABLE",
        page: int = 1,
        limit: int = 30,
        region_id: str = "77000000000000000000000000",
        location: str = "77000000000000000000000000",
        price_min: int | None = None,
        price_max: int | None = None
    ) -> requests.Response:
        params = {
            "st": query,
            "project": "shop",
            "platform": "web",
            "strategy": "advanced_xname,zero_queries",
            "regionId": region_id,
            "showUnavailable": "true",
            "page": page,
            "limit": limit,
            "location": location,
            "sort": sort,
            "withCorrection": "true",
            "withFacets": "true",
            "treeFacets": "true",
            "bundlesInfo": "true"
        }

        if price_min is not None and price_max is not None:
            params["filter"] = f"price:{price_min};{price_max}"

        return self._make_request(
            method="GET",
            endpoint=self.API_ENDPOINT,
            params=params
        )

    def search_with_invalid_method(
        self,
        query: str,
        method: str = "DELETE"
    ) -> requests.Response:
        params = {
            "st": query,
            "project": "shop",
            "platform": "web",
            "strategy": "advanced_xname,zero_queries",
            "regionId": "77000000000000000000000000",
            "showUnavailable": "true",
            "page": 1,
            "limit": 30,
            "location": "77000000000000000000000000",
            "sort": "ONLY_AVAILABLE",
            "withCorrection": "true",
            "withFacets": "true",
            "treeFacets": "true",
            "bundlesInfo": "true"
        }

        return self._make_request(
            method=method,
            endpoint=self.API_ENDPOINT,
            params=params
        )
