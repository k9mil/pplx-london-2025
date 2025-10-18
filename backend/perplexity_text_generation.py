import os
from dotenv import load_dotenv
import traceback
from perplexity import Perplexity
from config import settings

api_key = settings.PERPLEXITY_API_KEY
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables")

async def generate_text(model: str, messages: str) :
    # Initialize Perplexity client
    try:
        client = Perplexity(api_key=api_key)
        print("✅ Perplexity client initialized")
    except Exception:
        print("❌ Error initializing Perplexity client:")
        traceback.print_exc()
        raise

    # Generate text
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            disable_search= True
        )
        content = response.choices[0].message.content
        return content
    except Exception:
        print("❌ Error generating text:")
        traceback.print_exc()
        raise