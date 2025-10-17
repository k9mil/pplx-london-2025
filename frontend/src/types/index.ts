export type ConversationStatus = "connected" | "disconnected" | "connecting";

export type BedroomItemId = "bedroom1" | "bedroom2";

export interface UploadResponse {
  success: boolean;
  filename: string;
  content_type: string;
  size: number;
  data: string;
}

export interface UploadError {
  detail: string;
}

export type UploadStatus = "idle" | "uploading" | "success" | "error";
