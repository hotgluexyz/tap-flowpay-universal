"""FlowpayUniversal Authentication."""
import json
import datetime
from typing import Optional

import requests
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
import backoff

class MissingCredentialConfigException(Exception):
    pass

JWT_AUTH = "JWT"
API_KEY_AUTH = "API_KEY"
TOKEN_EXPIRATION_THRESHOLD = 60  # in seconds

class OAuth2Authenticator(APIAuthenticatorBase):
    """API Authenticator for OAuth 2.0 flows."""

    def __init__(
        self,
        stream: RESTStreamBase,
        config_file: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
    ) -> None:
        required_fields = ["client_id", "client_secret", "redirect_uri", "refresh_token"]
        for field in required_fields:
            if stream._tap.config.get(field) is None:
                raise MissingCredentialConfigException(f"Auth type `{JWT_AUTH}` requires `{field}` in config file.")

        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._config_file = config_file
        self._tap = stream._tap

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.update_access_token()
        result = super().auth_headers
        result["Authorization"] = f"Bearer {self._tap._config.get('access_token')}"
        return result

    @property
    def auth_endpoint(self) -> str:
        """Get the authorization endpoint.

        Returns:
            The API authorization endpoint if it is set.

        Raises:
            ValueError: If the endpoint is not set.
        """
        if not self._auth_endpoint:
            raise ValueError("Authorization endpoint not set.")
        return self._auth_endpoint

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the hubspot API."""
        return {
            "client_id": self._tap._config["client_id"],
            "client_secret": self._tap._config["client_secret"],
            "redirect_uri": self._tap._config["redirect_uri"],
            "refresh_token": self._tap._config["refresh_token"],
            "grant_type": "refresh_token",
        }

    def is_token_valid(self) -> bool:
        access_token = self._tap._config.get("access_token")
        now = self.get_now_timestamp()
        expires_in = self._tap._config.get("expires_in")

        return bool(access_token and expires_in and ((expires_in - now) >= TOKEN_EXPIRATION_THRESHOLD))

    def get_now_timestamp(self):
        return round(datetime.datetime.now(datetime.timezone.utc).timestamp())

    @property
    def oauth_request_payload(self) -> dict:
        """Get request body.

        Returns:
            A plain (OAuth) or encrypted (JWT) request body.
        """
        return self.oauth_request_body

    @backoff.on_exception(backoff.expo, (RetriableAPIError, requests.exceptions.RequestException), max_tries=5)
    def request_token(self, endpoint: str, data: dict) -> requests.Response:
        """Request a new access token."""
        try:
            token_response = requests.post(endpoint, data)
            token_response.raise_for_status()
            return token_response
        except requests.exceptions.Timeout:
            raise RetriableAPIError("Timeout occurred during token request.")
        except requests.exceptions.ConnectionError:
            raise RetriableAPIError("Connection error occurred during token request.")
        except requests.exceptions.HTTPError as http_err:
            if 500 <= token_response.status_code < 600:
                raise RetriableAPIError(f"Auth error: {token_response.text}")
            else:
                raise FatalAPIError(f"Auth error: {http_err}")
        except Exception as ex:
            raise FatalAPIError(f"Failed token request: {ex}")

    # Authentication and refresh
    def update_access_token(self) -> None:
        """Update `access_token` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = round(self.get_now_timestamp())
        token_response = self.request_token(self.auth_endpoint, data=self.oauth_request_payload)

        try:
            # Raise an HTTPError if the response contains a non-200 status code
            token_response.raise_for_status()
            token_json = token_response.json()

            # Extract and save the new token and expiration time
            self._tap._config["access_token"] = token_json["access_token"]
            self._tap._config["expires_in"] = request_time + token_json["expires_in"]

            # Save the updated configuration back to the file
            self._save_config()
            self.logger.info("OAuth token refreshed successfully.")
        except requests.exceptions.HTTPError as http_err:
            # Handle different HTTP error responses
            raise FatalAPIError(f"HTTP error occurred during token refresh: {http_err}")
        except KeyError as key_err:
            # Handle missing keys in the token response
            raise FatalAPIError(f"Missing key in token response: {key_err}")
        except Exception as ex:
            # Catch any other exception and raise it as a FatalAPIError
            raise FatalAPIError(f"Failed to refresh access token: {ex}")

    def _save_config(self) -> None:
        """Save the updated config to the config file."""
        try:
            with open(self._tap.config_file, "w") as outfile:
                json.dump(self._tap._config, outfile, indent=4)
        except IOError as e:
            raise FatalAPIError(f"Failed to write config file: {e}")

class ApiKeyAuthenticator(APIAuthenticatorBase):
    """API Authenticator for API KEY flows."""

    def __init__(self,
        stream: RESTStreamBase,
        token: Optional[str] = None,
        header_name: Optional[str] = None
    ) -> None:
        if stream._tap.config.get("api_key") is None:
            raise MissingCredentialConfigException(f"Auth type `{API_KEY_AUTH}` requires 'api_key' in config file.")
        if stream._tap.config.get("api_key_header_name") is None:
            raise MissingCredentialConfigException(f"Auth type `{API_KEY_AUTH}` requires 'api_key_header_name' in config file.")

        super().__init__(stream)
        self.token = token or stream._tap.config["api_key"]
        self.header_name = header_name or stream._tap.config["api_key_header_name"]

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers."""
        headers = super().auth_headers
        headers[self.header_name] = self.token
        return headers