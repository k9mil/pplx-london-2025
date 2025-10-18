import { motion } from "framer-motion";
import { useState, useCallback, useEffect } from "react";
import { X, Check } from "lucide-react";
import { FinalProductView } from "./FinalProductView";
import { ANIMATION } from "@/constants";
import type { ProductResult } from "@/types";

interface ItemSelectionViewProps {
  products: ProductResult[];
}

export function ItemSelectionView({ products = [] }: ItemSelectionViewProps) {
  const [currentItemIndex, setCurrentItemIndex] = useState<number>(0);
  const [showFinalView, setShowFinalView] = useState<boolean>(false);

  const currentProduct = products[currentItemIndex];
  const isLastItem = currentItemIndex === products.length - 1;

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

  useEffect(() => {
    if (currentProduct && !currentProduct.image_url) {
      handleNext();
    }
  }, [currentProduct, handleNext]);

  if (showFinalView) {
    return <FinalProductView />;
  }

  if (!currentProduct) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
        <p className="text-muted-foreground">No products available</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <div className="flex flex-col items-center gap-8">
        <motion.div
          key={currentProduct.url}
          initial={{ filter: ANIMATION.BLUR.EXTRA_LARGE, opacity: 0 }}
          animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
          transition={{
            duration: ANIMATION.DURATION.SLOW,
            ease: ANIMATION.EASING.OUT,
          }}
          className="relative"
        >
          <img
            src={currentProduct.image_url || ""}
            alt={currentProduct.name}
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
