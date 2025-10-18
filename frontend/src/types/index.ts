export type ConversationStatus = "connected" | "disconnected" | "connecting";

export type BedroomItemId = "bedroom1" | "bedroom2";

export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    file: {
      filename: string;
      original_filename: string;
      size: number;
      width: number;
      height: number;
      format: string;
      content_type: string;
      storage: string;
      public_url?: string;
      path?: string;
      bucket?: string;
      blob_name?: string;
      created_at?: string;
    };
    analysis: {
      status: string;
      message: string;
    };
  };
}

export interface UploadError {
  detail: string;
}

export type UploadStatus = "idle" | "uploading" | "success" | "error";

export interface ImageToTextRequest {
  blob_name?: string;
  image_url?: string;
  prompt?: string;
  detail_level?: "low" | "medium" | "high";
}

export interface ImageToTextResponse {
  success: boolean;
  message: string;
  description?: string;
  image_info?: {
    blob_name?: string;
    bucket?: string;
    size?: number;
    content_type?: string;
    created?: string;
    image_url?: string;
  };
}

export interface ImageDescription {
  filename: string;
  description: string;
  blob_name?: string;
}

export interface ProductResult {
  name: string;
  url: string;
  price: number;
  description: string;
  image_url: string | null;
}

export interface GeneralSearchRequest {
  budget_range: [number, number];
  essential_features: string[];
  type: string;
}

export interface MergeImagesRequest {
  url1: string;
  url2: string;
  prompt?: string;
}

export interface MergeImagesResponse {
  success: boolean;
  message: string;
  data: {
    file: {
      filename: string;
      original_filename: string;
      public_url?: string;
      path?: string;
      size: number;
      width: number;
      height: number;
      format: string;
      content_type: string;
      storage: string;
    };
  };
}
