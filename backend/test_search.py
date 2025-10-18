#!/usr/bin/env python3
"""
Test script for the updated search_service.py
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import UserPreference
from api.services.search_service import general_search


async def test_search():
    """Test the general_search function with sample data"""
    
    # Create test user preferences
    user_pref = UserPreference(
        type="sofa",
        budget_range=[200, 1000],
        essential_features=["fabric", "3-seater"],
        dimensions={
            "width": 200,
            "depth": 90,
            "height": 80
        }
    )
    
    print("🧪 Testing general_search function...")
    print(f"Searching for: {user_pref.type}")
    print(f"Budget: £{user_pref.budget_range[0]}-£{user_pref.budget_range[1]}")
    print(f"Features: {user_pref.essential_features}")
    print("-" * 50)
    
    try:
        # Test with 10 results
        results = await general_search(user_pref, num_results=10)
        
        print(f"\n✅ Search completed!")
        print(f"Found {len(results)} products")
        
        for i, product in enumerate(results, 1):
            print(f"\n{i}. {product.name}")
            print(f"   Price: £{product.price}")
            print(f"   URL: {product.url}")
            if product.image_url:
                print(f"   Image: {product.image_url}")
            if product.description:
                print(f"   Description: {product.description}")
                
    except Exception as e:
        print(f"❌ Error during search: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_search())
