"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_flowpay_universal.tap import TapFlowpayUniversal

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "merchantId": "test_merchant",
    "url": "https://test.flowpay.com",    
}


# Run standard built-in tap tests from the SDK:
TestTapFlowpayUniversal = get_tap_test_class(
    tap_class=TapFlowpayUniversal,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
