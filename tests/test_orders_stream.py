from unittest.mock import patch
from tap_flowpay_universal.tap import TapFlowpayUniversal
from tap_flowpay_universal.streams import OrdersStream
import pytest

@pytest.mark.parametrize('flowpay_config', ['API_KEY', 'JWT'], indirect=True)
def test_orders_stream_parsing(orders_response, flowpay_config):
    """Test the orders stream data parsing with mocked API response."""
    
    # Mock the request_records method instead of _request
    with patch("singer_sdk.streams.RESTStream.request_records") as mock_request_records:
        # Mock the API response
        mock_request_records.return_value = iter(orders_response["data"])

        # Create the stream instance with the appropriate config (API_KEY or JWT)
        stream = OrdersStream(tap=TapFlowpayUniversal(config=flowpay_config))

        # Get records from the stream (usually an iterator)
        records = list(stream.get_records(None))

        # Assert that one record is returned
        assert len(records) == 1
        record = records[0]

        # Check specific fields in the record
        assert record["id"] == "Bj60hk9kkPVAH9QBXr2a"
        assert record["totalPrice"] == 59.99
        assert record["billingAddress"]["city"] == "Praha 6"
        
        # Check the structure of the keys in the record
        expected_keys = [
            "id", "createdAt", "updatedAt", "status", "delivery", "payment", 
            "customerId", "customerName", "currency", "totalPrice", "totalDiscount", 
            "totalShipping", "totalTax", "items", "billingAddress", "shippingAddress"
        ]
        assert list(record.keys()) == expected_keys

        # Check the structure of the items
        expected_item_keys = ["productId", "productName", "quantity", "unitPrice", "totalPrice", "discountAmount", "taxAmount"]
        assert list(record["items"][0].keys()) == expected_item_keys

        # Check the structure of the billingAddress
        expected_address_keys = ["line1", "city", "country", "zip"]
        assert list(record["billingAddress"].keys()) == expected_address_keys
        assert list(record["shippingAddress"].keys()) == expected_address_keys