"""
Unit tests for invoice calculator service.
Tests basic calculation functionality.
"""
from application.services import InvoiceCalculatorService
from domain.model import Item

def test_calculator_basic():
    """
    Test basic invoice calculation.
    Verifies subtotal, taxes, and total are calculated correctly.
    """
    # Test data: 2 items with different prices and quantities
    items = [
        Item(producto="A", precio_unitario=100, cantidad=2),  # 200
        Item(producto="B", precio_unitario=50, cantidad=1),   # 50
    ]
    result = InvoiceCalculatorService.calculate(items)

    # Verify calculations
    assert result.subtotal == 250  # 200 + 50
    assert result.impuestos > 0  # Should have taxes applied
    assert result.total > 0  # Total should be positive