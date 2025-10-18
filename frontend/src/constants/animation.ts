export const ANIMATION_DURATION = {
  FAST: 1.2,
  NORMAL: 1.3,
  SLOW: 1.4,
} as const;

export const ANIMATION_DELAY = {
  SHORT: 0.2,
  MEDIUM: 0.4,
  LONG: 0.6,
  EXTRA_LONG: 0.8,
} as const;

export const BLUR_VALUES = {
  SMALL: "blur(12px)",
  MEDIUM: "blur(14px)",
  LARGE: "blur(16px)",
  EXTRA_LARGE: "blur(20px)",
  NONE: "blur(0px)",
} as const;

export const EASING = {
  OUT: "easeOut",
  IN: "easeIn",
  IN_OUT: "easeInOut",
} as const;
