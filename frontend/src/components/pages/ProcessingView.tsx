import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useConversation } from "@elevenlabs/react";
import { Orb, AgentState } from "@/components/ui/orb";
import { ItemSelectionView } from "./ItemSelectionView";
import { Mic, MicOff, PhoneOff } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ProcessingView() {
  const [showItemSelection, setShowItemSelection] = useState(false);
  const [conversationStarted, setConversationStarted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);

  const conversation = useConversation();
  const { status, isSpeaking } = conversation;

  // Map ElevenLabs conversation state to Orb agent state
  const getAgentState = (): AgentState => {
    if (status === "disconnected" || !conversationStarted) {
      return null;
    }
    if (isSpeaking) {
      return "talking";
    }
    return "listening";
  };

  useEffect(() => {
    const initConversation = async () => {
      try {
        // Request microphone permissions
        await navigator.mediaDevices.getUserMedia({ audio: true });

        // Start ElevenLabs session
        await conversation.startSession({
          agentId: import.meta.env.VITE_ELEVENLABS_AGENT_ID,
        });

        setConversationStarted(true);
      } catch (err) {
        console.error("Failed to start conversation:", err);
        if (err instanceof Error) {
          if (err.name === "NotAllowedError") {
            setError("Microphone access denied. Please enable it to continue.");
          } else if (err.name === "NotFoundError") {
            setError("No microphone found. Please connect a microphone.");
          } else {
            setError("Failed to start conversation. Please try again.");
          }
        }
      }
    };

    initConversation();

    // Cleanup: end session when component unmounts
    return () => {
      if (conversationStarted) {
        conversation.endSession();
      }
    };
  }, []);

  // Monitor conversation status to detect when it ends
  useEffect(() => {
    if (status === "disconnected" && conversationStarted) {
      // Conversation has ended, transition to item selection
      setShowItemSelection(true);
    }
  }, [status, conversationStarted]);

  const handleMuteToggle = () => {
    setIsMuted(!isMuted);
    // Note: ElevenLabs SDK doesn't have a built-in mute method
    // This would require additional audio track management
  };

  const handleEndConversation = async () => {
    try {
      await conversation.endSession();
      setShowItemSelection(true);
    } catch (err) {
      console.error("Failed to end conversation:", err);
    }
  };

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
          className="w-64 h-64"
        >
          <Orb agentState={getAgentState()} />
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
          {error ? (
            <span className="text-red-500">{error}</span>
          ) : status === "connected" ? (
            "Now you are conversing with a real-time AI agent to understand your preferences, budget & other needs."
          ) : (
            "Connecting to AI agent..."
          )}
        </motion.p>

        {/* Connection status and controls */}
        {conversationStarted && !error && (
          <motion.div
            initial={{ filter: "blur(14px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{
              duration: 1.3,
              delay: 0.6,
              ease: "easeOut",
            }}
            className="flex gap-3 items-center"
          >
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <div
                className={`w-2 h-2 rounded-full ${
                  status === "connected" ? "bg-green-500" : "bg-gray-300"
                }`}
              />
              <span>{status === "connected" ? "Connected" : "Connecting..."}</span>
            </div>

            {status === "connected" && (
              <>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8"
                  onClick={handleMuteToggle}
                  title={isMuted ? "Unmute" : "Mute"}
                >
                  {isMuted ? (
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
                  title="End conversation"
                >
                  <PhoneOff className="h-4 w-4" />
                </Button>
              </>
            )}
          </motion.div>
        )}

        {/* Retry button if there's an error */}
        {error && (
          <motion.div
            initial={{ filter: "blur(14px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            transition={{
              duration: 1.3,
              delay: 0.6,
              ease: "easeOut",
            }}
          >
            <Button
              variant="outline"
              size="sm"
              onClick={() => window.location.reload()}
            >
              Retry
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
