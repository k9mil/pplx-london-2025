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
    try:
        results = await general_search(user_pref, num_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/narrow", response_model=List[RefinedProduct])
async def perform_narrow_search(request: NarrowSearchRequest):
    try:
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narrow search failed: {str(e)}")


@router.post("/debug/full-response")
async def debug_full_response(user_pref: UserPreference):
    try:
        return {"message": "Not implemented yet"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Full response request failed: {str(e)}"
        )
