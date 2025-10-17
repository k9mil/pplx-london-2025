import { motion } from "framer-motion";
import { useState } from "react";
import { X, Check } from "lucide-react";
import { FinalProductView } from "./FinalProductView";

export function ItemSelectionView() {
  const [currentItem, setCurrentItem] = useState<"item1" | "item2">("item1");
  const [showFinalView, setShowFinalView] = useState(false);

  const handleReject = () => {
    if (currentItem === "item1") {
      setCurrentItem("item2");
    } else if (currentItem === "item2") {
      setShowFinalView(true);
    }
  };

  const handleAccept = () => {
    if (currentItem === "item1") {
      setCurrentItem("item2");
    } else if (currentItem === "item2") {
      setShowFinalView(true);
    }
  };

  const imageSrc = currentItem === "item1" ? "/item_1.jpg" : "/item_2.jpg";

  if (showFinalView) {
    return <FinalProductView />;
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <div className="flex flex-col items-center gap-8">
        <motion.div
          key={currentItem}
          initial={{ filter: "blur(20px)", opacity: 0 }}
          animate={{ filter: "blur(0px)", opacity: 1 }}
          transition={{
            duration: 1.4,
            ease: "easeOut",
          }}
          className="relative"
        >
          <img
            src={imageSrc}
            alt={`Item ${currentItem === "item1" ? "1" : "2"}`}
            className="max-w-2xl max-h-[32rem] object-contain rounded-lg"
          />
        </motion.div>

        <div className="flex gap-6">
          <motion.button
            initial={{ filter: "blur(16px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{ delay: 0.6, duration: 1.2, ease: "easeOut" }}
            onClick={handleReject}
            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:border-red-200 transition-colors"
          >
            <X className="w-4 h-4 text-gray-600" />
          </motion.button>

          <motion.button
            initial={{ filter: "blur(16px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{ delay: 0.6, duration: 1.2, ease: "easeOut" }}
            onClick={handleAccept}
            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:border-green-200 transition-colors"
          >
            <Check className="w-4 h-4 text-gray-600" />
          </motion.button>
        </div>
      </div>
    </div>
  );
}
