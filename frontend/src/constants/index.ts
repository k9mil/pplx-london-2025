export const ANIMATION = {
  DURATION: {
    FAST: 1.2,
    NORMAL: 1.3,
    SLOW: 1.4,
  },
  DELAY: {
    SHORT: 0.2,
    MEDIUM: 0.4,
    LONG: 0.6,
    EXTRA_LONG: 0.8,
  },
  BLUR: {
    SMALL: "blur(12px)",
    MEDIUM: "blur(14px)",
    LARGE: "blur(16px)",
    EXTRA_LARGE: "blur(20px)",
    NONE: "blur(0px)",
  },
  EASING: {
    OUT: "easeOut",
  },
} as const;

export const IMAGES = {
  LOGO: "/logo.png",
  BEDROOM_ONE: "/bedroom-one.jpg",
  BEDROOM_TWO: "/bedroom-two.jpg",
  BEDROOM_THREE: "/bedroom-three.jpg",
} as const;

export const ALT_TEXT = {
  LOGO: "Space Logo",
  BEDROOM_ONE: "Modern Bedroom Design",
  BEDROOM_TWO: "Contemporary Bedroom Layout",
  BEDROOM_THREE: "HEMNES Coffee Table",
} as const;

export const ERRORS = {
  MICROPHONE_ACCESS_DENIED:
    "Microphone access denied. Please enable it to continue.",
  MICROPHONE_NOT_FOUND: "No microphone found. Please connect a microphone.",
  CONVERSATION_FAILED: "Failed to start conversation. Please try again.",
  NOT_ALLOWED: "NotAllowedError",
  NOT_FOUND: "NotFoundError",
} as const;

export const FILE_UPLOAD = {
  MAX_FILES: 5,
  MAX_SIZE_MB: 10,
  MAX_SIZE_BYTES: 10 * 1024 * 1024,
  ALLOWED_TYPES: ["image/"],
  MESSAGES: {
    MAX_FILES_EXCEEDED: "You can only upload up to 5 files",
    INVALID_FILE_TYPE: "Only images are allowed",
    FILE_TOO_LARGE: (sizeMB: number) =>
      `File size must be less than ${sizeMB}MB`,
  },
} as const;

export const API = {
  BASE_URL: "https://pplx-london-api-1052898433949.europe-west2.run.app",
  ENDPOINTS: {
    PROCESS: "/api/process",
    IMAGE_TO_TEXT: "/api/image-to-text",
  },
} as const;

export const UI = {
  STATUS: {
    CONNECTED: "connected" as const,
    DISCONNECTED: "disconnected" as const,
  },
  LABELS: {
    CONNECTED: "Connected",
    CONNECTING: "Connecting",
    MUTE: "Mute",
    UNMUTE: "Unmute",
    END_CONVERSATION: "End conversation",
    RETRY: "Retry",
    PURCHASE: "Purchase",
    BEGIN_PROCESS: "Begin process",
    BROWSE_FILES: "Browse files",
  },
  TEXT: {
    AGENT_CONVERSATION:
      "Now you are conversing with a real-time AI agent to understand your preferences, budget & other needs.",
    DRAG_DROP: "Drag & drop files here",
    CLICK_BROWSE: "Or click to browse (max 5 files)",
    UPLOADING: "Uploading...",
    UPLOAD_SUCCESS: "Upload successful!",
    UPLOAD_ERROR: "Upload failed. Please try again.",
  },
} as const;
