"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { RecommendationCard } from "@/components/RecommendationCard";
import { UMAPVisualization } from "@/components/UMAPVisualization";
import { ForceGraphVisualization } from "@/components/ForceGraphVisualization";
import { Sparkles, ArrowLeft, BarChart3, Network } from "lucide-react";
import type { RecommendationItem, UserPreferences } from "@/lib/api";

export default function ResultsPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [data, setData] = useState<{ recommendations: RecommendationItem[]; preferences: UserPreferences } | null>(null);
  
  const recommendations = data?.recommendations || [];
  const preferences = data?.preferences || {};

  useEffect(() => {
    setMounted(true);
    
    const storedRecs = sessionStorage.getItem("recommendations");
    const storedPrefs = sessionStorage.getItem("preferences");

    if (!storedRecs) {
      router.push("/chat");
      return;
    }

    try {
      const parsedRecs = JSON.parse(storedRecs);
      const parsedPrefs = storedPrefs ? JSON.parse(storedPrefs) : {};
      setData({ recommendations: parsedRecs, preferences: parsedPrefs });
    } catch (error) {
      console.error("Failed to parse stored data:", error);
      router.push("/chat");
    }
  }, [router]);

  if (!mounted || !data) {
    return (
      <div className="min-h-screen bg-gradient-animated flex items-center justify-center">
        <div className="flex items-center gap-3">
          <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-animated">
      {/* Header */}
      <div className="border-b border-border/50 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <Sparkles className="w-5 h-5 text-primary transition-transform group-hover:rotate-12" />
            <span className="text-xl font-bold text-gradient">periph4all</span>
          </Link>
          <Badge variant="secondary" className="glass">Your Results</Badge>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12 max-w-7xl space-y-16">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-6xl font-bold text-gradient">
            Your Perfect Matches
          </h1>
          <p className="text-muted-foreground text-xl max-w-2xl mx-auto">
            Based on your preferences, we&apos;ve found these top gaming mice tailored just for you
          </p>
        </div>

        {/* Recommendations Grid */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-3xl font-bold">Top 3 Recommendations</h2>
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push("/chat")}
              className="glass hover:bg-primary/10 hover:border-primary/50"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Chat
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {recommendations.map((rec: RecommendationItem, index: number) => (
              <RecommendationCard
                key={index}
                recommendation={rec}
                index={index}
              />
            ))}
          </div>
        </section>

        {/* UMAP Visualization Section */}
        <section className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-8 h-8 text-primary" />
              <h2 className="text-3xl font-bold">Embedding Space Visualization</h2>
            </div>
            <p className="text-muted-foreground text-lg">
              See how your preferences compare to all available mice in our database
            </p>
          </div>

          {/* Visualization Container */}
          <UMAPVisualization preferences={preferences} />
        </section>

        {/* Force Graph Visualization Section */}
        <section className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <Network className="w-8 h-8 text-primary" />
              <h2 className="text-3xl font-bold">Force-Directed Graph</h2>
            </div>
            <p className="text-muted-foreground text-lg">
              Interactive network showing relationships between similar mice
            </p>
          </div>

          {/* Force Graph */}
          <ForceGraphVisualization preferences={preferences} />
        </section>

        {/* Actions */}
        <div className="flex justify-center gap-4">
          <Button
            variant="outline"
            size="lg"
            onClick={() => {
              sessionStorage.removeItem("recommendations");
              sessionStorage.removeItem("preferences");
              router.push("/chat");
            }}
            className="glass hover:bg-primary/10 hover:border-primary/50"
          >
            Start New Search
          </Button>
        </div>
      </div>
    </div>
  );
}

