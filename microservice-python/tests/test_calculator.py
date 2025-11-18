"""
Unit tests for invoice calculator service and API endpoints.
Tests calculation functionality, authentication, and edge cases.
"""
import os
import pytest
from fastapi.testclient import TestClient
from application.services import InvoiceCalculatorService
from domain.model import Item

# Set test token BEFORE importing app modules
os.environ["TOKEN_SECRET"] = "test-secret-token"

# Import app after setting environment variable
# auth.py now reads TOKEN_SECRET dynamically, so this will work
from main import app

# Create test client
client = TestClient(app)


# Service layer tests
class TestInvoiceCalculatorService:
    """Tests for InvoiceCalculatorService business logic."""

    def test_calculator_basic(self):
        """
        Test basic invoice calculation.
        Verifies subtotal, taxes, and total are calculated correctly.
        """
        # Test data: 2 items with different prices and quantities
        items = [
            Item(product="A", unit_price=100, quantity=2),  # 200
            Item(product="B", unit_price=50, quantity=1),   # 50
        ]
        result = InvoiceCalculatorService.calculate(items)

        # Verify calculations
        assert result.subtotal == 250  # 200 + 50
        assert result.taxes == 47.5  # 250 * 0.19 (19% VAT)
        assert result.discounts == 0.0  # No discount (subtotal < 1000)
        assert result.total == 297.5  # 250 + 47.5 - 0

    def test_calculator_with_discount(self):
        """
        Test invoice calculation with discount applied.
        Discount should be 5% when subtotal > 1000.
        """
        items = [
            Item(product="A", unit_price=500, quantity=3),  # 1500
        ]
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 1500
        assert result.taxes == 285.0  # 1500 * 0.19
        assert result.discounts == 75.0  # 1500 * 0.05 (5% discount)
        assert result.total == 1710.0  # 1500 + 285 - 75

    def test_calculator_single_item(self):
        """Test calculation with a single item."""
        items = [
            Item(product="Single", unit_price=100, quantity=1),
        ]
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 100
        assert result.taxes == 19.0
        assert result.total == 119.0

    def test_calculator_zero_quantity(self):
        """Test calculation with zero quantity item."""
        items = [
            Item(product="A", unit_price=100, quantity=0),
        ]
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 0
        assert result.taxes == 0
        assert result.discounts == 0
        assert result.total == 0

    def test_calculator_empty_list(self):
        """Test calculation with empty items list."""
        items = []
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 0
        assert result.taxes == 0
        assert result.discounts == 0
        assert result.total == 0

    def test_calculator_discount_threshold(self):
        """
        Test discount threshold at exactly 1000.
        Discount should not apply at 1000, only above.
        """
        items = [
            Item(product="A", unit_price=1000, quantity=1),  # Exactly 1000
        ]
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 1000
        assert result.discounts == 0.0  # No discount at threshold
        assert result.total == 1190.0  # 1000 + 190

    def test_calculator_discount_above_threshold(self):
        """Test discount applies when subtotal is above 1000."""
        items = [
            Item(product="A", unit_price=1000.01, quantity=1),  # Just above 1000
        ]
        result = InvoiceCalculatorService.calculate(items)

        assert result.subtotal == 1000.01
        assert result.discounts > 0  # Discount should apply
        assert result.total > 0


# API endpoint tests
class TestInvoiceAPI:
    """Tests for API endpoints including authentication."""

    def test_calculate_endpoint_success(self):
        """
        Test successful invoice calculation via API.
        Verifies endpoint returns correct calculation with valid token.
        """
        headers = {"X-API-Token": "test-secret-token"}
        payload = [
            {"product": "A", "unit_price": 100, "quantity": 2},
            {"product": "B", "unit_price": 50, "quantity": 1},
        ]
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["subtotal"] == 250
        assert data["taxes"] == 47.5
        assert data["discounts"] == 0.0
        assert data["total"] == 297.5

    def test_calculate_endpoint_missing_token(self):
        """
        Test API endpoint without authentication token.
        Should return 401 Unauthorized.
        """
        payload = [
            {"product": "A", "unit_price": 100, "quantity": 2},
        ]
        response = client.post("/calculate", json=payload)

        assert response.status_code == 401
        assert "Token missing" in response.json()["detail"]

    def test_calculate_endpoint_invalid_token(self):
        """
        Test API endpoint with invalid authentication token.
        Should return 401 Unauthorized.
        """
        headers = {"X-API-Token": "invalid-token"}
        payload = [
            {"product": "A", "unit_price": 100, "quantity": 2},
        ]
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]

    def test_calculate_endpoint_with_discount(self):
        """
        Test API endpoint with items that trigger discount.
        Verifies discount calculation through API.
        """
        headers = {"X-API-Token": "test-secret-token"}
        payload = [
            {"product": "A", "unit_price": 500, "quantity": 3},
        ]
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["subtotal"] == 1500
        assert data["discounts"] == 75.0
        assert data["total"] == 1710.0

    def test_calculate_endpoint_empty_items(self):
        """
        Test API endpoint with empty items list.
        Should return valid response with zero amounts.
        """
        headers = {"X-API-Token": "test-secret-token"}
        payload = []
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["subtotal"] == 0
        assert data["taxes"] == 0
        assert data["discounts"] == 0
        assert data["total"] == 0

    def test_calculate_endpoint_invalid_payload(self):
        """
        Test API endpoint with invalid payload structure.
        Should return 422 validation error.
        """
        headers = {"X-API-Token": "test-secret-token"}
        payload = {"invalid": "data"}
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 422  # Validation error

    def test_calculate_endpoint_missing_fields(self):
        """
        Test API endpoint with missing required fields.
        Should return 422 validation error.
        """
        headers = {"X-API-Token": "test-secret-token"}
        payload = [
            {"product": "A"}  # Missing unit_price and quantity
        ]
        response = client.post("/calculate", json=payload, headers=headers)

        assert response.status_code == 422  # Validation error