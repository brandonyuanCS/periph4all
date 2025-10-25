"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Sparkles, ArrowRight } from "lucide-react";
import { sendChatMessage, getRecommendations, type UserPreferences, type RecommendationItem } from "@/lib/api";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const [preferences, setPreferences] = useState<UserPreferences>({});
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [showResultsButton, setShowResultsButton] = useState(false);
  const [quickSuggestions, setQuickSuggestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize chat
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const initChat = async () => {
      try {
        setIsLoading(true);
        const response = await sendChatMessage([]);
        
        // Simulate streaming effect
        await streamMessage(response.message.content);
        
        const aiMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: response.message.content,
        };
        
        setMessages([aiMessage]);
        if (response.updated_preferences) {
          setPreferences(response.updated_preferences);
        }
        
        const suggestions = getQuickSuggestionsForType(response.question_type);
        setQuickSuggestions(suggestions);
      } catch (err) {
        console.error("Failed to initialize chat:", err);
        const fallbackMsg = "Hi! I'm here to help you find your perfect gaming mouse. What's your hand size? (small, medium, or large)";
        await streamMessage(fallbackMsg);
        setMessages([{
          id: "1",
          role: "assistant",
          content: fallbackMsg,
        }]);
        setQuickSuggestions(['small', 'medium', 'large']);
      } finally {
        setIsLoading(false);
      }
    };
    
    initChat();
  }, []);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isStreaming, streamingText]);

  // Simulate streaming effect
  const streamMessage = async (text: string) => {
    setIsStreaming(true);
    setStreamingText("");
    
    const words = text.split(" ");
    for (let i = 0; i < words.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 30));
      setStreamingText(prev => prev + (i > 0 ? " " : "") + words[i]);
    }
    
    setIsStreaming(false);
    setStreamingText("");
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setQuickSuggestions([]);

    try {
      const apiMessages = [...messages, userMessage].map(msg => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await sendChatMessage(apiMessages, preferences);
      
      // Stream the response
      await streamMessage(response.message.content);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message.content,
      };
      
      setMessages((prev) => [...prev, aiMessage]);
      
      if (response.updated_preferences) {
        setPreferences(response.updated_preferences);
      }
      
      const suggestions = getQuickSuggestionsForType(response.question_type);
      setQuickSuggestions(suggestions);
      
      if (response.ready_for_recommendation && !showResultsButton) {
        const recsResponse = await getRecommendations(response.updated_preferences || preferences);
        setRecommendations(recsResponse.recommendations);
        setShowResultsButton(true);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickSuggestion = async (suggestion: string) => {
    if (isLoading) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: suggestion,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setQuickSuggestions([]);

    try {
      const apiMessages = [...messages, userMessage].map(msg => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await sendChatMessage(apiMessages, preferences);
      
      await streamMessage(response.message.content);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message.content,
      };
      
      setMessages((prev) => [...prev, aiMessage]);
      
      if (response.updated_preferences) {
        setPreferences(response.updated_preferences);
      }
      
      const newSuggestions = getQuickSuggestionsForType(response.question_type);
      setQuickSuggestions(newSuggestions);
      
      if (response.ready_for_recommendation && !showResultsButton) {
        const recsResponse = await getRecommendations(response.updated_preferences || preferences);
        setRecommendations(recsResponse.recommendations);
        setShowResultsButton(true);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const getQuickSuggestionsForType = (questionType: string | null | undefined): string[] => {
    if (!questionType) return [];
    
    const suggestionMap: Record<string, string[]> = {
      'hand_size': ['small', 'medium', 'large'],
      'grip_type': ['palm', 'claw', 'fingertip', 'hybrid'],
      'genre': ['fps', 'moba', 'mmo', 'battle royale', 'general'],
      'sensitivity': ['low', 'medium', 'high'],
      'weight_preference': ['light', 'medium', 'heavy'],
      'wireless_preference': ['wireless', 'wired'],
      'budget': [],
    };
    
    return suggestionMap[questionType] || [];
  };

  const handleViewResults = () => {
    // Store recommendations and preferences in sessionStorage
    sessionStorage.setItem("recommendations", JSON.stringify(recommendations));
    sessionStorage.setItem("preferences", JSON.stringify(preferences));
    
    // Navigate to results page
    router.push("/results");
  };

  return (
    <div className="min-h-screen bg-gradient-animated">
      {/* Minimalist Header */}
      <div className="border-b border-border/50 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <Sparkles className="w-5 h-5 text-primary transition-transform group-hover:rotate-12" />
            <span className="text-xl font-bold text-gradient">periph4all</span>
          </Link>
          <Badge variant="secondary" className="glass">AI Assistant</Badge>
        </div>
      </div>

      {/* Main Chat Container */}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex flex-col h-[calc(100vh-12rem)]">
          {/* Messages Area */}
          <ScrollArea className="flex-1 pr-4">
            <div className="space-y-8 pb-4">
              {messages.map((message) => (
                <div key={message.id} className="flex flex-col">
                  {message.role === "assistant" ? (
                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                        <span className="text-xs text-muted-foreground font-medium">AI Assistant</span>
                      </div>
                      <div className="text-2xl md:text-3xl font-bold leading-relaxed bg-gradient-to-r from-foreground/90 via-primary/80 to-foreground/90 bg-clip-text text-transparent animate-gradient">
                        {message.content}
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 justify-end">
                        <span className="text-xs text-muted-foreground font-medium">You</span>
                        <div className="w-2 h-2 rounded-full bg-foreground/60" />
                      </div>
                      <div className="text-xl md:text-2xl font-semibold text-right text-foreground/80">
                        {message.content}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {/* Streaming Message */}
              {isStreaming && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                    <span className="text-xs text-muted-foreground font-medium">AI Assistant</span>
                  </div>
                  <div className="text-2xl md:text-3xl font-bold leading-relaxed bg-gradient-to-r from-foreground/90 via-primary/80 to-foreground/90 bg-clip-text text-transparent">
                    {streamingText}
                    <span className="inline-block w-1 h-8 ml-1 bg-primary animate-pulse" />
                  </div>
                </div>
              )}
              
              {/* Loading Dots */}
              {isLoading && !isStreaming && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                    <span className="text-xs text-muted-foreground font-medium">AI Assistant</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-3 h-3 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-3 h-3 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Quick Suggestions - Above Input */}
          {quickSuggestions.length > 0 && !showResultsButton && (
            <div className="py-4 space-y-2">
              <p className="text-xs text-muted-foreground font-medium">Quick replies:</p>
              <div className="flex flex-wrap gap-2">
                {quickSuggestions.map((suggestion) => (
                  <Button
                    key={suggestion}
                    variant="outline"
                    size="sm"
                    onClick={() => handleQuickSuggestion(suggestion)}
                    disabled={isLoading}
                    className="glass hover:bg-primary/10 hover:border-primary/50 hover:scale-105 transition-all capitalize border-border/50"
                  >
                    {suggestion}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {/* Results Button */}
          {showResultsButton && (
            <div className="py-6 space-y-4">
              <div className="text-center space-y-3">
                <p className="text-sm text-muted-foreground">
                  ✨ Your personalized recommendations are ready!
                </p>
                <Button
                  onClick={handleViewResults}
                  size="lg"
                  className="bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-lg px-8 py-6 glow-md hover:scale-105 transition-all"
                >
                  View Your Results
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="pt-4 space-y-4">
            <div className="glass rounded-2xl p-2 flex items-center gap-2 focus-within:ring-2 focus-within:ring-primary/50 transition-all">
              <Input
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading || showResultsButton}
                className="border-0 bg-transparent text-lg focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-muted-foreground/50"
              />
              <Button 
                onClick={handleSend} 
                disabled={isLoading || !input.trim() || showResultsButton}
                size="icon"
                className="rounded-xl h-10 w-10 shrink-0 bg-primary hover:bg-primary/90 hover:scale-105 transition-all disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <style jsx global>{`
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        
        .animate-gradient {
          background-size: 200% auto;
          animation: gradient 3s linear infinite;
        }
      `}</style>
    </div>
  );
}