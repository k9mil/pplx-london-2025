import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export function FinalProductView() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-8">
      <div className="w-full max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Left side - Product Image */}
          <motion.div
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{
              duration: 1.4,
              ease: "easeOut",
            }}
            className="flex justify-center"
          >
            <img
              src="/item_3.jpg"
              alt="HEMNES Coffee Table"
              className="max-w-lg max-h-96 object-contain rounded-lg"
            />
          </motion.div>

          {/* Right side - Product Information */}
          <motion.div
            initial={{ filter: "blur(16px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{
              duration: 1.4,
              delay: 0.2,
              ease: "easeOut",
            }}
            className="space-y-6"
          >
            <h1 className="text-3xl font-light text-gray-900">
              HEMNES Coffee Table
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
                    <p>
                      This premium product combines cutting-edge technology with
                      elegant design. Crafted with attention to detail and built
                      to last.
                    </p>
                    <ul className="list-disc list-inside space-y-1 mt-3">
                      <li>High-quality materials and construction</li>
                      <li>Advanced performance features</li>
                      <li>User-friendly interface and controls</li>
                      <li>Comprehensive warranty and support</li>
                    </ul>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="price">
                <AccordionTrigger>Price & Availability</AccordionTrigger>
                <AccordionContent>
                  <p className="text-gray-600">
                    The HEMNES coffee table costs £299.99 including shipping and
                    is currently in stock.
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
                        47 1/4" x 27 1/2" x 16 7/8"
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Weight:</span>
                      <span className="font-semibold">77 lbs</span>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>

            <motion.div
              initial={{ filter: "blur(14px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              transition={{
                duration: 1.4,
                delay: 0.4,
                ease: "easeOut",
              }}
              className="mt-6"
            >
              <Button variant="outline" size="sm" className="w-fit" asChild>
                <a
                  href="https://www.ikea.com"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Purchase
                </a>
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
