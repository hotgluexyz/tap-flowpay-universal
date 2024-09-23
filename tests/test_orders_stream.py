from unittest.mock import patch
from tap_flowpay_universal.tap import TapFlowpayUniversal
from tap_flowpay_universal.streams import OrdersStream

# Test if the stream fetches the correct records
def test_orders_stream_parsing(orders_response, api_key_config):
    """Test the orders stream data parsing."""
    # Mock the API call
    with patch("singer_sdk.streams.RESTStream._request") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = orders_response

        # Create the stream instance
        stream = OrdersStream(tap=TapFlowpayUniversal(config=api_key_config))
        
        # Get records from the stream (usually an iterator)
        records = list(stream.get_records(None))

        # Check if the records match the expected result
        assert len(records) == 1
        record = records[0]
        assert record["id"] == "Bj60hk9kkPVAH9QBXr2a"
        assert record["totalPrice"] == 59.99
        assert record["billingAddress"]["city"] == "Praha 6"
        assert list(record.keys()) == ["id","createdAt","updatedAt","status","delivery","payment","customerId","customerName","currency","totalPrice","totalDiscount","totalShipping","totalTax", "items", "billingAddress", "shippingAddress"]
        assert list(record["items"][0].keys()) == ["productId","productName","quantity","unitPrice","totalPrice","discountAmount","taxAmount"]
        assert list(record["billingAddress"].keys()) == ["line1","city","country","zip"]
        assert list(record["billingAddress"].keys()) == ["line1","city","country","zip"]