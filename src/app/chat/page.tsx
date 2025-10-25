"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import styles from "./page.module.css";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hi! I'm here to help you find your perfect gaming mouse. Let's start with a few questions. What size are your hands? (Small, Medium, or Large)",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate AI response (replace with actual API call later)
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Got it! Next question: What's your preferred grip style? (Palm, Claw, or Fingertip)",
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1000);
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
            <Card className={styles.sidebarCard}>
              <CardHeader>
                <CardTitle className="text-lg">Questions We&apos;ll Ask</CardTitle>
              </CardHeader>
              <CardContent className={styles.infoList}>
                <div className={styles.infoItem}>
                  <div className={styles.infoDot} />
                  <p className="text-sm text-muted-foreground">Hand size</p>
                </div>
                <div className={styles.infoItem}>
                  <div className={styles.infoDot} />
                  <p className="text-sm text-muted-foreground">Grip style</p>
                </div>
                <div className={styles.infoItem}>
                  <div className={styles.infoDot} />
                  <p className="text-sm text-muted-foreground">Games you play</p>
                </div>
                <div className={styles.infoItem}>
                  <div className={styles.infoDot} />
                  <p className="text-sm text-muted-foreground">Weight preference</p>
                </div>
                <div className={styles.infoItem}>
                  <div className={styles.infoDot} />
                  <p className="text-sm text-muted-foreground">Budget range</p>
                </div>
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
      </div>
    </div>
  );
}

