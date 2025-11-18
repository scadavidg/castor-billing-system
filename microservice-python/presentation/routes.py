"""
API routes for invoice calculation endpoints.
Handles HTTP requests and delegates to application services.
All endpoints require authentication via X-API-Token header.
"""
from fastapi import APIRouter, Depends
from domain.model import Item, InvoiceCalculationResult
from typing import List
from application.services import InvoiceCalculatorService
from infrastructure.auth import verify_token

# API router for invoice endpoints
router = APIRouter()

@router.post("/calculate", response_model=InvoiceCalculationResult)
def calculate_invoice(
    items: List[Item],
    authorized: bool = Depends(verify_token)
):
    """
    Calculate invoice total from list of items.
    
    Requires authentication via X-API-Token header.
    
    POST /calculate
    Headers:
        X-API-Token: Valid API token (required)
    Request body: JSON array of items with product, unit_price, quantity
    
    Example request:
        Headers: { "X-API-Token": "your-secret-token" }
        Body: [
            {"product": "A", "unit_price": 100, "quantity": 2},
            {"product": "B", "unit_price": 50, "quantity": 1}
        ]
    
    Returns:
        InvoiceCalculationResult with calculated amounts (subtotal, taxes, discounts, total)
        
    Raises:
        HTTPException 401: If authentication token is missing or invalid
    """
    # Authentication is handled by verify_token dependency
    # If we reach here, token is valid
    result = InvoiceCalculatorService.calculate(items)
    return result

