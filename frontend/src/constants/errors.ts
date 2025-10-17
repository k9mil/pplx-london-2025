export const ERROR_MESSAGES = {
  MICROPHONE_ACCESS_DENIED:
    "Microphone access denied. Please enable it to continue.",
  MICROPHONE_NOT_FOUND: "No microphone found. Please connect a microphone.",
  CONVERSATION_FAILED: "Failed to start conversation. Please try again.",
} as const;

export const ERROR_TYPES = {
  NOT_ALLOWED: "NotAllowedError",
  NOT_FOUND: "NotFoundError",
} as const;
