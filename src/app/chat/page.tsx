"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import styles from "./page.module.css";
import { sendChatMessage, getRecommendations, type UserPreferences, type RecommendationItem } from "@/lib/api";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [preferences, setPreferences] = useState<UserPreferences>({});
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Initialize chat with first message from backend
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;
    
    const initChat = async () => {
      try {
        setIsLoading(true);
        const response = await sendChatMessage([]);
        
        const aiMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: response.message.content,
        };
        
        setMessages([aiMessage]);
        if (response.updated_preferences) {
          setPreferences(response.updated_preferences);
        }
        setError(null); // Clear any previous errors
      } catch (err) {
        console.error("Failed to initialize chat:", err);
        setError("Failed to connect to backend. Make sure the API is running on http://localhost:8000");
        // Fallback message
        setMessages([{
          id: "1",
          role: "assistant",
          content: "Hi! I'm here to help you find your perfect gaming mouse. Let's start with a few questions. What's your hand size? (exact dimensions or small/medium/large)",
        }]);
      } finally {
        setIsLoading(false);
      }
    };
    
    initChat();
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading]);

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
    setError(null);

    try {
      // Send to backend API
      const apiMessages = [...messages, userMessage].map(msg => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await sendChatMessage(apiMessages, preferences);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message.content,
      };
      
      setMessages((prev) => [...prev, aiMessage]);
      
      // Update preferences
      if (response.updated_preferences) {
        setPreferences(response.updated_preferences);
      }
      
      // Check if ready for recommendations
      if (response.ready_for_recommendation && !showRecommendations) {
        // Fetch recommendations
        const recsResponse = await getRecommendations(response.updated_preferences || preferences);
        setRecommendations(recsResponse.recommendations);
        setShowRecommendations(true);
      }
    } catch (err) {
      setError("Failed to get response. Please try again.");
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

  return (
    <div className={styles.chatContainer}>
      {/* Header */}
      <div className={styles.header}>
        <div className={`container mx-auto ${styles.headerContent}`}>
          <Link href="/" className={styles.logo}>
            <span>periph4all</span>
          </Link>
          <Badge variant="secondary">AI Chat</Badge>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="container mx-auto px-4 py-8">
        <div className="mx-auto max-w-4xl grid md:grid-cols-3 gap-6">
          {/* Chat Interface - 2/3 width */}
          <Card className={`md:col-span-2 ${styles.chatCard}`}>
            <CardHeader>
              <CardTitle>Find Your Perfect Mouse</CardTitle>
              <CardDescription>
                Answer a few questions to get personalized recommendations
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-0">
              {/* Messages */}
              <ScrollArea className={styles.messageArea}>
                <div className={styles.messagesContainer}>
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`${styles.messageRow} ${
                        message.role === "user" ? styles.messageRowUser : styles.messageRowAssistant
                      }`}
                    >
                      {message.role === "assistant" && (
                        <Avatar className="h-8 w-8">
                          <AvatarFallback>AI</AvatarFallback>
                        </Avatar>
                      )}
                      <div
                        className={`${styles.messageBubble} ${
                          message.role === "user"
                            ? styles.messageBubbleUser
                            : styles.messageBubbleAssistant
                        }`}
                      >
                        <p className="text-sm">{message.content}</p>
                      </div>
                      {message.role === "user" && (
                        <Avatar className="h-8 w-8">
                          <AvatarFallback>You</AvatarFallback>
                        </Avatar>
                      )}
                    </div>
                  ))}
                  {isLoading && (
                    <div className={`${styles.messageRow} ${styles.messageRowAssistant}`}>
                      <Avatar className="h-8 w-8">
                        <AvatarFallback>AI</AvatarFallback>
                      </Avatar>
                      <div className={`${styles.messageBubble} ${styles.messageBubbleAssistant}`}>
                        <div className={styles.typingIndicator}>
                          <div className={styles.typingDot} />
                          <div className={styles.typingDot} />
                          <div className={styles.typingDot} />
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={scrollRef} />
                </div>
              </ScrollArea>

              {/* Input Area */}
              <div className={styles.inputArea}>
                <div className={styles.inputWrapper}>
                  <Input
                    placeholder="Type your answer..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                  />
                  <Button onClick={handleSend} disabled={isLoading || !input.trim()}>
                    Send
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Info Sidebar - 1/3 width */}
          <div className="space-y-6">
            {/* Error Display */}
            {error && (
              <Card className={`${styles.sidebarCard} border-destructive`}>
                <CardHeader>
                  <CardTitle className="text-lg text-destructive">Connection Error</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{error}</p>
                </CardContent>
              </Card>
            )}

            {/* Extracted Preferences */}
            <Card className={styles.sidebarCard}>
              <CardHeader>
                <CardTitle className="text-lg">Your Preferences</CardTitle>
              </CardHeader>
              <CardContent className={styles.infoList}>
                {preferences.hand_size && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Hand Size: <span className="text-primary">{preferences.hand_size}</span></p>
                  </div>
                )}
                {preferences.grip_type && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Grip: <span className="text-primary">{preferences.grip_type}</span></p>
                  </div>
                )}
                {preferences.genre && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Genre: <span className="text-primary">{preferences.genre.toUpperCase()}</span></p>
                  </div>
                )}
                {preferences.weight_preference && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Weight: <span className="text-primary">{preferences.weight_preference}</span></p>
                  </div>
                )}
                {(preferences.budget_min || preferences.budget_max) && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Budget: <span className="text-primary">
                      {preferences.budget_min ? `$${preferences.budget_min}` : '$0'} - 
                      {preferences.budget_max ? ` $${preferences.budget_max}` : ' Any'}
                    </span></p>
                  </div>
                )}
                {preferences.wireless_preference !== undefined && preferences.wireless_preference !== null && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Connection: <span className="text-primary">
                      {preferences.wireless_preference ? 'Wireless' : 'Wired'}
                    </span></p>
                  </div>
                )}
                {preferences.sensitivity && (
                  <div className={styles.infoItem}>
                    <div className={`${styles.infoDot} ${styles.infoDotActive}`} />
                    <p className="text-sm">Sensitivity: <span className="text-primary">{preferences.sensitivity}</span></p>
                  </div>
                )}
                {Object.keys(preferences).length === 0 && (
                  <p className="text-sm text-muted-foreground">No preferences collected yet...</p>
                )}
              </CardContent>
            </Card>

            <Card className={styles.sidebarCard}>
              <CardHeader>
                <CardTitle className="text-lg">What Happens Next?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-muted-foreground">
                <p>
                  After collecting your preferences, our AI will:
                </p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Convert your inputs to vectors</li>
                  <li>Compare against 175 mice</li>
                  <li>Show your top 3 matches</li>
                  <li>Explain why they fit you</li>
                </ul>
              </CardContent>
            </Card>

            <Card className={styles.sidebarCard}>
              <CardHeader>
                <CardTitle className="text-lg">Pro Tip</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Be specific about your preferences! The more details you provide, the better your recommendations will be.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Recommendations Section */}
        {showRecommendations && recommendations.length > 0 && (
          <div className="mx-auto max-w-6xl mt-12">
            <div className="mb-6">
              <h2 className="text-3xl font-bold mb-2">Your Top Matches</h2>
              <p className="text-muted-foreground">Based on your preferences, here are the best mice for you:</p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-6">
              {recommendations.map((rec, index) => (
                <Card key={index} className={`${styles.recommendationCard} relative overflow-hidden`}>
                  <div className="absolute top-4 right-4">
                    <Badge variant="secondary" className="text-lg font-bold">
                      #{index + 1}
                    </Badge>
                  </div>
                  
                  <CardHeader>
                    <CardTitle className="text-xl">{rec.mouse.name}</CardTitle>
                    <CardDescription className="text-base">
                      by {rec.mouse.brand}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    {/* Mouse Stats */}
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      {rec.mouse.price && (
                        <div>
                          <p className="text-muted-foreground">Price</p>
                          <p className="font-semibold text-primary text-lg">${rec.mouse.price}</p>
                        </div>
                      )}
                      {rec.mouse.weight && (
                        <div>
                          <p className="text-muted-foreground">Weight</p>
                          <p className="font-semibold">{rec.mouse.weight}g</p>
                        </div>
                      )}
                      {rec.mouse.wireless !== undefined && rec.mouse.wireless !== null && (
                        <div>
                          <p className="text-muted-foreground">Connection</p>
                          <p className="font-semibold">{rec.mouse.wireless ? 'Wireless' : 'Wired'}</p>
                        </div>
                      )}
                      {rec.mouse.dpi_max && (
                        <div>
                          <p className="text-muted-foreground">Max DPI</p>
                          <p className="font-semibold">{rec.mouse.dpi_max.toLocaleString()}</p>
                        </div>
                      )}
                      {rec.mouse.shape && (
                        <div className="col-span-2">
                          <p className="text-muted-foreground">Shape</p>
                          <p className="font-semibold">{rec.mouse.shape}</p>
                        </div>
                      )}
                      {rec.mouse.sensor && (
                        <div className="col-span-2">
                          <p className="text-muted-foreground">Sensor</p>
                          <p className="font-semibold text-xs">{rec.mouse.sensor}</p>
                        </div>
                      )}
                    </div>

                    {/* Match Score */}
                    <div className="pt-4 border-t">
                      <div className="flex items-center justify-between mb-2">
                        <p className="text-sm text-muted-foreground">Match Score</p>
                        <p className="text-lg font-bold text-primary">{(rec.score * 100).toFixed(0)}%</p>
                      </div>
                      <div className="w-full bg-secondary rounded-full h-2">
                        <div 
                          className="bg-primary h-2 rounded-full transition-all duration-500"
                          style={{ width: `${rec.score * 100}%` }}
                        />
                      </div>
                    </div>

                    {/* Reasoning */}
                    <div className="pt-4 border-t">
                      <p className="text-sm text-muted-foreground mb-2">Why this mouse?</p>
                      <p className="text-sm">{rec.reasoning}</p>
                    </div>

                    {/* Buy Button */}
                    {rec.mouse.url && (
                      <div className="pt-4">
                        <Button asChild className="w-full">
                          <a href={rec.mouse.url} target="_blank" rel="noopener noreferrer">
                            View on Amazon →
                          </a>
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Refine Preferences Button */}
            <div className="mt-8 text-center">
              <Button 
                variant="outline" 
                size="lg"
                onClick={() => {
                  setShowRecommendations(false);
                  setRecommendations([]);
                }}
              >
                Refine Preferences
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

