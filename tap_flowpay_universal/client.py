"""REST client handling, including FlowpayUniversalStream base class."""

from functools import lru_cache
from urllib.parse import urlparse

from singer_sdk.streams import RESTStream

from tap_flowpay_universal.auth import OAuth2Authenticator, ApiKeyAuthenticator


class MissingConfig(Exception):
    pass


class FlowpayUniversalStream(RESTStream):
    """FlowpayUniversal stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105
    
    size = 100


    def __init__(self, *args, **kwargs):
        """Initialize the FlowpayUniversal stream.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Raises:
            MissingConfig: If the URL is not provided in the config.
        """
        super().__init__(*args, **kwargs)
        
        url = self.config.get("url")
        if not url:
            raise MissingConfig("The 'url' parameter is required in config file.")
            
        parsed_url = urlparse(url.rstrip('/'))
        
        # Extract the last path component as orders_path
        path_components = [p for p in parsed_url.path.split('/') if p]
        orders_path = f"/{path_components[-1]}" if path_components else ""
        
        # Construct base URL by removing orders_path
        base_path = '/'.join(path_components[:-1]) if path_components else ''
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if base_path:
            base_url = f"{base_url}/{base_path}"
                
        self._config["orders_path"] = orders_path
        self._base_url = base_url

    @property
    def url_base(self) -> str:
        return self._base_url

    @property
    @lru_cache(maxsize=None)
    def authenticator(self):
        if self._tap.config.get("auth_type") == "JWT":
            return OAuth2Authenticator(
                self, self._tap.config_file, self._tap.config.get("token_url")
            )
        if self._tap.config.get("auth_type") == "API_KEY":
            return ApiKeyAuthenticator(self, self._tap.config.get("api_key"), "X-API-Key")
        raise MissingConfig("Auth type should be `API_KEY` or `JWT`.")

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["Content-Type"] = "application/json"
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_url_params(self, context, next_page_token):
        params: dict = {}
        if not self._tap.config.get("merchant_id"):
            raise MissingConfig("The request requires 'merchant_id' in config file.")
        params["merchantId"] = self._config.get("merchant_id")

        if self._config.get("tenant_id"):
            params["tenantId"] = self._config.get("tenant_id")

        if next_page_token:
            params["page"] = next_page_token
        
        if self.size:
            params["size"] = self.size
        return params
    
    