import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Orb } from "@/components/ui/orb";
import { ItemSelectionView } from "./ItemSelectionView";

export function ProcessingView() {
  const [showItemSelection, setShowItemSelection] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowItemSelection(true);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  if (showItemSelection) {
    return <ItemSelectionView />;
  }
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6">
        <motion.div
          initial={{ filter: "blur(16px)", opacity: 0 }}
          animate={{ filter: "blur(0px)", opacity: 1 }}
          transition={{
            duration: 1.3,
            ease: "easeOut",
          }}
        >
          <Orb />
        </motion.div>
        <motion.p
          initial={{ filter: "blur(14px)", opacity: 0 }}
          animate={{ filter: "blur(0px)", opacity: 1 }}
          transition={{
            duration: 1.3,
            delay: 0.4,
            ease: "easeOut",
          }}
          className="text-muted-foreground text-xs text-center max-w-sm leading-relaxed"
        >
          Now you will converse with a real-time AI agent to understand your
          preferences, budget & other needs.
        </motion.p>
      </div>
    </div>
  );
}
