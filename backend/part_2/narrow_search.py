import os
from pathlib import Path
from dotenv import load_dotenv
from perplexity import Perplexity
from typing import List
from .models import UserPreference, ProductRating, RefinedProduct

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")

if not api_key:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables")


def narrow_search(user_pref: UserPreference, product_ratings: List[ProductRating]) -> List[RefinedProduct]:
    """
    Performs a refined furniture search based on user preferences and product ratings.
    Learns style preferences from rated products to find better matches.

    Args:
        user_pref: UserPreference object containing search criteria
        product_ratings: List of ProductRating objects showing user's preferences

    Returns:
        List of exactly 3 RefinedProduct objects (top recommendations)
    """
    # Initialize the client with API key
    client = Perplexity(api_key=api_key)

    # Segment ratings into high, low, and neutral
    high_rated = [r for r in product_ratings if r.score >= 8]
    low_rated = [r for r in product_ratings if r.score <= 5]
    neutral_rated = [r for r in product_ratings if 5 < r.score < 8]

    # Build the search prompt
    dimensions_str = ", ".join([f"{k}: {v} inches" for k, v in user_pref.dimensions.items()])
    features_str = ", ".join(user_pref.essential_features) if user_pref.essential_features else "none specified"

    # Build rating sections
    high_rated_str = "\n".join([f"- {r.url} (Score: {r.score}/10)" for r in high_rated]) if high_rated else "None"
    low_rated_str = "\n".join([f"- {r.url} (Score: {r.score}/10)" for r in low_rated]) if low_rated else "None"
    neutral_rated_str = "\n".join([f"- {r.url} (Score: {r.score}/10)" for r in neutral_rated]) if neutral_rated else "None"

    prompt = f"""
I'm helping a user find the perfect {user_pref.type}. They provided basic requirements and
rated an initial set of products. I need to understand their STYLE preferences from these
ratings and find better matches.

FUNCTIONAL REQUIREMENTS (must maintain):
- Type: {user_pref.type}
- Budget: ${user_pref.budget_range[0]} - ${user_pref.budget_range[1]}
- Dimensions: {dimensions_str}
- Essential features: {features_str}

STYLE LEARNING - Products they rated:

HIGH RATED (what they LIKED):
{high_rated_str}

LOW RATED (what they DIDN'T like):
{low_rated_str}

NEUTRAL:
{neutral_rated_str}

Please:
1. Visit these URLs and analyze the visual style, materials, and design details
2. Identify patterns in what they liked vs disliked (color, style, materials, design era, brand aesthetic)
3. Create a style profile for this user
4. Search for EXACTLY 3 new {user_pref.type} options that:
   - Meet ALL the functional requirements
   - Match the inferred style preferences
   - Are NOT the products already rated
   - Are currently available for purchase

For each of the 3 recommendations, provide:
- Product name
- Direct product URL
- Price (numeric value)
- Image URL (if available)
- Why it matches functional requirements (1-2 sentences)
- Why it matches their style preferences based on the rated products (2-3 sentences)
- Visual characteristics: color, material, and design style

Format each product clearly with all fields labeled. Be highly selective - only recommend products you're confident about.
"""

    # Make the API call
    completion = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system",
                "content": "You are an expert interior designer and furniture consultant. Analyze user preferences deeply and provide highly targeted recommendations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,  # Slightly higher for creative style analysis
        extra_body={
            "return_images": True,
        },
        search_recency_filter="month"  # Current inventory only
    )

    # Get the response
    response_text = completion.choices[0].message.content

    # Extract images from the response if available
    images = []
    if hasattr(completion, 'images') and completion.images:
        # Images is a list of dicts with 'image_url' keys
        images = [img.get('image_url') for img in completion.images if img.get('image_url')]

    # Extract citations and search_results for real URLs
    citations = []
    if hasattr(completion, 'citations') and completion.citations:
        citations = completion.citations

    search_results = []
    if hasattr(completion, 'search_results') and completion.search_results:
        search_results = completion.search_results

    # Parse the response into RefinedProduct objects
    products = parse_refined_response(response_text, images, citations, search_results)

    # Ensure we return exactly 3 products
    return products[:3]


