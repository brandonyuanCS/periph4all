"use client";

import { useState, useEffect, useCallback } from "react";
import dynamic from "next/dynamic";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { getGraphData, type UserPreferences } from "@/lib/api";

// Dynamically import ForceGraph2D to avoid SSR issues
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
});

interface ForceGraphVisualizationProps {
  preferences: UserPreferences;
}

interface GraphNode {
  id: string;
  name: string;
  x?: number;
  y?: number;
  val: number;
  color: string;
  isRecommended: boolean;
  isUser: boolean;
}

interface GraphLink {
  source: string;
  target: string;
  value: number;
  similarity: number;
  isUserLink: boolean;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export function ForceGraphVisualization({ preferences }: ForceGraphVisualizationProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [kNeighbors, setKNeighbors] = useState(5);
  const [showLabels, setShowLabels] = useState(false);

  const colors = {
    foreground: 'rgba(250, 250, 250, 0.4)',
    recommended: 'rgb(34, 197, 94)',
    user: 'rgb(234, 179, 8)',
    link: 'rgba(100, 100, 100, 0.2)',
    userLink: 'rgba(234, 179, 8, 0.6)'
  };

  useEffect(() => {
    const fetchGraphData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getGraphData(preferences, kNeighbors);
        
        console.log("Graph data received:", data);
        
        const viz = data.visualization;
        const recommendedNames = new Set(
          viz.recommended_points?.map(p => p.mouse_name) || []
        );

        // Create nodes
        const nodes: GraphNode[] = viz.mouse_points.map((point, idx) => {
          const isRecommended = recommendedNames.has(point.mouse_name);
          return {
            id: `mouse-${idx}`,
            name: point.mouse_name,
            x: point.x * 100,
            y: point.y * 100,
            val: isRecommended ? 10 : 4,
            color: isRecommended ? colors.recommended : colors.foreground,
            isRecommended,
            isUser: false,
          };
        });

        // Add user node
        if (viz.user_point) {
          nodes.push({
            id: 'user-preference',
            name: viz.user_point.mouse_name,
            x: viz.user_point.x * 100,
            y: viz.user_point.y * 100,
            val: 14,
            color: colors.user,
            isRecommended: false,
            isUser: true,
          });
        }

        // Create links from backend edges (based on embedding similarity)
        const links: GraphLink[] = data.edges.map(edge => ({
          source: `mouse-${edge.source}`,
          target: `mouse-${edge.target}`,
          value: edge.similarity,
          similarity: edge.similarity,
          isUserLink: false,
        }));

        // Add user links
        if (data.user_edges) {
          data.user_edges.forEach(edge => {
            links.push({
              source: 'user-preference',
              target: `mouse-${edge.target}`,
              value: edge.similarity * 2, // Stronger visual weight
              similarity: edge.similarity,
              isUserLink: true,
            });
          });
        }

        console.log(`Created ${nodes.length} nodes and ${links.length} links`);
        
        setGraphData({ nodes, links });
      } catch (err) {
        console.error("Failed to load graph data:", err);
        setError(err instanceof Error ? err.message : "Failed to load visualization");
      } finally {
        setIsLoading(false);
      }
    };

    fetchGraphData();
  }, [preferences, kNeighbors]);

  const handleNodeHover = useCallback((node: any) => {
    setHoveredNode(node as GraphNode | null);
  }, []);

  const paintNode = useCallback((node: any, ctx: CanvasRenderingContext2D) => {
    const size = node.val;
    
    if (node.isUser) {
      // Draw star for user
      drawStar(ctx, node.x || 0, node.y || 0, 5, size, size / 2, node.color);
    } else {
      // Draw circle for mice
      ctx.beginPath();
      ctx.arc(node.x || 0, node.y || 0, size, 0, 2 * Math.PI);
      ctx.fillStyle = node.color;
      ctx.fill();
      
      // Add ring for recommended mice
      if (node.isRecommended) {
        ctx.strokeStyle = node.color;
        ctx.lineWidth = 3;
        ctx.stroke();
      }
    }

    // Draw label on hover or if showLabels is true
    if ((hoveredNode && hoveredNode.id === node.id) || (showLabels && (node.isRecommended || node.isUser))) {
      ctx.font = '12px Sans-Serif';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.8)';
      ctx.lineWidth = 3;
      
      const text = node.name;
      const textX = (node.x || 0) + size + 8;
      const textY = (node.y || 0) + 4;
      
      ctx.strokeText(text, textX, textY);
      ctx.fillText(text, textX, textY);
    }
  }, [hoveredNode, showLabels]);

  const paintLink = useCallback((link: any, ctx: CanvasRenderingContext2D) => {
    const { source, target } = link;
    if (typeof source !== 'object' || typeof target !== 'object') return;
    
    // Highlight user links
    const isUserLink = link.isUserLink;
    
    ctx.beginPath();
    ctx.moveTo(source.x, source.y);
    ctx.lineTo(target.x, target.y);
    ctx.strokeStyle = isUserLink ? colors.userLink : colors.link;
    ctx.lineWidth = isUserLink ? 3 : 1;
    ctx.stroke();
  }, [colors]);

  const drawStar = (
    ctx: CanvasRenderingContext2D,
    cx: number,
    cy: number,
    spikes: number,
    outerRadius: number,
    innerRadius: number,
    color: string
  ) => {
    let rot = (Math.PI / 2) * 3;
    const step = Math.PI / spikes;

    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);

    for (let i = 0; i < spikes; i++) {
      let x = cx + Math.cos(rot) * outerRadius;
      let y = cy + Math.sin(rot) * outerRadius;
      ctx.lineTo(x, y);
      rot += step;

      x = cx + Math.cos(rot) * innerRadius;
      y = cy + Math.sin(rot) * innerRadius;
      ctx.lineTo(x, y);
      rot += step;
    }

    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    
    // Add glow
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.stroke();
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
        {/* Controls */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          {/* Legend */}
          <div className="flex items-center gap-6 flex-wrap">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-foreground/40" />
              <span className="text-xs text-muted-foreground">All Mice</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-green-500 ring-2 ring-green-500/30" />
              <span className="text-xs text-green-500 font-medium">Recommended</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-yellow-500 clip-star" />
              <span className="text-xs text-yellow-500 font-medium">Your Preferences</span>
            </div>
          </div>

          {/* K-Neighbors Control */}
          <div className="flex items-center gap-3">
            <label className="text-xs text-muted-foreground whitespace-nowrap">
              Connections per mouse: {kNeighbors}
            </label>
            <Slider
              value={[kNeighbors]}
              onValueChange={(values) => setKNeighbors(values[0])}
              min={3}
              max={10}
              step={1}
              className="w-32"
            />
          </div>
        </div>

        {/* Graph Stats */}
        <div className="flex gap-4 text-xs text-muted-foreground">
          <Badge variant="outline" className="font-mono">
            {graphData.nodes.length} nodes
          </Badge>
          <Badge variant="outline" className="font-mono">
            {graphData.links.length} edges
          </Badge>
          <Badge variant="outline" className="font-mono">
            Avg: {(graphData.links.reduce((sum, l) => sum + l.similarity, 0) / graphData.links.length).toFixed(3)} similarity
          </Badge>
        </div>

        {/* Force Graph */}
        <div className="relative bg-background/40 rounded-lg overflow-hidden" style={{ height: '600px' }}>
          <ForceGraph2D
            graphData={graphData}
            nodeLabel="name"
            nodeCanvasObject={paintNode}
            linkCanvasObject={paintLink}
            onNodeHover={handleNodeHover}
            linkDirectionalParticles={2}
            linkDirectionalParticleWidth={2}
            linkDirectionalParticleSpeed={0.005}
            cooldownTicks={100}
            width={1000}
            height={600}
            backgroundColor="rgba(0,0,0,0)"
            nodeRelSize={1}
            linkWidth={1}
            d3AlphaDecay={0.02}
            d3VelocityDecay={0.3}
          />
        </div>

        {/* Info text */}
        <div className="text-center pt-2 space-y-1">
          <p className="text-xs text-muted-foreground">
            Force-directed graph showing mouse similarities based on embedding space.
          </p>
          <p className="text-xs text-muted-foreground">
            Each mouse connects to its {kNeighbors} most similar mice. Yellow lines show your preferences.
          </p>
        </div>
      </div>
    </Card>
  );
}