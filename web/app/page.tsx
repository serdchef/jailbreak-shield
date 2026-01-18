import Link from "next/link";
import { Shield, ChevronRight, CheckCircle2 } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-8 relative overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-aegis-primary/10 via-black to-black -z-10" />

      <main className="max-w-3xl mx-auto text-center space-y-12">

        {/* Hero Section */}
        <div className="space-y-6">
          <div className="flex justify-center mb-8">
            <div className="p-3 bg-aegis-primary/10 rounded-2xl border border-aegis-primary/20 animate-pulse">
              <Shield className="w-12 h-12 text-aegis-primary" />
            </div>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
            LLMs are exploitable.<br />
            <span className="text-aegis-primary">Shield Aegis</span> exists to stop that.
          </h1>

          <p className="text-xl text-aegis-text-muted max-w-2xl mx-auto leading-relaxed">
            Real-time detection and response against prompt injection, jailbreaks, and model abuse.
          </p>
        </div>

        {/* 3 Bullet Points (Sert) */}
        <div className="grid md:grid-cols-3 gap-6 text-left">
          <FeatureItem text="Detect malicious prompt patterns in real time" />
          <FeatureItem text="Enforce policy before the model responds" />
          <FeatureItem text="Designed for production LLM systems" />
        </div>

        {/* Single CTA */}
        <div className="pt-8">
          <Link
            href="/console"
            className="inline-flex items-center gap-3 bg-aegis-primary text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-aegis-primary/90 transition-all hover:scale-105 group"
          >
            Access Console
            <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <p className="mt-4 text-xs font-mono text-aegis-text-muted opacity-50">v3.0.0 // PRODUCTION READY</p>
        </div>

      </main>

      {/* Footer Statement */}
      <footer className="absolute bottom-8 text-center text-aegis-text-muted text-sm font-mono opacity-40">
        AI systems will be attacked. We are building the defense layer.
      </footer>
    </div>
  );
}

function FeatureItem({ text }: { text: string }) {
  return (
    <div className="flex items-start gap-3 p-4 rounded-lg border border-white/5 bg-white/5 backdrop-blur-sm">
      <CheckCircle2 className="w-5 h-5 text-aegis-primary shrink-0 mt-0.5" />
      <span className="text-sm font-medium text-aegis-text">{text}</span>
    </div>
  )
}
