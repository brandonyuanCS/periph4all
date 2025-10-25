import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Home() {
  return (
    <div className="min-h-screen bg-background overflow-x-hidden">
      {/* Hero Section */}
      <div className="relative min-h-screen flex items-center overflow-hidden">
        {/* Animated background gradient orbs - positioned outside container */}
        <div className="absolute top-20 -left-48 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[140px] animate-pulse" />
        
        <div className="container mx-auto px-4 py-16 w-full relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center w-full">
            {/* Left - Mouse Image */}
            <div className="relative h-[600px] lg:h-[700px] group">
              <div className="absolute -inset-4 bg-linear-to-br from-primary/20 to-transparent rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-500" />
              <div className="relative h-full">
                <Image
                  src="/mouse.png"
                  alt="Gaming Mouse"
                  fill
                  className="object-contain drop-shadow-2xl group-hover:scale-105 transition-transform duration-500"
                  priority
                />
              </div>
            </div>

            {/* Right - Content */}
            <div className="space-y-8">
              <div className="space-y-6">
                <Badge variant="secondary" className="text-sm font-medium px-4 py-1.5">
                  AI-Powered Recommendations
                </Badge>
                <div className="space-y-4">
                  <h1 className="text-6xl md:text-8xl font-bold tracking-tight text-gradient">
                    periph4all
                  </h1>
                </div>
                <p className="text-xl md:text-2xl text-muted-foreground max-w-lg leading-relaxed">
                  Find your perfect gaming mouse in <span className="text-primary font-semibold">60 seconds</span> with <b>LLMs</b> leveraging <b>transformer-based embeddings</b>
                </p>
              </div>

              {/* CTA */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/chat">
                  <Button size="lg" className="text-lg px-8 glow-md hover:glow-lg transition-all group">
                    Start Finding Your Mouse
                    <span className="ml-2 group-hover:translate-x-1 transition-transform inline-block">→</span>
                  </Button>
                </Link>
                <Button size="lg" variant="outline" className="text-lg px-8 hover:bg-secondary/50">
                  View All Mice
                </Button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8">
                <div className="text-center lg:text-left space-y-1 group cursor-default">
                  <div className="text-4xl md:text-5xl font-bold text-primary group-hover:scale-110 transition-transform">175+</div>
                  <p className="text-sm text-muted-foreground">Curated Mice</p>
                </div>
                <div className="text-center lg:text-left space-y-1 group cursor-default">
                  <div className="text-4xl md:text-5xl font-bold text-primary group-hover:scale-110 transition-transform">30+</div>
                  <p className="text-sm text-muted-foreground">Brands</p>
                </div>
                <div className="text-center lg:text-left space-y-1 group cursor-default">
                  <div className="text-4xl md:text-5xl font-bold text-primary group-hover:scale-110 transition-transform">20+</div>
                  <p className="text-sm text-muted-foreground">Unique Shapes</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-32">
        <div className="mx-auto max-w-6xl space-y-16">
          <div className="text-center space-y-4">
            <Badge variant="outline" className="mb-4">The Process</Badge>
            <h2 className="text-5xl md:text-6xl font-bold">How It Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Sophisticated AI technology meets intuitive design
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <Card className="glass transition-all hover:-translate-y-2 border-border/50 group overflow-hidden duration-300">
              <div className="absolute inset-0 bg-linear-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <CardHeader className="relative">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-primary/10 text-primary text-2xl font-bold mb-6 group-hover:scale-110 transition-transform">
                  1
                </div>
                <CardTitle className="text-2xl mb-2">Chat with AI</CardTitle>
                <CardDescription className="text-base">
                  Natural conversation interface
                </CardDescription>
              </CardHeader>
              <CardContent className="relative">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Tell us about your hand size, grip style, games you play, and budget through a friendly chat powered by LLMs.
                </p>
              </CardContent>
            </Card>

            <Card className="relative glass transition-all hover:glow-md hover:-translate-y-2 border-border/50 group overflow-hidden duration-300">
              <div className="absolute inset-0 bg-linear-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <CardHeader className="relative">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-primary/10 text-primary text-2xl font-bold mb-6 group-hover:scale-110 transition-transform">
                  2
                </div>
                <CardTitle className="text-2xl mb-2">Vector Embeddings</CardTitle>
                <CardDescription className="text-base">
                  Semantic similarity matching
                </CardDescription>
              </CardHeader>
              <CardContent className="relative">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Your preferences are converted into vectors and compared against our database using cosine similarity.
                </p>
              </CardContent>
            </Card>

            <Card className="relative glass transition-all hover:glow-md hover:-translate-y-2 border-border/50 group overflow-hidden duration-300">
              <div className="absolute inset-0 bg-linear-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <CardHeader className="relative">
                <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-primary/10 text-primary text-2xl font-bold mb-6 group-hover:scale-110 transition-transform">
                  3
                </div>
                <CardTitle className="text-2xl mb-2">Get Matches</CardTitle>
                <CardDescription className="text-base">
                  Top 3 personalized results
                </CardDescription>
              </CardHeader>
              <CardContent className="relative">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  See your top matches with detailed specs, pricing, and AI-generated explanations for why each mouse fits you.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Tech Stack Section */}
      <div className="container mx-auto px-4 py-32">
        <div className="mx-auto max-w-4xl">
          <Card className="relative glass border-border/50 overflow-hidden group">
            <div className="absolute inset-0 bg-linear-to-br from-primary/5 via-transparent to-primary/5 opacity-50" />
            <CardHeader className="relative">
              <Badge variant="outline" className="w-fit mb-4">Tech Stack</Badge>
              <CardTitle className="text-3xl md:text-4xl">Built with Modern AI/ML Stack</CardTitle>
              <CardDescription className="text-base mt-2">
                Demonstrating cutting-edge technologies for production-grade applications
              </CardDescription>
            </CardHeader>
            <CardContent className="relative">
              <div className="flex flex-wrap gap-3">
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">Next.js 16</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">FastAPI</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">OpenAI Embeddings</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">Vector Similarity</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">UMAP</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">Plotly.js</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">Tailwind CSS</Badge>
                <Badge variant="secondary" className="text-sm py-1.5 px-3 hover:bg-primary hover:text-primary-foreground transition-colors cursor-default">shadcn/ui</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer CTA */}
      <div className="container mx-auto px-4 py-32">
        <div className="mx-auto max-w-3xl text-center space-y-8">
          <h2 className="text-5xl md:text-6xl font-bold leading-tight">
            Ready to find your <span className="text-gradient">perfect mouse?</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto">
            It&apos;s hard. Let us do the heavy lifting.
          </p>
          <Link href="/chat">
            <Button size="lg" className="text-lg px-12 py-6 glow-lg hover:scale-105 transition-all group">
              Get Started Now
              <span className="ml-2 group-hover:translate-x-1 transition-transform inline-block">→</span>
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}