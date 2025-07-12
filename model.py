from typing import TypedDict, Literal
from pydantic import BaseModel

class PortfolioState(TypedDict):
    """
    Represents the state of a portfolio in a trading system.
    """
    usd_amount: float
    user_input: str
    total_usd: float
    target_currency: Literal["INR", "EUR", "GBP", "AUD", "CAD", "JPY", "CNY", "NZD"]
    total_amount: float


class PortfolioRequest(BaseModel):
    """Request model for portfolio operations."""
    usd_amount: float
    user_input: str


class PortfolioResponse(BaseModel):
    """Response model for portfolio operations."""
    usd_amount: float
    total_usd: float
    target_currency: str
    total_amount: float
