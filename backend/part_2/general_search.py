import os
from dotenv import load_dotenv
from perplexity import Perplexity
from typing import List, Optional, Dict, Any
from .models import UserPreference, ProductResult
import re
import httpx
import asyncio
import traceback

load_dotenv()

api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables")


async def fetch_and_parse_product(
    url: str, index: int, total: int, client: Perplexity
) -> Optional[ProductResult]:
    try:
        print(f"\n[{index}/{total}] Processing: {url}")

        jina_url = f"https://r.jina.ai/{url}"
        print("   Fetching via Jina Reader...")

        url_lower = url.lower()
        if "ikea.com" in url_lower:
            css_selectors = ".pip-price-module__primary-currency-price, .pip-product-gallery__right-section-wrapper, .pip-product-summary__description"
            site_name = "IKEA"
        elif "jysk.co.uk" in url_lower:
            css_selectors = (
                ".product-sumbox-series, .ssr-product-price__value, .img-responsive"
            )
            site_name = "JYSK"
        else:
            css_selectors = "body"
            site_name = "Unknown"

        print(f"   Site: {site_name}")

        try:
            async with httpx.AsyncClient(timeout=120.0) as http_client:
                headers = {"X-Target-Selector": css_selectors}
                # print(headers)
                jina_response = await http_client.get(jina_url, headers=headers)
                jina_content = jina_response.text
                # print(jina_content)

            print(f"   ✅ Fetched {len(jina_content)} characters from Jina")
        except httpx.TimeoutException:
            print("   ❌ Timeout fetching from Jina")
            return None
        except httpx.HTTPError as e:
            print(f"   ❌ HTTP error fetching from Jina: {str(e)}")
            return None
        except Exception as e:
            print(f"   ❌ Unexpected error fetching from Jina: {str(e)}")
            return None

        print("   Parsing with Sonar...")

        parse_prompt = f"""
Extract product information from this {site_name} product page content:

{jina_content}

Return in this exact format:
Product Name: [exact product name]
URL: {url}
Price: [price in GBP with £ symbol]
Description: [brief 1-2 sentence description]
Image URL: [main product image URL if found]
"""

        try:
            parse_response = client.chat.completions.create(
                model="sonar",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a product information extractor. Extract structured data accurately.",
                    },
                    {"role": "user", "content": parse_prompt},
                ],
                temperature=0.1,
            )
        except Exception as e:
            print(f"   ❌ Error calling Sonar API: {str(e)}")
            traceback.print_exc()
            return None

        try:
            parsed_content = parse_response.choices[0].message.content
            parsed_text = parsed_content if isinstance(parsed_content, str) else ""
            product = parse_single_product(parsed_text, url)

            if product:
                print(f"   ✅ {product.name} - £{product.price}")
                print(f"   📍 URL: {product.url}")
                print(
                    f"   🖼️  Image: {product.image_url if product.image_url else 'None'}"
                )
                return product
            else:
                print("   ❌ Failed to parse product data")
                return None
        except Exception as e:
            print(f"   ❌ Error parsing response: {str(e)}")
            traceback.print_exc()
            return None

    except Exception as e:
        print(f"   ❌ Unexpected error in fetch_and_parse_product: {str(e)}")
        traceback.print_exc()
        return None


