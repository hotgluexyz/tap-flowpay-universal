"""Tests standard tap features using the built-in SDK tests library."""

import datetime
from singer_sdk.testing import get_tap_test_class
from tap_flowpay_universal.tap import TapFlowpayUniversal
import pytest


@pytest.mark.parametrize('flowpay_config', ['API_KEY', 'JWT'], indirect=True)
def test_api_key_flowpay_universal(flowpay_config):
    """
    Test the tap with the API_KEY configuration.
    """
    TestTapFlowpayUniversal = get_tap_test_class(
        tap_class=TapFlowpayUniversal,
        config=flowpay_config,
    )
    # Dynamically create the class and let pytest handle discovery
    globals()['TestTapFlowpayUniversal'] = TestTapFlowpayUniversal