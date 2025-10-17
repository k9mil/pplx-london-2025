import base64
import os
from typing import Dict, Any, List
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import mimetypes
import time
import requests

class ImageMerger:
    """Class for merging images using Gemini API."""
    MODEL = "gemini-2.5-flash-image"
    
    def __init__(self, api_key: str = None):
        """
        Initialize the ImageMerger with Gemini API key.
        
        Args:
            api_key (str): Gemini API key
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = genai.Client(api_key=api_key)
    
    def merge_images(self, image1_url: str, image2_url: str, prompt: str = None):
        """
        Merge two images using Gemini API with a given prompt.
        
        Args:
            image1_url (str): URL of the first image
            image2_url (str): URL of the second image
            prompt (str): Text prompt describing how to merge the images
            
        Returns:
            Dict[str, Any]: API response containing the merged image
        """
        # Loads images from URLs and converts them into GenAI Part objects.
        contents = []
        image_urls = [image1_url, image2_url]
        
        for image_url in image_urls:
            try:
                # Download image from URL
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                image_data = response.content
                
                # Determine MIME type from URL or response headers
                mime_type = self._get_mime_type_from_url(image_url, response.headers)
                
                contents.append(
                    types.Part(inline_data=types.Blob(data=image_data, mime_type=mime_type))
                )
                
            except requests.RequestException as e:
                raise Exception(f"Error downloading image from {image_url}: {str(e)}")
        
        # Use provided prompt or default prompt
        if prompt is None:
            prompt = "Create a combination of the images. Blend the first image object in the foreground with the second image background as ambiance and background, mixing elements from both. Make sure the lighting and style remain consistent."

        contents.append(genai.types.Part.from_text(text=prompt))
        
        try:
            response = self.client.models.generate_content(
                model=self.MODEL, 
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )
            print(response)
            return response
            
        except Exception as e:
            raise Exception(f"Error merging images: {str(e)}")
    
    def save_merged_image(self, api_response, output_dir: str) -> bool:
        for part in api_response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                timestamp = int(time.time())
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type)
                file_name = os.path.join(
                    output_dir,
                    f"remixed_image_{timestamp}_{file_extension}",
                )
                self._save_binary_file(file_name, part.inline_data.data)

    def _get_mime_type(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            raise ValueError(f"Could not determine MIME type for {file_path}")
        return mime_type
    
    def _get_mime_type_from_url(self, url: str, headers: dict = None) -> str:
        """
        Determine MIME type from URL or response headers.
        
        Args:
            url (str): Image URL
            headers (dict): HTTP response headers
            
        Returns:
            str: MIME type
        """
        # First try to get from Content-Type header
        if headers and 'content-type' in headers:
            content_type = headers['content-type']
            # Remove any charset information
            mime_type = content_type.split(';')[0].strip()
            if mime_type.startswith('image/'):
                return mime_type
        
        # Fallback to URL extension
        mime_type, _ = mimetypes.guess_type(url)
        if mime_type and mime_type.startswith('image/'):
            return mime_type
        
        # Default fallback
        return 'image/jpeg'
    
    def _save_binary_file(self, file_name: str, data: bytes):
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")