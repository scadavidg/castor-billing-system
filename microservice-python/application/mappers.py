"""
Mappers for converting domain calculations to response DTOs.
"""
from domain.model import InvoiceCalculationResult

def map_to_result(subtotal, taxes, discounts):
    """
    Map calculation results to InvoiceCalculationResult DTO.
    
    Formula: total = subtotal + taxes - discounts
    
    Args:
        subtotal: Base amount before taxes and discounts
        taxes: Tax amount to add
        discounts: Discount amount to subtract
        
    Returns:
        InvoiceCalculationResult DTO
    """
    # Calculate final total: subtotal + taxes - discounts
    total = subtotal + taxes - discounts
    return InvoiceCalculationResult(
        subtotal=subtotal,
        taxes=taxes,
        discounts=discounts,
        total=total
    )
