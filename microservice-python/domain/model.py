"""
Domain models for invoice calculation.
Uses Pydantic for data validation and serialization.
"""
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    """
    Represents a single line item in an invoice.
    """
    product: str  # Product name/identifier
    unit_price: float  # Unit price
    quantity: int  # Quantity

class InvoiceCalculationResult(BaseModel):
    """
    Result of invoice calculation.
    Contains all calculated amounts for the invoice.
    """
    subtotal: float  # Base amount before taxes and discounts
    taxes: float  # Tax amount (e.g., IVA)
    discounts: float  # Discount amount
    total: float  # Final total: subtotal + taxes - discounts
