from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from part_2.models import (
    UserPreference,
    ProductResult,
    NarrowSearchRequest,
    RefinedProduct,
)
from part_2.general_search import general_search
from part_2.narrow_search import narrow_search
from part_2.full_response import get_full_response

app = FastAPI(
    title="Furniture Research API",
    description="API for furniture buying research with AI-powered recommendations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Furniture Research API",
        "endpoints": {
            "general_search": "/search/general",
            "narrow_search": "/search/narrow",
        },
    }


@app.post("/search/general", response_model=List[ProductResult])
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


@app.post("/search/narrow", response_model=List[RefinedProduct])
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
        results = narrow_search(request.user_preference, request.product_ratings)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narrow search failed: {str(e)}")


@app.post("/debug/full-response")
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
        response = get_full_response(user_pref)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Full response request failed: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
