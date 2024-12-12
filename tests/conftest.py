import pytest

@pytest.fixture
def api_key_config():
    """Fixture that provides a valid config."""
    return {
        "url": "https://api.flowpay-universal.com",
        "start_date": "2022-01-01T00:00:00Z",
        "merchant_id": "test_merchant",
        "url": "https://test.flowpay.com",
        "auth_type": "API_KEY",
        "api_key": "token",
    }

@pytest.fixture
def oauth_config():
    """Fixture that provides a valid config."""
    return {
        "url": "https://api.flowpay-universal.com",
        "token_url": "https://auth.flowpay-universal.com/oauth/token",
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "redirect_uri": "https://example.com/oauth/callback",
        "start_date": "2022-01-01T00:00:00Z",
        "merchant_id": "test_merchant",
        "url": "https://test.flowpay.com",
        "auth_type": "JWT",
    }


@pytest.fixture
def orders_response():
    """Fixture to simulate a valid orders response from the API."""
    return {
        "data": [
            {
                "id": "Bj60hk9kkPVAH9QBXr2a",
                "createdAt": "2024-01-21T19:19:19Z",
                "updatedAt": "2024-01-21T19:19:19Z",
                "status": "DELIVERED",
                "delivery": "CARRIER",
                "payment": "CASH",
                "customerId": "Bj60hk9kkPVAH9QBXr2a",
                "customerName": "Customer Name",
                "currency": "USD",
                "totalPrice": 59.99,
                "totalDiscount": 10,
                "totalShipping": 10,
                "totalTax": 10,
                "items": [
                    {
                        "productId": "Bj60hk9kkPVAH9QBXr2a",
                        "productName": "Product Title",
                        "quantity": 1,
                        "unitPrice": 49.99,
                        "totalPrice": 49.99,
                        "discountAmount": 10,
                        "taxAmount": 10
                    }
                ],
                "billingAddress": {
                    "line1": "Rooseveltova 613/38",
                    "city": "Praha 6",
                    "country": "CZ",
                    "zip": "16000"
                },
                "shippingAddress": {
                    "line1": "Rooseveltova 613/38",
                    "city": "Praha 6",
                    "country": "CZ",
                    "zip": "16000"
                }
            }
        ]
    }

