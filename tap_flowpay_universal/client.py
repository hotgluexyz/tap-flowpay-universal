"""REST client handling, including FlowpayUniversalStream base class."""

from functools import lru_cache

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

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("url")

    @property
    @lru_cache(maxsize=None)
    def authenticator(self):
        if self._tap.config.get("auth_type") == "JWT":
            return OAuth2Authenticator(
                self, self._tap.config_file, self._tap.config.get("token_url")
            )
        if self._tap.config.get("auth_type") == "API_KEY":
            return ApiKeyAuthenticator(self, self._tap.config.get("api_key"), self._tap.config.get("api_key_header_name"))
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
        if not self._tap.config.get("merchantId"):
            raise MissingConfig("The request requires 'merchantId' in config file.")
        params["merchantId"] = self._config.get("merchantId")

        if self._config.get("tenantId"):
            params["tenantId"] = self._config.get("tenantId")

        if next_page_token:
            params["page"] = next_page_token
        
        if self.size:
            params["size"] = self.size
        return params
    
    