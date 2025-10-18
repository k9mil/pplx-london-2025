"""
Search endpoints for furniture research
"""

from fastapi import APIRouter, HTTPException
from typing import List

from api.models import (
    UserPreference,
    ProductResult,
    NarrowSearchRequest,
    RefinedProduct,
)
from api.services.search_service import general_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/general", response_model=List[ProductResult])
async def perform_general_search(user_pref: UserPreference, num_results: int = 10):
    """
    Perform a general furniture search based on user preferences.

    Args:
        user_pref: User preferences including type, budget, dimensions, features
        num_results: Number of results to return (default: 10)

    Returns:
        List of product results matching the criteria
    """
    try:
        results = await general_search(user_pref, num_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/narrow", response_model=List[RefinedProduct])
async def perform_narrow_search(request: NarrowSearchRequest):
    """
    Perform a refined furniture search based on user preferences and product ratings.
    Learns style preferences from rated products to find better matches.

    Args:
        request: Contains user preferences and product ratings

    Returns:
        List of exactly 3 refined product recommendations
    """
    try:
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narrow search failed: {str(e)}")


@router.post("/debug/full-response")
async def debug_full_response(user_pref: UserPreference):
    """
    Debug endpoint to see raw Perplexity API response without any parsing.
    Shows the complete response structure including all metadata.

    Args:
        user_pref: User preferences for furniture search

    Returns:
        Raw response from Perplexity API with all available fields
    """
    try:
        return {"message": "Not implemented yet"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Full response request failed: {str(e)}"
        )
