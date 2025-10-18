import { motion } from "framer-motion";
import { useState, useCallback, useEffect } from "react";
import { X, Check } from "lucide-react";
import { FinalProductView } from "./FinalProductView";
import { ANIMATION } from "@/constants";
import type { ProductResult } from "@/types";
import { mergeImages } from "@/services/api";

interface ItemSelectionViewProps {
  products: ProductResult[];
  uploadedImageUrl?: string;
}

const STORAGE_KEY = "lastLikedProduct";

export function ItemSelectionView({
  products = [],
  uploadedImageUrl,
}: ItemSelectionViewProps) {
  const [currentItemIndex, setCurrentItemIndex] = useState<number>(0);
  const [showFinalView, setShowFinalView] = useState<boolean>(false);
  const [lastLikedProduct, setLastLikedProduct] =
    useState<ProductResult | null>(null);
  const [mergedImageUrl, setMergedImageUrl] = useState<string | null>(null);
  const [isMerging, setIsMerging] = useState<boolean>(false);

  const currentProduct = products[currentItemIndex];
  const isLastItem = currentItemIndex === products.length - 1;

  const handleMergeImages = useCallback(
    async (likedProduct: ProductResult): Promise<void> => {
      if (!uploadedImageUrl || !likedProduct.image_url) {
        console.error("Missing image URLs for merging");
        setShowFinalView(true);
        return;
      }

      setIsMerging(true);
      try {
        const result = await mergeImages({
          url1: likedProduct.image_url,
          url2: uploadedImageUrl,
        });

        const imageUrl =
          result.data.file.public_url ||
          (result.data.file.path
            ? `http://localhost:8000/${result.data.file.path}`
            : null);

        if (imageUrl) {
          setMergedImageUrl(imageUrl);
        }
      } catch (error) {
        console.error("Failed to merge images:", error);
      } finally {
        setIsMerging(false);
        setShowFinalView(true);
      }
    },
    [uploadedImageUrl]
  );

  const handleReject = useCallback((): void => {
    if (isLastItem) {
      if (lastLikedProduct) {
        handleMergeImages(lastLikedProduct);
      } else {
        setShowFinalView(true);
      }
    } else {
      setCurrentItemIndex((prev) => prev + 1);
    }
  }, [isLastItem, lastLikedProduct, handleMergeImages]);

  const handleAccept = useCallback((): void => {
    if (currentProduct) {
      setLastLikedProduct(currentProduct);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(currentProduct));

      if (isLastItem) {
        handleMergeImages(currentProduct);
      } else {
        setCurrentItemIndex((prev) => prev + 1);
      }
    }
  }, [currentProduct, isLastItem, handleMergeImages]);

  useEffect(() => {
    if (currentProduct && !currentProduct.image_url) {
      handleReject();
    }
  }, [currentProduct, handleReject]);

  if (isMerging || showFinalView) {
    return (
      <FinalProductView
        mergedImageUrl={mergedImageUrl || undefined}
        likedProduct={lastLikedProduct || undefined}
        isLoading={isMerging}
      />
    );
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
          initial={{ filter: ANIMATION.BLUR.MEDIUM, opacity: 0 }}
          animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
          transition={{
            duration: ANIMATION.DURATION.NORMAL,
            ease: ANIMATION.EASING.OUT,
          }}
          className="text-xs text-muted-foreground text-center mb-2"
        >
          {currentItemIndex + 1} of {products.length}
        </motion.div>

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
