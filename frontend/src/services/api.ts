import { API } from "@/constants";
import type {
  UploadResponse,
  UploadError,
  ImageToTextRequest,
  ImageToTextResponse,
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
