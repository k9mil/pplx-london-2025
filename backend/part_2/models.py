from pydantic import BaseModel, Field
from typing import Optional, List


class UserPreference(BaseModel):
    """
    Model for storing user preferences for furniture buying research.
    """

    type: str = Field(..., description="Type of furniture (e.g., sofa, chair, table)")
    budget_range: tuple[float, float] = Field(
        ..., description="Budget range as (min, max) in currency units"
    )
    dimensions: Optional[dict[str, float]] = Field(
        default=None,
        description="Dimensions requirements (e.g., {'width': 200, 'depth': 90, 'height': 85})",
    )
    essential_features: List[str] = Field(
        default_factory=list, description="List of essential features required"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "type": "sofa",
                "budget_range": (500.0, 1500.0),
                "essential_features": [],
            }
        }


class ProductResult(BaseModel):
    """
    Model for a product result from search.
    """

    name: str = Field(..., description="Product name")
    url: str = Field(..., description="Product URL")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Brief product description")
    image_url: Optional[str] = Field(None, description="Product image URL")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Modern Sectional Sofa",
                "url": "https://example.com/sofa",
                "price": 1299.99,
                "description": "Contemporary gray sectional with reclining seats",
                "image_url": "https://example.com/images/sofa.jpg",
            }
        }


class ProductRating(BaseModel):
    """
    Model for user rating of a product.
    """

    url: str = Field(..., description="Product URL")
    score: int = Field(..., ge=1, le=10, description="User rating from 1-10")

    class Config:
        json_schema_extra = {"example": {"url": "https://example.com/sofa", "score": 8}}


class NarrowSearchRequest(BaseModel):
    """
    Request model for narrow/refined search.
    """

    user_preference: UserPreference
    product_ratings: List[ProductRating] = Field(
        ..., min_length=1, description="List of rated products from general search"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_preference": {
                    "type": "sofa",
                    "budget_range": (500.0, 1500.0),
                    "essential_features": ["reclining", "leather"],
                },
                "product_ratings": [
                    {"url": "https://example.com/sofa1", "score": 9},
                    {"url": "https://example.com/sofa2", "score": 7},
                    {"url": "https://example.com/sofa3", "score": 4},
                ],
            }
        }


class RefinedProduct(BaseModel):
    """
    Model for a refined product recommendation with style analysis.
    """

    name: str = Field(..., description="Product name")
    url: str = Field(..., description="Product URL")
    price: float = Field(..., description="Product price")
    image_url: Optional[str] = Field(None, description="Product image URL")
    functional_match: str = Field(
        ..., description="Why it matches functional requirements"
    )
    style_match: str = Field(
        ..., description="Why it matches inferred style preferences"
    )
    visual_characteristics: dict = Field(
        ..., description="Visual characteristics for image generation"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Luxe Leather Reclining Sectional",
                "url": "https://example.com/refined-sofa",
                "price": 1450.00,
                "image_url": "https://example.com/images/refined-sofa.jpg",
                "functional_match": "Has reclining feature, leather material, within budget",
                "style_match": "Modern minimalist design matching highly-rated products, clean lines, neutral color palette",
                "visual_characteristics": {
                    "color": "charcoal gray",
                    "material": "top-grain leather",
                    "style": "modern minimalist",
                },
            }
        }