async def general_search(
    user_pref: UserPreference, num_results: int = 200
) -> List[ProductResult]:
    try:
        print("\n" + "=" * 80)
        print(f"STEP 1: Finding {num_results} product URLs")
        print("=" * 80 + "\n")

        features_str = (
            ", ".join(user_pref.essential_features)
            if user_pref.essential_features
            else "none specified"
        )

        search_prompt = f"""
Search for many different {user_pref.type} product pages from IKEA UK and JYSK UK. I need at least {num_results} individual products total.

Budget: £{user_pref.budget_range[0]}-£{user_pref.budget_range[1]}
Features: {features_str}

Search for things like:
"site:ikea.com/gb/en/p sofa"
"site:jysk.co.uk sofa"

Use the web_search tool - this is MANDATORY.

Find as many DIFFERENT products as you can from these 2 retailers - different models, brands, sizes, colors within the budget.
"""

        try:
            client = Perplexity(api_key=api_key)
            print("✅ Perplexity client initialized")
        except Exception:
            print("❌ Error initializing Perplexity client:")
            traceback.print_exc()
            raise

        try:
            print("🔍 Calling Sonar Pro with Pro Search (streaming)...")
            stream_response = client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "user", "content": search_prompt},
                ],
                temperature=0.1,
                stream=True,
                web_search_options={"search_type": "pro"},
            )

            print("📡 Processing streaming response...")
            final_chunk = None
            for chunk in stream_response:
                final_chunk = chunk
                if hasattr(chunk, "choices") and chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        pass

            print("✅ Streaming complete")

            if not final_chunk:
                raise Exception("No response chunks received")

        except Exception:
            print("❌ Error calling Sonar API:")
            traceback.print_exc()
            raise

        try:
            search_results = getattr(final_chunk, "search_results", []) or []

            print(f"🔍 Found {len(search_results)} search results from Perplexity")

            urls = []

            product_patterns = [
                "/p/",
            ]

            category_patterns = [
                "/cat/",
                "/category/",
                "/categories/",
                "/collection/",
                "/collections/",
                "/shop-by-product/",
                "/browse/",
                "/department/",
                "/departments/",
                "/by-price/",
                "/by-style/",
                "/rooms/",
                "/filter",
                "youtube.com",
                "lowerBound=",
                "upperBound=",
                "?number-of-seats=",
                "?type=",
                "?page=",
                "?material-type=",
                "/features/",
            ]

            def is_product_page(url: str) -> bool:
                url_lower = url.lower()

                has_category_pattern = any(
                    pattern in url_lower for pattern in category_patterns
                )
                if has_category_pattern:
                    return False

                has_product_pattern = any(
                    pattern in url_lower for pattern in product_patterns
                )
                if has_product_pattern:
                    return True

                if "jysk.co.uk" in url_lower:
                    path_parts = url.split("/")
                    if len(path_parts) >= 5:
                        last_part = path_parts[-1] if path_parts[-1] else path_parts[-2]
                        if last_part and len(last_part) > 15 and "-" in last_part:
                            return True

                return False

            if search_results:
                print("🔗 Filtering for product pages...")
                for i, result in enumerate(search_results[:10], 1):
                    url = None
                    if hasattr(result, "url"):
                        url = result.url
                    elif isinstance(result, dict) and "url" in result:
                        url = result["url"]

                    if url:
                        url_lower = url.lower()
                        has_product = any(p in url_lower for p in product_patterns)
                        has_category = any(c in url_lower for c in category_patterns)

                        print(f"\n   [{i}] {url}")
                        print(f"       Has /p/ or /product/: {has_product}")
                        print(f"       Has category pattern: {has_category}")

                        if is_product_page(url):
                            urls.append(url)
                            print("       ✅ ACCEPTED")
                        else:
                            print("       ❌ REJECTED")

                for result in search_results:
                    url = None
                    if hasattr(result, "url"):
                        url = result.url
                    elif isinstance(result, dict) and "url" in result:
                        url = result["url"]

                    if url and is_product_page(url):
                        if url not in urls:
                            urls.append(url)

            print(f"\n✅ Found {len(urls)} product page(s)")
        except Exception:
            print("❌ Error extracting URLs:")
            traceback.print_exc()
            raise

        if not urls:
            print("⚠️ No product URLs found after filtering, returning empty list")
            return []

        if len(urls) < num_results:
            print(
                f"⚠️ Warning: Only found {len(urls)} product URLs, requested {num_results}"
            )

        print("\n" + "=" * 80)
        print(
            f"STEP 2: Fetching and parsing {min(len(urls), num_results)} products concurrently"
        )
        print("=" * 80 + "\n")

        async def fetch_all_products():
            try:
                tasks = [
                    fetch_and_parse_product(url, i, len(urls[:num_results]), client)
                    for i, url in enumerate(urls[:num_results], 1)
                ]
                print(f"✅ Created {len(tasks)} async tasks")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                print("✅ Completed all async tasks")

                valid_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        print(f"❌ Task {i + 1} raised exception: {result}")
                        traceback.print_exception(
                            type(result), result, result.__traceback__
                        )
                    elif result is not None:
                        valid_results.append(result)

                return valid_results
            except Exception:
                print("❌ Error in fetch_all_products:")
                traceback.print_exc()
                return []

        try:
            products = await fetch_all_products()
            print(f"✅ Async execution completed, got {len(products)} products")
        except Exception:
            print("❌ Error running async tasks:")
            traceback.print_exc()
            raise

        print("\n" + "=" * 80)
        print(f"✅ Successfully parsed {len(products)} products")
        print("=" * 80 + "\n")

        return products

    except Exception:
        print("\n❌ FATAL ERROR in general_search:")
        traceback.print_exc()
        raise


def extract_urls(text: str) -> List[str]:
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    return urls


def parse_single_product(response_text: str, url: str) -> Optional[ProductResult]:
    lines = response_text.split("\n")
    product_data: Dict[str, Any] = {"url": url}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower_line = line.lower()

        if lower_line.startswith("product name:"):
            product_data["name"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("price:"):
            price_text = line.split(":", 1)[1].strip()
            price_match = re.search(r"£?\s*([0-9,]+(?:\.[0-9]{2})?)", price_text)
            if price_match:
                try:
                    product_data["price"] = float(price_match.group(1).replace(",", ""))
                except ValueError:
                    product_data["price"] = 0.0
        elif lower_line.startswith("description:"):
            product_data["description"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("image url:"):
            img_url = line.split(":", 1)[1].strip()
            if img_url and img_url.startswith("http"):
                product_data["image_url"] = img_url

    if "name" in product_data:
        if "price" not in product_data:
            product_data["price"] = 0.0
        if "description" not in product_data:
            product_data["description"] = ""
        if "image_url" not in product_data:
            product_data["image_url"] = None

        try:
            return ProductResult(**product_data)
        except Exception as e:
            print(f"   Error creating ProductResult: {e}")
            return None

    return None
