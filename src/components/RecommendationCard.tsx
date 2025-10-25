import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { type RecommendationItem } from "@/lib/api";

interface RecommendationCardProps {
  recommendation: RecommendationItem;
  index: number;
}

export function RecommendationCard({ recommendation, index }: RecommendationCardProps) {
  const { mouse, score, reasoning } = recommendation;

  return (
    <Card className="glass relative overflow-hidden group hover:scale-105 transition-all duration-300 border-border/50 hover:border-primary/50">
      <div className="absolute top-4 right-4 z-10">
        <Badge className="text-lg font-bold bg-primary/20 text-primary border-primary/50">
          #{index + 1}
        </Badge>
      </div>
      
      <div className="p-6 space-y-4">
        <div className="space-y-1">
          <h3 className="text-xl font-bold">{mouse.name}</h3>
          <p className="text-sm text-muted-foreground">by {mouse.brand}</p>
        </div>
        
        {/* Mouse Stats */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          {mouse.price && (
            <div>
              <p className="text-muted-foreground text-xs">Price</p>
              <p className="font-bold text-primary text-lg">${mouse.price}</p>
            </div>
          )}
          {mouse.weight && (
            <div>
              <p className="text-muted-foreground text-xs">Weight</p>
              <p className="font-semibold">{mouse.weight}g</p>
            </div>
          )}
          {mouse.wireless !== undefined && (
            <div>
              <p className="text-muted-foreground text-xs">Connection</p>
              <p className="font-semibold">{mouse.wireless ? 'Wireless' : 'Wired'}</p>
            </div>
          )}
          {mouse.dpi_max && (
            <div>
              <p className="text-muted-foreground text-xs">Max DPI</p>
              <p className="font-semibold">{mouse.dpi_max.toLocaleString()}</p>
            </div>
          )}
        </div>

        {/* Match Score */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <p className="text-xs text-muted-foreground">Match Score</p>
            <p className="text-lg font-bold text-primary">{(score * 100).toFixed(0)}%</p>
          </div>
          <div className="w-full bg-secondary/50 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-primary to-primary/60 h-2 rounded-full transition-all duration-1000 glow-sm"
              style={{ width: `${score * 100}%` }}
            />
          </div>
        </div>

        {/* Reasoning */}
        <div className="pt-3 border-t border-border/50">
          <p className="text-sm text-muted-foreground leading-relaxed">{reasoning}</p>
        </div>

        {/* Buy Button */}
        {mouse.url && (
          <Button asChild className="w-full bg-primary hover:bg-primary/90 group-hover:glow-md transition-all">
            <a href={mouse.url} target="_blank" rel="noopener noreferrer">
              View Details →
            </a>
          </Button>
        )}
      </div>
    </Card>
  );
}

