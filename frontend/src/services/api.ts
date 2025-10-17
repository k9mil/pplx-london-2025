import { API } from "@/constants";
import type { UploadResponse, UploadError } from "@/types";

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
