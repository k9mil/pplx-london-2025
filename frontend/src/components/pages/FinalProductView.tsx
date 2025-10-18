import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Skeleton } from "@/components/ui/skeleton";
import { ANIMATION, UI } from "@/constants";
import type { ProductResult } from "@/types";

interface FinalProductViewProps {
  mergedImageUrl?: string;
  likedProduct?: ProductResult;
  isLoading?: boolean;
}

export function FinalProductView({
  mergedImageUrl,
  likedProduct,
  isLoading = false,
}: FinalProductViewProps) {
  if (isLoading) {
    return (
      <div className="min-h-screen bg-white relative overflow-hidden flex items-center justify-center p-8">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage: "url('/gradient.svg')",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
          }}
        />
        <div className="relative z-10 w-full max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
            <div className="flex justify-center">
              <Skeleton className="w-full max-w-lg h-96 rounded-lg" />
            </div>

            <div className="space-y-6">
              <Skeleton className="h-10 w-3/4" />

              <div className="space-y-4">
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
              </div>

              <Skeleton className="h-10 w-32 mt-6" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!mergedImageUrl || !likedProduct) {
    return (
      <div className="min-h-screen bg-white relative overflow-hidden flex items-center justify-center p-8">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage: "url('/gradient.svg')",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
          }}
        />
        <p className="relative z-10 text-muted-foreground">
          No product selected
        </p>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-white relative overflow-hidden flex items-center justify-center p-8">
      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: "url('/gradient.svg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      />
      <div className="relative z-10 w-full max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <motion.div
            initial={{ filter: ANIMATION.BLUR.EXTRA_LARGE, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              duration: ANIMATION.DURATION.SLOW,
              ease: ANIMATION.EASING.OUT,
            }}
            className="flex justify-center"
          >
            <img
              src={mergedImageUrl}
              alt={likedProduct.name}
              className="max-w-lg max-h-96 object-contain rounded-lg"
            />
          </motion.div>

          <motion.div
            initial={{ filter: ANIMATION.BLUR.LARGE, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              duration: ANIMATION.DURATION.SLOW,
              delay: ANIMATION.DELAY.SHORT,
              ease: ANIMATION.EASING.OUT,
            }}
            className="space-y-6"
          >
            <h1 className="text-3xl font-light text-gray-900">
              {likedProduct.name}
            </h1>

            <Accordion
              type="single"
              collapsible
              defaultValue="product-info"
              className="w-full"
            >
              <AccordionItem value="product-info">
                <AccordionTrigger>Product Information</AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-2 text-gray-600">
                    <p>{likedProduct.description}</p>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="price">
                <AccordionTrigger>Price & Availability</AccordionTrigger>
                <AccordionContent>
                  <p className="text-gray-600">
                    The {likedProduct.name} costs £{likedProduct.price} and is
                    currently available.
                  </p>
                </AccordionContent>
              </AccordionItem>
            </Accordion>

            <motion.div
              initial={{ filter: ANIMATION.BLUR.MEDIUM, opacity: 0 }}
              animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
              transition={{
                duration: ANIMATION.DURATION.SLOW,
                delay: ANIMATION.DELAY.MEDIUM,
                ease: ANIMATION.EASING.OUT,
              }}
              className="mt-6"
            >
              <Button variant="outline" size="sm" className="w-fit" asChild>
                <a
                  href={likedProduct.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {UI.LABELS.PURCHASE}
                </a>
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
