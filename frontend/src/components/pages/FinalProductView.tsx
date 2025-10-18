import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ANIMATION, IMAGES, ALT_TEXT, UI } from "@/constants";

const PRODUCT_INFO = {
  NAME: "HEMNES Coffee Table",
  PRICE: "£299.99",
  DIMENSIONS: '47 1/4" x 27 1/2" x 16 7/8"',
  WEIGHT: "77 lbs",
  PURCHASE_URL: "https://www.ikea.com",
  DESCRIPTION:
    "This premium product combines cutting-edge technology with elegant design. Crafted with attention to detail and built to last.",
  FEATURES: [
    "High-quality materials and construction",
    "Advanced performance features",
    "User-friendly interface and controls",
    "Comprehensive warranty and support",
  ],
} as const;

export function FinalProductView() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-8">
      <div className="w-full max-w-6xl">
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
              src={IMAGES.BEDROOM_THREE}
              alt={ALT_TEXT.BEDROOM_THREE}
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
              {PRODUCT_INFO.NAME}
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
                    <p>{PRODUCT_INFO.DESCRIPTION}</p>
                    <ul className="list-disc list-inside space-y-1 mt-3">
                      {PRODUCT_INFO.FEATURES.map((feature) => (
                        <li key={feature}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="price">
                <AccordionTrigger>Price & Availability</AccordionTrigger>
                <AccordionContent>
                  <p className="text-gray-600">
                    The {PRODUCT_INFO.NAME} costs {PRODUCT_INFO.PRICE} including
                    shipping and is currently in stock.
                  </p>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="specifications">
                <AccordionTrigger>Specifications</AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-2 text-gray-600">
                    <div className="flex justify-between items-center">
                      <span>Dimensions:</span>
                      <span className="font-semibold">
                        {PRODUCT_INFO.DIMENSIONS}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Weight:</span>
                      <span className="font-semibold">
                        {PRODUCT_INFO.WEIGHT}
                      </span>
                    </div>
                  </div>
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
                  href={PRODUCT_INFO.PURCHASE_URL}
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
