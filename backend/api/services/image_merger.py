import os
from typing import Optional
from google import genai
from google.genai import types
import mimetypes
import time
import requests


class ImageMerger:
    MODEL = "gemini-2.5-flash-image"

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = genai.Client(api_key=api_key)

    def merge_images(
        self, image1_url: str, image2_url: str, prompt: Optional[str] = None
    ):
        contents = []
        image_urls = [image1_url, image2_url]

        for image_url in image_urls:
            try:
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                image_data = response.content

                mime_type = self._get_mime_type_from_url(
                    image_url, dict(response.headers)
                )

                contents.append(
                    types.Part(
                        inline_data=types.Blob(data=image_data, mime_type=mime_type)
                    )
                )

            except requests.RequestException as e:
                raise Exception(f"Error downloading image from {image_url}: {str(e)}")

        if prompt is None:
            prompt = "Create a combination of the images. Blend the first image object in the foreground with the second image background as ambiance and background, mixing elements from both. Make sure the lighting and style remain consistent."

        contents.append(types.Part.from_text(text=prompt))

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            )
            return response

        except Exception as e:
            raise Exception(f"Error merging images: {str(e)}")

    def save_merged_image(
        self, api_response, output_dir: str = "image_temp_folder/"
    ) -> Optional[str]:
        os.makedirs(output_dir, exist_ok=True)

        image_path = None
        for part in api_response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                timestamp = int(time.time())
                file_extension = (
                    mimetypes.guess_extension(part.inline_data.mime_type) or ".png"
                )
                file_name = os.path.join(
                    output_dir,
                    f"remixed_image_{timestamp}{file_extension}",
                )
                image_path = self._save_binary_file(file_name, part.inline_data.data)
        return image_path

    def _get_mime_type(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            raise ValueError(f"Could not determine MIME type for {file_path}")
        return mime_type

    def _get_mime_type_from_url(self, url: str, headers: Optional[dict] = None) -> str:
        if headers and "content-type" in headers:
            content_type = headers["content-type"]
            mime_type = content_type.split(";")[0].strip()
            if mime_type.startswith("image/"):
                return mime_type

        mime_type, _ = mimetypes.guess_type(url)
        if mime_type and mime_type.startswith("image/"):
            return mime_type

        return "image/jpeg"

    def _save_binary_file(self, file_name: str, data: bytes) -> str:
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")
        return file_name
