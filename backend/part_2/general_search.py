import os
from pathlib import Path
from dotenv import load_dotenv
from perplexity import Perplexity
from typing import List
from datetime import datetime
from .models import UserPreference, ProductResult

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables")


def general_search(user_pref: UserPreference, num_results: int = 5) -> List[ProductResult]:  # Reduced to 5 for better quality
    """
    Performs a general furniture search based on user preferences.

    Args:
        user_pref: UserPreference object containing search criteria
        num_results: Number of results to return (default: 10)

    Returns:
        List of ProductResult objects
    """
    # Initialize Perplexity client
    client = Perplexity(api_key=api_key)

    # Build the search prompt
    dimensions_str = ", ".join([f"{k}: {v} inches" for k, v in user_pref.dimensions.items()])
    features_str = ", ".join(user_pref.essential_features) if user_pref.essential_features else "none specified"

    prompt = f"""
TASK: Find EXACTLY {num_results} real {user_pref.type} products currently for sale online from UK retailers.

REQUIREMENTS:
- Budget: £{user_pref.budget_range[0]} - £{user_pref.budget_range[1]} (prices in GBP)
- Dimensions: {dimensions_str}
- Features: {features_str}
- ONLY search from these UK retailers: IKEA UK, H&M Home UK, Zara Home UK, JYSK UK

MANDATORY PROCESS - YOU MUST FOLLOW THESE STEPS:

STEP 1: Use the web_search tool to search for "{user_pref.type} for sale site:ikea.com/gb OR site:hm.com/gb OR site:zarahome.com/gb OR site:jysk.co.uk -inurl:"https://jysk.co.uk/living-room/sofa-beds""

STEP 2: For EACH product URL you find, you MUST use the fetch_url_content tool to:
- Open the URL and read the actual product page
- Verify it's a real product page (not a category page, blog, or search results)
- Verify it's from one of the approved UK retailers (IKEA UK, H&M Home UK, Zara Home UK, JYSK UK)
- Extract the exact product name from the page
- Extract the exact price from the page in GBP (£)
- Verify the product is in stock

STEP 3: ONLY after using fetch_url_content to verify a product, include it in your response with:
- Product name (from the fetched page content)
- URL (the URL you fetched - must be .co.uk or /gb domain)
- Price (from the fetched page content in GBP £)
- Brief description

IMPORTANT: I need to see you use both web_search AND fetch_url_content tools. Show your reasoning for each product you evaluate. Do NOT skip the fetch_url_content step - it is mandatory for each product. All prices must be in British Pounds (£).

Find {num_results} products total from the approved UK retailers only. Take your time and be thorough.
"""

    print(prompt)

    # Make the API call with Pro Search enabled
    response_stream = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful furniture shopping assistant. Use web_search and fetch_url_content tools to find REAL products with working URLs and accurate prices."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,  # Lower for more careful/consistent behavior
        stream=True,  # Required for Pro Search
        web_search_options={
            "search_type": "pro"  # Enable Pro Search
        },
        extra_body={
            "return_images": True,
        },
        search_recency_filter="month"
    )

    # Collect the full response from streaming
    full_content = ""
    reasoning_steps = []
    search_results = []
    citations = []
    images = []

    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    first_chunk_logged = False
    for chunk in response_stream:
        try:
            # Log first chunk to see structure
            if not first_chunk_logged:
                chunk_debug_file = Path(__file__).parent.parent / f'chunk_debug_{timestamp}.txt'
                with open(chunk_debug_file, 'w') as f:
                    f.write("=== FIRST CHUNK ATTRIBUTES ===\n")
                    f.write(str(dir(chunk)) + "\n\n")
                    f.write("=== FIRST CHUNK DICT (if available) ===\n")
                    if hasattr(chunk, '__dict__'):
                        f.write(str(chunk.__dict__) + "\n\n")
                    f.write("=== FIRST CHUNK STR ===\n")
                    f.write(str(chunk))
                print(f"First chunk debug written to: {chunk_debug_file}")

                # Print all fields from the sample response format
                print("\n=== CHUNK METADATA ===")
                if hasattr(chunk, 'id'):
                    print(f"ID: {chunk.id}")
                if hasattr(chunk, 'model'):
                    print(f"Model: {chunk.model}")
                if hasattr(chunk, 'created'):
                    print(f"Created: {chunk.created}")
                if hasattr(chunk, 'object'):
                    print(f"Object: {chunk.object}")
                if hasattr(chunk, 'usage'):
                    print(f"Usage: {chunk.usage}")
                    if hasattr(chunk.usage, 'prompt_tokens'):
                        print(f"  Prompt tokens: {chunk.usage.prompt_tokens}")
                    if hasattr(chunk.usage, 'completion_tokens'):
                        print(f"  Completion tokens: {chunk.usage.completion_tokens}")
                    if hasattr(chunk.usage, 'total_tokens'):
                        print(f"  Total tokens: {chunk.usage.total_tokens}")
                    if hasattr(chunk.usage, 'search_context_size'):
                        print(f"  Search context size: {chunk.usage.search_context_size}")
                    if hasattr(chunk.usage, 'cost'):
                        print(f"  Cost: {chunk.usage.cost}")
                print("===================\n")
                first_chunk_logged = True

            # Collect reasoning steps from top level (new format)
            if hasattr(chunk, 'reasoning_steps') and chunk.reasoning_steps:
                print(f"Found {len(chunk.reasoning_steps)} reasoning steps in chunk")
                reasoning_steps.extend(chunk.reasoning_steps)

            # Collect reasoning steps from delta or message (old format - fallback)
            if chunk.choices:
                choice = chunk.choices[0]

                # Check delta for reasoning steps
                if hasattr(choice.delta, 'reasoning_steps') and choice.delta.reasoning_steps:
                    print(f"Found {len(choice.delta.reasoning_steps)} reasoning steps in delta")
                    reasoning_steps.extend(choice.delta.reasoning_steps)

                # Check message for reasoning steps (fallback)
                if hasattr(choice, 'message') and hasattr(choice.message, 'reasoning_steps') and choice.message.reasoning_steps:
                    for step in choice.message.reasoning_steps:
                        if step not in reasoning_steps:  # Avoid duplicates
                            reasoning_steps.append(step)

            # Collect search results
            if hasattr(chunk, 'search_results') and chunk.search_results:
                print(f"Found {len(chunk.search_results)} search results")
                search_results.extend(chunk.search_results)

            # Collect citations
            if hasattr(chunk, 'citations') and chunk.citations:
                print(f"Found {len(chunk.citations)} citations")
                citations.extend(chunk.citations)

            # Collect images
            if hasattr(chunk, 'images') and chunk.images:
                print(f"Found {len(chunk.images)} images")
                images.extend(chunk.images)

            # Collect content
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content

        except Exception as e:
            import traceback
            print(f"\n!!! ERROR processing chunk !!!")
            print(f"Error: {str(e)}")
            print(f"Stack trace:")
            traceback.print_exc()
            print(f"Chunk: {chunk}")
            print(f"!!!\n")

    # Create a completion-like object for compatibility
    class CompletionWrapper:
        def __init__(self, content, reasoning_steps, search_results, citations, images):
            self.choices = [type('obj', (object,), {
                'message': type('obj', (object,), {'content': content})()
            })()]
            self.reasoning_steps = reasoning_steps
            self.search_results = search_results
            self.citations = citations
            self.images = images

    completion = CompletionWrapper(full_content, reasoning_steps, search_results, citations, images)

    # Get the response
    response_text = completion.choices[0].message.content

    # Extract data from completion
    images_list = []
    if hasattr(completion, 'images') and completion.images:
        for img in completion.images:
            if isinstance(img, dict) and 'image_url' in img:
                images_list.append(img.get('image_url'))
            elif hasattr(img, 'image_url'):
                images_list.append(img.image_url)

    # Write debug output to file
    debug_file = Path(__file__).parent.parent / f'debug_output_{timestamp}.txt'
    with open(debug_file, 'w') as f:
        f.write("=== RESPONSE METADATA ===\n")
        # Try to get metadata from the first chunk if we saved it
        # Note: In streaming, some fields may only appear in specific chunks
        f.write(f"Model: sonar-pro (from request)\n")
        f.write(f"Stream: True\n")
        f.write(f"Search type: pro\n\n")

        f.write("=== PRO SEARCH SUMMARY ===\n")
        f.write(f"Reasoning steps: {len(reasoning_steps)}\n")
        f.write(f"Citations: {len(citations)}\n")
        f.write(f"Search results: {len(search_results)}\n")
        f.write(f"Images: {len(images_list)}\n\n")

        f.write("=== TOOL USAGE ===\n")
        for i, step in enumerate(reasoning_steps, 1):
            # Convert object to dict if possible
            step_dict = None
            if isinstance(step, dict):
                step_dict = step
            elif hasattr(step, 'model_dump'):
                step_dict = step.model_dump()
            elif hasattr(step, 'dict'):
                step_dict = step.dict()
            elif hasattr(step, '__dict__'):
                step_dict = step.__dict__

            if step_dict:
                f.write(f"{i}. {step_dict}\n\n")
            else:
                f.write(f"{i}. {step}\n\n")

        f.write("\n=== ALL SEARCH RESULTS (DETAILED) ===\n")
        for i, sr in enumerate(search_results, 1):
            f.write(f"\n{i}. ")
            if isinstance(sr, dict):
                f.write(f"Title: {sr.get('title', 'N/A')}\n")
                f.write(f"   URL: {sr.get('url', 'No URL')}\n")
                f.write(f"   Date: {sr.get('date', 'N/A')}\n")
                f.write(f"   Last Updated: {sr.get('last_updated', 'N/A')}\n")
                f.write(f"   Snippet: {sr.get('snippet', 'N/A')}\n")
                f.write(f"   Source: {sr.get('source', 'N/A')}\n")
            elif hasattr(sr, 'url'):
                # Handle object format
                f.write(f"Title: {getattr(sr, 'title', 'N/A')}\n")
                f.write(f"   URL: {sr.url}\n")
                f.write(f"   Date: {getattr(sr, 'date', 'N/A')}\n")
                f.write(f"   Last Updated: {getattr(sr, 'last_updated', 'N/A')}\n")
                f.write(f"   Snippet: {getattr(sr, 'snippet', 'N/A')}\n")
                f.write(f"   Source: {getattr(sr, 'source', 'N/A')}\n")
            else:
                f.write(f"{sr}\n")

        f.write("\n=== CITATIONS ===\n")
        for i, citation in enumerate(citations, 1):
            f.write(f"{i}. {citation}\n")

        f.write("\n=== FULL RESPONSE ===\n")
        f.write(response_text)

    print(f"\nDebug output written to: {debug_file}")

    # Parse the response into ProductResult objects
    products = parse_product_response(response_text, images, citations, search_results)

    return products


