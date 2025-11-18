"""
Application service layer for invoice calculations.
Orchestrates business logic from domain layer.
"""
from domain.rules import calculate_subtotal, calculate_taxes, calculate_discounts
from application.mappers import map_to_result

class InvoiceCalculatorService:
    """
    Service for calculating invoice totals.
    Coordinates domain rules and maps results to DTOs.
    """

    @staticmethod
    def calculate(items):
        """
        Calculate invoice total from list of items.
        
        Args:
            items: List of Item objects
            
        Returns:
            InvoiceCalculationResult with subtotal, taxes, discounts, and total
        """
        # Calculate base subtotal from items
        subtotal = calculate_subtotal(items)
        # Apply tax rules (e.g., VAT)
        taxes = calculate_taxes(subtotal)
        # Apply discount rules based on subtotal
        discounts = calculate_discounts(subtotal)
        # Map to response DTO
        return map_to_result(subtotal, taxes, discounts)

