import os
from pathlib import Path
from dotenv import load_dotenv
from perplexity import Perplexity
from typing import Dict, Any
from .models import UserPreference

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables")


def get_full_response(user_pref: UserPreference) -> Dict[str, Any]:
    """
    Get full raw Perplexity API response without parsing.

    Args:
        user_pref: UserPreference object containing search criteria

    Returns:
        Dictionary with raw response data and metadata
    """
    client = Perplexity(api_key=api_key)

    # Build simple search query
    dimensions_str = ", ".join([f"{k}: {v} inches" for k, v in user_pref.dimensions.items()])
    features_str = ", ".join(user_pref.essential_features) if user_pref.essential_features else "none specified"

    prompt = f"""
Find 3 {user_pref.type} options that meet these requirements:
- Budget: ${user_pref.budget_range[0]} - ${user_pref.budget_range[1]}
- Dimensions: {dimensions_str}
- Features: {features_str}

For each product, provide:
1. Product name
2. URL
3. Price
4. Brief description

"""

    # Make the API call
    completion = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system",
                "content": "You are a furniture shopping assistant. Always provide direct product URLs, not just retailer homepages."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        extra_body={
            "return_images": True,
        },
        search_recency_filter="month"
    )

    print(completion)

    # Extract all available data from the response
    response_data = {
        "message_content": completion.choices[0].message.content,
        "model": completion.model,
        "finish_reason": completion.choices[0].finish_reason,
    }

    print(response_data["message_content"])
    # Check for images attribute
    message = completion.choices[0].message
    if hasattr(message, 'images'):
        response_data["images"] = message.images
    else:
        response_data["images"] = None

    # Check for citations
    if hasattr(completion, 'citations'):
        response_data["citations"] = completion.citations
    else:
        response_data["citations"] = None

    # Check for other metadata
    if hasattr(completion.choices[0], 'metadata'):
        response_data["metadata"] = completion.choices[0].metadata
    else:
        response_data["metadata"] = None

    # Try to get all attributes from the completion object
    response_data["completion_attributes"] = dir(completion)
    response_data["message_attributes"] = dir(message)
    response_data["choice_attributes"] = dir(completion.choices[0])

    # Convert to dict if possible
    if hasattr(completion, 'model_dump'):
        response_data["full_completion_dict"] = completion.model_dump()
    elif hasattr(completion, 'dict'):
        response_data["full_completion_dict"] = completion.dict()
    else:
        response_data["full_completion_str"] = str(completion)

    return response_data
