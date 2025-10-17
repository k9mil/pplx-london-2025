import { motion } from "framer-motion";
import { useState, useCallback, useMemo } from "react";
import { X, Check } from "lucide-react";
import { FinalProductView } from "./FinalProductView";
import { ANIMATION, IMAGES, ALT_TEXT } from "@/constants";
import type { BedroomItemId } from "@/types";

const BEDROOM_ITEMS: readonly BedroomItemId[] = [
  "bedroom1",
  "bedroom2",
] as const;

export function ItemSelectionView() {
  const [currentItemIndex, setCurrentItemIndex] = useState<number>(0);
  const [showFinalView, setShowFinalView] = useState<boolean>(false);

  const currentItem = BEDROOM_ITEMS[currentItemIndex];
  const isLastItem = currentItemIndex === BEDROOM_ITEMS.length - 1;

  const imageSrc = useMemo(() => {
    return currentItem === "bedroom1" ? IMAGES.BEDROOM_ONE : IMAGES.BEDROOM_TWO;
  }, [currentItem]);

  const imageAlt = useMemo(() => {
    return currentItem === "bedroom1"
      ? ALT_TEXT.BEDROOM_ONE
      : ALT_TEXT.BEDROOM_TWO;
  }, [currentItem]);

  const handleNext = useCallback((): void => {
    if (isLastItem) {
      setShowFinalView(true);
    } else {
      setCurrentItemIndex((prev) => prev + 1);
    }
  }, [isLastItem]);

  const handleReject = useCallback((): void => {
    handleNext();
  }, [handleNext]);

  const handleAccept = useCallback((): void => {
    handleNext();
  }, [handleNext]);

  if (showFinalView) {
    return <FinalProductView />;
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <div className="flex flex-col items-center gap-8">
        <motion.div
          key={currentItem}
          initial={{ filter: ANIMATION.BLUR.EXTRA_LARGE, opacity: 0 }}
          animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
          transition={{
            duration: ANIMATION.DURATION.SLOW,
            ease: ANIMATION.EASING.OUT,
          }}
          className="relative"
        >
          <img
            src={imageSrc}
            alt={imageAlt}
            className="max-w-2xl max-h-[32rem] object-contain rounded-lg"
          />
        </motion.div>

        <div className="flex gap-6">
          <motion.button
            initial={{ filter: ANIMATION.BLUR.LARGE, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              delay: ANIMATION.DELAY.LONG,
              duration: ANIMATION.DURATION.FAST,
              ease: ANIMATION.EASING.OUT,
            }}
            onClick={handleReject}
            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:border-red-200 transition-colors"
            aria-label="Reject item"
          >
            <X className="w-4 h-4 text-gray-600" />
          </motion.button>

          <motion.button
            initial={{ filter: ANIMATION.BLUR.LARGE, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              delay: ANIMATION.DELAY.LONG,
              duration: ANIMATION.DURATION.FAST,
              ease: ANIMATION.EASING.OUT,
            }}
            onClick={handleAccept}
            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:border-green-200 transition-colors"
            aria-label="Accept item"
          >
            <Check className="w-4 h-4 text-gray-600" />
          </motion.button>
        </div>
      </div>
    </div>
  );
}
