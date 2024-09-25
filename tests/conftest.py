import pytest

# Helper function for common values
def common_config():
    return {
        "merchantId": "test_merchant",
        "url": "https://test.flowpay.com"
    }

@pytest.fixture
def flowpay_config(request):
    """
    Fixture that provides a valid config for Flowpay.
    Pass 'auth_type' argument (either 'API_KEY' or 'JWT') to switch between the two configurations.
    """
    config = common_config()

    # Determine auth type based on the test request parameter or default to API_KEY
    auth_type = getattr(request, 'param', 'API_KEY')

    if auth_type == 'API_KEY':
        config.update({
            "auth_type": "API_KEY",
            "api_key": "token",
            "api_key_header_name": "Token",
        })
    elif auth_type == 'JWT':
        config.update({
            "auth_type": "JWT",
            "token_url": "https://auth.flowpay-universal.com/oauth/token",
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "https://example.com/oauth/callback",
        })
    else:
        raise ValueError(f"Unknown auth_type: {auth_type}")

    return config

@pytest.fixture
def orders_response():
    """Fixture to simulate a valid orders response from the Flowpay API."""
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