def parse_refined_response(response_text: str, images: List = None, citations: List = None, search_results: List = None) -> List[RefinedProduct]:
    """
    Parse Perplexity response into RefinedProduct objects.

    Args:
        response_text: Raw response from Perplexity API
        images: List of image URLs from the response
        citations: List of citation URLs from the response
        search_results: List of search result objects from the response

    Returns:
        List of RefinedProduct objects
    """
    # Extract real URLs from search results and citations
    real_urls = []
    if search_results:
        for result in search_results:
            if hasattr(result, 'url'):
                real_urls.append(result.url)
            elif isinstance(result, dict) and 'url' in result:
                real_urls.append(result['url'])
    if citations:
        real_urls.extend(citations)
    products = []
    lines = response_text.split('\n')
    current_product = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a new numbered item (1., 2., 3.)
        if len(line) > 0 and line[0].isdigit() and '.' in line[:3]:
            # Save previous product if complete
            if current_product and 'name' in current_product and 'url' in current_product:
                # Set defaults for missing fields
                current_product.setdefault('price', 0.0)
                current_product.setdefault('image_url', None)
                current_product.setdefault('functional_match', '')
                current_product.setdefault('style_match', '')
                current_product.setdefault('visual_characteristics', {})
                products.append(RefinedProduct(**current_product))
            current_product = {}

        # Parse fields
        lower_line = line.lower()

        if 'name:' in lower_line or 'product:' in lower_line:
            current_product['name'] = line.split(':', 1)[1].strip()
        elif 'url:' in lower_line or 'link:' in lower_line:
            url_part = line.split(':', 1)[1].strip()
            if '(' in url_part and ')' in url_part:
                url_part = url_part[url_part.index('(')+1:url_part.index(')')]
            current_product['url'] = url_part
        elif 'price:' in lower_line or '$' in line:
            price_str = line.replace('Price:', '').replace('price:', '').replace('$', '').replace(',', '').strip()
            try:
                price_num = ''.join(filter(lambda x: x.isdigit() or x == '.', price_str.split()[0]))
                current_product['price'] = float(price_num) if price_num else 0.0
            except (ValueError, IndexError):
                current_product['price'] = 0.0
        elif 'image:' in lower_line or 'image url:' in lower_line:
            img_url = line.split(':', 1)[1].strip()
            if '(' in img_url and ')' in img_url:
                img_url = img_url[img_url.index('(')+1:img_url.index(')')]
            current_product['image_url'] = img_url
        elif 'functional match:' in lower_line or 'matches functional' in lower_line:
            current_product['functional_match'] = line.split(':', 1)[1].strip()
        elif 'style match:' in lower_line or 'matches style' in lower_line or 'style preference' in lower_line:
            current_product['style_match'] = line.split(':', 1)[1].strip()
        elif 'visual characteristics:' in lower_line or 'characteristics:' in lower_line:
            # Try to parse as dict
            char_str = line.split(':', 1)[1].strip()
            # Simple parsing - look for color, material, style
            chars = {}
            if 'color' in char_str.lower():
                chars['color'] = 'extracted from text'  # Simplified
            if 'material' in char_str.lower():
                chars['material'] = 'extracted from text'
            if 'style' in char_str.lower():
                chars['style'] = 'extracted from text'
            current_product['visual_characteristics'] = chars if chars else {'raw': char_str}
        elif 'color:' in lower_line:
            if 'visual_characteristics' not in current_product:
                current_product['visual_characteristics'] = {}
            current_product['visual_characteristics']['color'] = line.split(':', 1)[1].strip()
        elif 'material:' in lower_line:
            if 'visual_characteristics' not in current_product:
                current_product['visual_characteristics'] = {}
            current_product['visual_characteristics']['material'] = line.split(':', 1)[1].strip()
        elif 'style:' in lower_line and 'style match' not in lower_line:
            if 'visual_characteristics' not in current_product:
                current_product['visual_characteristics'] = {}
            current_product['visual_characteristics']['style'] = line.split(':', 1)[1].strip()

    # Add last product if valid
    if current_product and 'name' in current_product and 'url' in current_product:
        current_product.setdefault('price', 0.0)
        current_product.setdefault('image_url', None)
        current_product.setdefault('functional_match', '')
        current_product.setdefault('style_match', '')
        current_product.setdefault('visual_characteristics', {})
        products.append(RefinedProduct(**current_product))

    # Replace hallucinated URLs with real ones from search results
    if real_urls and len(products) > 0:
        for i, product in enumerate(products):
            if i < len(real_urls):
                # Replace the URL with a real one from search results
                product.url = real_urls[i]

    # Associate images if available (overwrite any parsed from text)
    # The images from the API are real, the ones in the text are often hallucinated
    if images and len(products) > 0:
        for i, product in enumerate(products):
            if i < len(images):
                product.image_url = images[i]  # Always use real API images

    # If parsing failed, return debug info
    if not products:
        products.append(RefinedProduct(
            name="Parsing Error - Check Response",
            url="",
            price=0.0,
            image_url=None,
            functional_match="",
            style_match="",
            visual_characteristics={'debug': response_text[:300]}
        ))

    return products