def parse_product_response(response_text: str, images: List = None, citations: List = None, search_results: List = None) -> List[ProductResult]:
    """
    Parse Perplexity response into ProductResult objects.
    This is a simple parser - ideally we'd use structured JSON output.

    Args:
        response_text: Raw response from Perplexity API
        images: List of image URLs from the response
        citations: List of citation URLs from the response
        search_results: List of search result objects from the response

    Returns:
        List of ProductResult objects
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

    # Split by numbered items (1., 2., etc.)
    lines = response_text.split('\n')
    current_product = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a new numbered item
        if line[0].isdigit() and '.' in line[:3]:
            # Save previous product if complete
            if current_product:
                if 'name' in current_product and 'url' in current_product:
                    # Set defaults for missing fields
                    current_product.setdefault('price', 0.0)
                    current_product.setdefault('description', '')
                    current_product.setdefault('image_url', None)
                    products.append(ProductResult(**current_product))
            current_product = {}

        # Parse fields
        lower_line = line.lower()

        if 'name:' in lower_line or 'product:' in lower_line:
            current_product['name'] = line.split(':', 1)[1].strip()
        elif 'url:' in lower_line or 'link:' in lower_line:
            url_part = line.split(':', 1)[1].strip()
            # Clean up the URL (remove markdown if present)
            if '(' in url_part and ')' in url_part:
                url_part = url_part[url_part.index('(')+1:url_part.index(')')]
            current_product['url'] = url_part
        elif 'price:' in lower_line or '$' in line:
            # Extract price
            price_str = line.replace('Price:', '').replace('price:', '').replace('$', '').replace(',', '').strip()
            try:
                # Get first number found
                price_num = ''.join(filter(lambda x: x.isdigit() or x == '.', price_str.split()[0]))
                current_product['price'] = float(price_num) if price_num else 0.0
            except (ValueError, IndexError):
                current_product['price'] = 0.0
        elif 'description:' in lower_line:
            current_product['description'] = line.split(':', 1)[1].strip()
        elif 'image:' in lower_line or 'image url:' in lower_line:
            img_url = line.split(':', 1)[1].strip()
            if '(' in img_url and ')' in img_url:
                img_url = img_url[img_url.index('(')+1:img_url.index(')')]
            current_product['image_url'] = img_url

    # Add last product if valid
    if current_product and 'name' in current_product and 'url' in current_product:
        current_product.setdefault('price', 0.0)
        current_product.setdefault('description', '')
        current_product.setdefault('image_url', None)
        products.append(ProductResult(**current_product))

    # Replace hallucinated URLs with real ones from search results
    if real_urls and len(products) > 0:
        for i, product in enumerate(products):
            if i < len(real_urls):
                # Replace the URL with a real one from search results
                product.url = real_urls[i]

    # If we have images from the API response, use them (overwrite any parsed from text)
    # The images from the API are real, the ones in the text are often hallucinated
    if images and len(products) > 0:
        for i, product in enumerate(products):
            if i < len(images):
                product.image_url = images[i]  # Always use real API images

    # If parsing failed completely, return debug info
    if not products:
        products.append(ProductResult(
            name="Parsing Error - Check Response Format",
            url="",
            price=0.0,
            description=response_text[:500],  # First 500 chars for debugging
            image_url=None
        ))

    return products

