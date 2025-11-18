"""
Business rules for invoice calculations.
Contains domain logic for subtotal, taxes, and discounts.
"""
def calculate_subtotal(items):
    """
    Calculate subtotal by summing all item prices.
    
    Args:
        items: List of Item objects
        
    Returns:
        Total of (unit_price * quantity) for all items
    """
    return sum(item.unit_price * item.quantity for item in items)

def calculate_taxes(subtotal: float) -> float:
    """
    Calculate tax amount based on subtotal.
    Currently applies 19% IVA (VAT).
    
    Args:
        subtotal: Base amount before taxes
        
    Returns:
        Tax amount (subtotal * tax_rate)
    """
    VAT = 0.19  # 19% VAT rate
    return subtotal * VAT

def calculate_discounts(subtotal: float) -> float:
    """
    Calculate discount amount based on business rules.
    Current rule: 5% discount if subtotal > 1000.
    
    Args:
        subtotal: Base amount before discounts
        
    Returns:
        Discount amount (0 if no discount applies)
    """
    # Business rule: 5% discount for orders over 1000
    return subtotal * 0.05 if subtotal > 1000 else 0.0
