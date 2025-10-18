import { API } from "@/constants";
import type {
  UploadResponse,
  UploadError,
  ImageToTextRequest,
  ImageToTextResponse,
  GeneralSearchRequest,
  ProductResult,
  MergeImagesRequest,
  MergeImagesResponse,
} from "@/types";

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.PROCESS}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error: UploadError = await response.json();
    throw new Error(error.detail || "Upload failed");
  }

  return response.json();
};

export const imageToText = async (
  request: ImageToTextRequest
): Promise<ImageToTextResponse> => {
  const response = await fetch(
    `${API.BASE_URL}${API.ENDPOINTS.IMAGE_TO_TEXT}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    const error: UploadError = await response.json();
    throw new Error(error.detail || "Image to text conversion failed");
  }

  return response.json();
};

export const generalSearch = async (
  request: GeneralSearchRequest,
  numResults: number = 10
): Promise<ProductResult[]> => {
  const response = await fetch(
    `${API.BASE_URL}${API.ENDPOINTS.GENERAL_SEARCH}?num_results=${numResults}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    try {
      const error: UploadError = await response.json();
      throw new Error(
        error.detail || `Search failed with status ${response.status}`
      );
    } catch (parseError) {
      throw new Error(`Search failed with status ${response.status}`);
    }
  }

  return response.json();
};

export const mergeImages = async (
  request: MergeImagesRequest
): Promise<MergeImagesResponse> => {
  const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.MERGE_IMAGES}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error: UploadError = await response.json();
    throw new Error(error.detail || "Image merge failed");
  }

  return response.json();
};
