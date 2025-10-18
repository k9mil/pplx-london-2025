from pydantic import BaseModel, Field
from typing import Optional, List


class UserPreference(BaseModel):
    type: str = Field(..., description="Type of item (e.g., sofa, chair, table)")
    budget: float = Field(..., description="Maximum budget in currency units")
    additional_requirements: str = Field(
        default="", description="Additional requirements or preferences for the item"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "type": "sofa",
                "budget": 1500.0,
                "additional_requirements": "Must be comfortable and modern style",
            }
        }


class ProductResult(BaseModel):
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
    url: str = Field(..., description="Product URL")
    score: int = Field(..., ge=1, le=10, description="User rating from 1-10")

    class Config:
        json_schema_extra = {"example": {"url": "https://example.com/sofa", "score": 8}}


class NarrowSearchRequest(BaseModel):
    user_preference: UserPreference
    product_ratings: List[ProductRating] = Field(
        ..., min_length=1, description="List of rated products from general search"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_preference": {
                    "type": "sofa",
                    "budget": 1500.0,
                    "additional_requirements": "Must be comfortable and modern style",
                },
                "product_ratings": [
                    {"url": "https://example.com/sofa1", "score": 9},
                    {"url": "https://example.com/sofa2", "score": 7},
                    {"url": "https://example.com/sofa3", "score": 4},
                ],
            }
        }


class RefinedProduct(BaseModel):
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
