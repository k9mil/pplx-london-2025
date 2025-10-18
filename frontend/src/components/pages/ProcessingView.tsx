import { motion } from "framer-motion";
import { useState, useEffect, useCallback } from "react";
import { useConversation } from "@elevenlabs/react";
import { Orb, AgentState } from "@/components/ui/orb";
import { ItemSelectionView } from "./ItemSelectionView";
import { Mic, MicOff, PhoneOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ANIMATION, ERRORS, UI } from "@/constants";
import { generalSearch } from "@/services/api";
import type { ImageDescription, ProductResult } from "@/types";

interface ProcessingViewProps {
  imageDescriptions?: ImageDescription[];
}

export function ProcessingView({
  imageDescriptions = [],
}: ProcessingViewProps) {
  const [showItemSelection, setShowItemSelection] = useState<boolean>(false);
  const [conversationStarted, setConversationStarted] =
    useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [micMuted, setMicMuted] = useState<boolean>(false);
  const [mediaStream, setMediaStream] = useState<MediaStream | null>(null);
  const [products, setProducts] = useState<ProductResult[]>([]);
  const [isLoadingProducts, setIsLoadingProducts] = useState<boolean>(false);

  const conversation = useConversation({ micMuted });
  const { status, isSpeaking } = conversation;

  const getAgentState = useCallback((): AgentState => {
    if (status === UI.STATUS.DISCONNECTED || !conversationStarted) {
      return null;
    }
    return isSpeaking ? "talking" : "listening";
  }, [status, conversationStarted, isSpeaking]);

  const handleError = useCallback((err: Error): void => {
    console.error("Failed to start conversation:", err);

    if (err.name === ERRORS.NOT_ALLOWED) {
      setError(ERRORS.MICROPHONE_ACCESS_DENIED);
    } else if (err.name === ERRORS.NOT_FOUND) {
      setError(ERRORS.MICROPHONE_NOT_FOUND);
    } else {
      setError(ERRORS.CONVERSATION_FAILED);
    }
  }, []);

  const initConversation = useCallback(async (): Promise<void> => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setMediaStream(stream);

      const agentId = import.meta.env.VITE_ELEVENLABS_AGENT_ID;
      if (!agentId) {
        throw new Error("Missing VITE_ELEVENLABS_AGENT_ID");
      }

      await conversation.startSession({ agentId } as any);

      if (imageDescriptions.length > 0) {
        let contextMessage = "The user has uploaded the following images:\n\n";
        imageDescriptions.forEach((img, index) => {
          contextMessage += `Image ${index + 1} (${img.filename}):\n${
            img.description
          }\n\n`;
        });
        contextMessage +=
          "Use this information to understand the user's preferences and needs.";

        conversation.sendContextualUpdate(contextMessage);
      }

      setConversationStarted(true);
    } catch (err) {
      if (err instanceof Error) {
        handleError(err);
      }
    }
  }, [conversation, handleError, imageDescriptions]);

  useEffect(() => {
    initConversation();

    return () => {
      if (conversationStarted) {
        conversation.endSession();
      }
      mediaStream?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  const fetchProducts = useCallback(async (): Promise<void> => {
    setIsLoadingProducts(true);
    try {
      const results = await generalSearch(
        {
          budget_range: [500, 1500],
          essential_features: [],
          type: "sofa",
        },
        10
      );
      setProducts(results);
      setShowItemSelection(true);
    } catch (err) {
      console.error("Failed to fetch products:", err);
      setError("Failed to load products. Please try again.");
    } finally {
      setIsLoadingProducts(false);
    }
  }, []);

  useEffect(() => {
    if (status === UI.STATUS.DISCONNECTED && conversationStarted) {
      fetchProducts();
    }
  }, [status, conversationStarted, fetchProducts]);

  const handleMuteToggle = useCallback((): void => {
    setMicMuted((prev) => !prev);
  }, []);

  const handleEndConversation = useCallback(async (): Promise<void> => {
    try {
      await conversation.endSession();
      await fetchProducts();
    } catch (err) {
      console.error("Failed to end conversation:", err);
    }
  }, [conversation, fetchProducts]);

  if (showItemSelection) {
    return <ItemSelectionView products={products} />;
  }

  const isConnected = status === UI.STATUS.CONNECTED;

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6">
        <motion.div
          initial={{ filter: ANIMATION.BLUR.LARGE, opacity: 0 }}
          animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
          transition={{
            duration: ANIMATION.DURATION.NORMAL,
            ease: ANIMATION.EASING.OUT,
          }}
          className="w-64 h-64"
        >
          <Orb agentState={getAgentState()} />
        </motion.div>

        <motion.p
          initial={{ filter: ANIMATION.BLUR.MEDIUM, opacity: 0 }}
          animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
          transition={{
            duration: ANIMATION.DURATION.NORMAL,
            delay: ANIMATION.DELAY.MEDIUM,
            ease: ANIMATION.EASING.OUT,
          }}
          className="text-muted-foreground text-xs text-center max-w-sm leading-relaxed"
        >
          {error ? (
            <span className="text-red-500">{error}</span>
          ) : isLoadingProducts ? (
            "Loading products..."
          ) : (
            UI.TEXT.AGENT_CONVERSATION
          )}
        </motion.p>

        {!error && (
          <motion.div
            initial={{ filter: ANIMATION.BLUR.MEDIUM, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              duration: ANIMATION.DURATION.NORMAL,
              delay: ANIMATION.DELAY.LONG,
              ease: ANIMATION.EASING.OUT,
            }}
            className="flex gap-3 items-center"
          >
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <div
                className={`w-2 h-2 rounded-full ${
                  isConnected ? "bg-green-500" : "bg-red-500"
                }`}
              />
              <span>
                {isConnected ? UI.LABELS.CONNECTED : UI.LABELS.CONNECTING}
              </span>
            </div>

            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleMuteToggle}
              title={micMuted ? UI.LABELS.UNMUTE : UI.LABELS.MUTE}
              disabled={!isConnected}
            >
              {micMuted ? (
                <MicOff className="h-4 w-4" />
              ) : (
                <Mic className="h-4 w-4" />
              )}
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleEndConversation}
              title={UI.LABELS.END_CONVERSATION}
              disabled={!isConnected}
            >
              <PhoneOff className="h-4 w-4" />
            </Button>
          </motion.div>
        )}

        {error && (
          <motion.div
            initial={{ filter: ANIMATION.BLUR.MEDIUM, opacity: 0 }}
            animate={{ filter: ANIMATION.BLUR.NONE, opacity: 1 }}
            transition={{
              duration: ANIMATION.DURATION.NORMAL,
              delay: ANIMATION.DELAY.LONG,
              ease: ANIMATION.EASING.OUT,
            }}
          >
            <Button
              variant="outline"
              size="sm"
              onClick={() => window.location.reload()}
            >
              {UI.LABELS.RETRY}
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
