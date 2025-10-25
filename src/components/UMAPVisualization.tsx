"use client";

import { useState, useEffect } from "react";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getVisualizationWithUser, type UserPreferences, type EmbeddingPoint } from "@/lib/api";

interface UMAPVisualizationProps {
  preferences: UserPreferences;
}

export function UMAPVisualization({ preferences }: UMAPVisualizationProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mousePoints, setMousePoints] = useState<EmbeddingPoint[]>([]);
  const [userPoint, setUserPoint] = useState<EmbeddingPoint | null>(null);
  const [recommendedNames, setRecommendedNames] = useState<Set<string>>(new Set());
  
  // Use hardcoded colors based on your theme
  const colors = {
    foreground: 'hsl(0 0% 98%)',      // white-ish
    mutedForeground: 'hsl(0 0% 65%)', // gray
    primary: 'hsl(217 91% 60%)',      // blue
    border: 'hsl(0 0% 16%)',          // dark gray
    green: 'hsl(142 76% 55%)'         // green
  };

  useEffect(() => {
    const fetchVisualizationData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getVisualizationWithUser(preferences);
        
        console.log("Visualization data:", data); // Debug log
        console.log("Recommended points:", data.recommended_points); // Debug log
        
        setMousePoints(data.mouse_points);
        setUserPoint(data.user_point || null);
        
        // Create set of recommended mouse names for highlighting
        if (data.recommended_points) {
          // Normalize names: trim whitespace and convert to lowercase for comparison
          const names = new Set(data.recommended_points.map(p => p.mouse_name.trim().toLowerCase()));
          console.log("Recommended names set:", names); // Debug log
          console.log("Sample mouse point names:", data.mouse_points.slice(0, 5).map(p => p.mouse_name)); // Debug log
          setRecommendedNames(names);
        }
      } catch (err) {
        console.error("Failed to load visualization:", err);
        setError(err instanceof Error ? err.message : "Failed to load visualization");
      } finally {
        setIsLoading(false);
      }
    };

    fetchVisualizationData();
  }, [preferences]);

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: EmbeddingPoint }> }) => {
    if (active && payload && payload.length) {
      const point = payload[0].payload;
      const isUser = point.mouse_name === "Your Preferences";
      const isRecommended = recommendedNames.has(point.mouse_name);
      
      return (
        <Card className="glass p-3 border-border/50 shadow-lg">
          <div className="space-y-1">
            <p className="font-bold text-sm">{point.mouse_name}</p>
            {isUser && (
              <Badge className="text-xs bg-primary/20 text-primary border-primary/50">
                Your Preferences
              </Badge>
            )}
            {isRecommended && (
              <Badge className="text-xs bg-green-500/20 text-green-500 border-green-500/50">
                Recommended
              </Badge>
            )}
          </div>
        </Card>
      );
    }
    return null;
  };

  if (isLoading) {
    return (
      <Card className="glass border-border/50 p-8">
        <div className="flex items-center justify-center min-h-[600px]">
          <div className="flex items-center gap-3">
            <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-4 h-4 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="glass border-border/50 p-8">
        <div className="flex items-center justify-center min-h-[600px]">
          <div className="text-center space-y-2">
            <p className="text-red-500 font-semibold">Failed to Load Visualization</p>
            <p className="text-sm text-muted-foreground">{error}</p>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="glass border-border/50 p-6">
      <div className="space-y-4">
        {/* Technical Explanation */}
        <div className="text-center space-y-2 pb-2 border-b border-border/30">
          <p className="text-sm text-muted-foreground leading-relaxed max-w-4xl mx-auto">
            Each mouse is encoded into a <span className="text-primary font-semibold">384-dimensional vector</span> using the <span className="font-mono text-xs bg-muted px-1.5 py-0.5 rounded">all-MiniLM-L6-v2</span> transformer model. 
            <b className="text-foreground"> UMAP (Uniform Manifold Approximation and Projection)</b> reduces these high-dimensional embeddings to 2D while preserving local similarity structure. 
            Points closer together represent mice with more similar features and specifications.
          </p>
        </div>
        
        {/* Legend */}
        <div className="flex items-center justify-center gap-6 flex-wrap">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-foreground/40" />
            <span className="text-xs text-muted-foreground">All Mice ({mousePoints.length})</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-green-500 ring-2 ring-green-500/30" />
            <span className="text-xs text-green-500 font-medium">Recommended</span>
          </div>
          {userPoint && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-yellow-500 clip-star" />
              <span className="text-xs text-yellow-500 font-medium">Your Preferences</span>
            </div>
          )}
        </div>

        {/* Chart */}
        <ResponsiveContainer width="100%" height={600}>
          <ScatterChart
            margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
          >
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke={colors.border} 
              opacity={0.3} 
            />
            <XAxis 
              type="number" 
              dataKey="x" 
              name="UMAP 1"
              stroke={colors.mutedForeground}
              tick={{ fill: colors.mutedForeground, fontSize: 12 }}
              label={{ 
                value: 'UMAP Dimension 1', 
                position: 'insideBottom', 
                offset: -10,
                fill: colors.mutedForeground,
                fontSize: 12
              }}
            />
            <YAxis 
              type="number" 
              dataKey="y" 
              name="UMAP 2"
              stroke={colors.mutedForeground}
              tick={{ fill: colors.mutedForeground, fontSize: 12 }}
              label={{ 
                value: 'UMAP Dimension 2', 
                angle: -90, 
                position: 'insideLeft',
                fill: colors.mutedForeground,
                fontSize: 12
              }}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
            
            {/* All mice points */}
            <Scatter 
              name="Mice" 
              data={mousePoints} 
              fill={colors.foreground}
            >
              {mousePoints.map((point, index) => {
                // Normalize for comparison
                const normalizedName = point.mouse_name.trim().toLowerCase();
                const isRecommended = recommendedNames.has(normalizedName);
                
                if (index < 5 || isRecommended) {
                  console.log(`Point ${index}: "${point.mouse_name}" (normalized: "${normalizedName}"), isRecommended: ${isRecommended}`);
                }
                
                return (
                  <Cell 
                    key={`cell-${index}`}
                    fill={isRecommended ? colors.green : colors.foreground}
                    fillOpacity={isRecommended ? 1 : 0.3}
                    r={isRecommended ? 8 : 4}
                    stroke={isRecommended ? colors.green : 'none'}
                    strokeWidth={isRecommended ? 3 : 0}
                    strokeOpacity={0.5}
                  />
                );
              })}
            </Scatter>
            
            {/* User preferences point - YELLOW STAR */}
            {userPoint && (
              <Scatter 
                name="Your Preferences" 
                data={[userPoint]} 
                fill="hsl(45 93% 58%)"
                shape="star"
              >
                <Cell 
                  fill="hsl(45 93% 58%)"
                  r={14}
                  stroke="hsl(45 93% 58%)"
                  strokeWidth={4}
                  strokeOpacity={0.4}
                />
              </Scatter>
            )}
          </ScatterChart>
        </ResponsiveContainer>

        {/* Info text */}
        <div className="text-center pt-2">
          <p className="text-xs text-muted-foreground">
            Each point represents a gaming mouse in the embedding space. 
            Closer points indicate more similar mice based on their features.
          </p>
        </div>
      </div>
    </Card>
  );
}