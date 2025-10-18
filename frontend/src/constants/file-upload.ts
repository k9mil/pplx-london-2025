export const FILE_UPLOAD = {
  MAX_FILES: 5,
  MAX_SIZE_MB: 10,
  MAX_SIZE_BYTES: 10 * 1024 * 1024,
} as const;

export const ALLOWED_FILE_TYPES = [
  "image/",
  "application/pdf",
  "text/",
] as const;

export const FILE_UPLOAD_MESSAGES = {
  MAX_FILES_EXCEEDED: `You can only upload up to ${FILE_UPLOAD.MAX_FILES} files`,
  INVALID_FILE_TYPE: "Only images, PDFs, and text files are allowed",
  FILE_TOO_LARGE: (sizeMB: number) => `File size must be less than ${sizeMB}MB`,
} as const;
