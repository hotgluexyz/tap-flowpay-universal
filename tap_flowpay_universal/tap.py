"""FlowpayUniversal tap class."""
from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_flowpay_universal.streams import OrdersStream

STREAM_TYPES = [OrdersStream]


class TapFlowpayUniversal(Tap):
    """FlowpayUniversal tap class."""

    name = "tap-flowpay-universal"

    config_jsonschema = th.PropertiesList(
        th.Property("access_token", th.StringType, required=False),
        th.Property("refresh_token", th.StringType, required=False),
        th.Property("client_id", th.StringType, required=False),
        th.Property("client_secret", th.StringType, required=False),
        th.Property("audience", th.StringType, required=False),
        th.Property("expires_in", th.IntegerType, required=False),
        th.Property("redirect_uri", th.StringType, required=False),
        th.Property("token_url", th.StringType, required=False),
        th.Property("start_date", th.DateTimeType, required=True),
        th.Property("merchantId", th.StringType, required=True),
        th.Property("tenantId", th.StringType, required=False),
        th.Property("url", th.StringType, required=True),
        th.Property("api_key", th.StringType, required=False),
        th.Property("api_key_header_name", th.StringType, required=False),
        th.Property("auth_type", th.StringType, required=False),
    ).to_dict()

    def discover_streams(self):
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapFlowpayUniversal.cli()
