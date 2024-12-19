"""FlowpayUniversal tap class."""
from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_flowpay_universal.streams import OrdersStream

STREAM_TYPES = [OrdersStream]


class TapFlowpayUniversal(Tap):
    """FlowpayUniversal tap class."""

    name = "tap-flowpay-universal"
    
    def __init__(
        self,
        config=None,
        catalog=None,
        state=None,
        parse_env_config=False,
        validate_config=True,
    ) -> None:
        self.config_file = config[0]
        super().__init__(config, catalog, state, parse_env_config, validate_config)

    config_jsonschema = th.PropertiesList(
        th.Property("url", th.StringType, required=True, 
                   description="URL of the data source"),
        th.Property("auth_type", th.StringType, required=True,
                   description="Authentication type: API_KEY or JWT"),
        th.Property("api_key", th.StringType, required=False,
                   description="API key for API_KEY authentication"),
        th.Property("client_id", th.StringType, required=False,
                   description="Client ID for JWT authentication"),
        th.Property("client_secret", th.StringType, required=False,
                   description="Client secret for JWT authentication"),
        th.Property("audience", th.StringType, required=False,
                   description="Audience for JWT authentication"),
        th.Property("token_endpoint_url", th.StringType, required=False,
                   description="Authorization server token endpoint URL for JWT authentication"),
        th.Property("merchant_id", th.StringType, required=True,
                   description="Merchant ID to specify when querying the data source"),
        th.Property("tenant_id", th.StringType, required=False,
                   description="Optional tenant ID to specify a customer's operation"),
        th.Property("start_date", th.DateTimeType, required=True,
                   description="Start date for data extraction"),
    ).to_dict()

    def discover_streams(self):
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapFlowpayUniversal.cli()
