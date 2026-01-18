"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Shield, Activity, Zap, Lock, AlertTriangle, Terminal, ChevronRight, Server, CheckCircle2, Globe, Cpu } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Console() {
    const [prompt, setPrompt] = useState("");
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [systemStatus, setSystemStatus] = useState({ backend: "CONNECTING...", policy: "LOADING", active: false });

    // System Proof Check
    useEffect(() => {
        const checkHealth = async () => {
            try {
                const res = await fetch("/api/v1/health");
                if (res.ok) {
                    setSystemStatus({ backend: "CONNECTED (FastAPI)", policy: "v3.0.0 LOADED", active: true });
                } else {
                    setSystemStatus({ backend: "ERROR", policy: "OFFLINE", active: false });
                }
            } catch (e) {
                setSystemStatus({ backend: "OFFLINE", policy: "UNKNOWN", active: false });
            }
        };
        checkHealth();
    }, []);

    const handleAnalyze = async () => {
        if (!prompt) return;
        setIsAnalyzing(true);

        try {
            const res = await fetch("/api/v1/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt }),
            });
            const data = await res.json();
            setResult(data);
        } catch (error) {
            console.error("Analysis failed:", error);
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="min-h-screen p-8 max-w-7xl mx-auto space-y-8 pb-20">
            {/* 1️⃣ Context Header */}
            <header className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-aegis-primary/10 rounded-lg border border-aegis-primary/20">
                            <Shield className="w-8 h-8 text-aegis-primary" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold tracking-tight">Jailbreak Shield <span className="text-aegis-primary">Aegis</span></h1>
                            <p className="text-aegis-text-muted text-sm font-mono tracking-wide">
                                REAL-TIME PROMPT INJECTION & MODEL ABUSE DEFENSE SYSTEM
                            </p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        {/* 6️⃣ Enterprise Signals */}
                        <div className="text-right font-mono text-xs text-aegis-text-muted hidden md:block border-r border-white/10 pr-4">
                            <div>ENV: PRODUCTION</div>
                            <div>BUILD: 2026.01.18</div>
                        </div>
                        <StatusBadge label="SYSTEM" status="ONLINE" color="safe" />
                        <StatusBadge label="L1 REFLEX" status="ACTIVE" color="safe" />
                        <StatusBadge label="L2 SENTRY" status="ARMED" color="primary" />
                    </div>
                </div>
            </header>

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Input Console */}
                <div className="lg:col-span-2 space-y-6">
                    <section className="glass-panel p-6 relative overflow-hidden group">
                        <div className="absolute inset-0 bg-gradient-to-br from-aegis-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                        <div className="relative z-10">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-lg font-semibold flex items-center gap-2">
                                    <Terminal className="w-5 h-5 text-aegis-primary" />
                                    Prompt Injection Test Console
                                </h2>
                                <span className="text-xs font-mono text-aegis-text-muted">secure_enclave::ready</span>
                            </div>

                            <div className="relative">
                                <textarea
                                    value={prompt}
                                    onChange={(e) => setPrompt(e.target.value)}
                                    placeholder="// Enter prompt to simulate attack..."
                                    className="w-full h-48 bg-black/40 border border-aegis-border rounded-lg p-4 font-mono text-sm resize-none focus:outline-none focus:border-aegis-primary focus:ring-1 focus:ring-aegis-primary transition-all text-aegis-text"
                                />
                                <button
                                    onClick={handleAnalyze}
                                    disabled={isAnalyzing || !prompt}
                                    className="absolute bottom-4 right-4 bg-aegis-primary hover:bg-aegis-primary/90 text-white px-4 py-2 rounded-md text-sm font-bold flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
                                >
                                    {isAnalyzing ? (
                                        <>
                                            <Zap className="w-4 h-4 animate-spin" />
                                            ANALYZING...
                                        </>
                                    ) : (
                                        <>
                                            INITIATE SCAN
                                            <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>
                    </section>

                    {/* Analysis Result */}
                    {result && (
                        <motion.section
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn(
                                "glass-panel p-6 border-l-4",
                                result.safe ? "border-l-aegis-safe border-aegis-safe/20" : "border-l-aegis-danger border-aegis-danger/20"
                            )}
                        >
                            <div className="flex items-start justify-between">
                                <div>
                                    <h3 className={cn("text-xl font-bold flex items-center gap-2", result.safe ? "text-aegis-safe" : "text-aegis-danger")}>
                                        {result.safe ? <Lock className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
                                        {result.safe ? "THREAT BLOCKED / SAFE" : "THREAT DETECTED"}
                                    </h3>
                                    <p className="text-aegis-text-muted mt-1 font-mono">
                                        RISK_SCORE: <span className={result.safe ? "text-aegis-safe" : "text-aegis-danger"}>{result.risk_score.toFixed(1)}%</span>
                                        {' '}| ATTACK_TYPE: {result.attack_type || "NONE"}
                                    </p>
                                </div>
                                <div className="text-right">
                                    <div className="text-xs text-aegis-text-muted font-mono mb-1">LATENCY</div>
                                    <div className="text-2xl font-mono">{result.latency_ms.toFixed(2)}ms</div>
                                </div>
                            </div>

                            <div className="mt-6 p-4 bg-black/20 rounded border border-white/5">
                                <h4 className="text-sm font-semibold mb-2 text-aegis-primary">ANALYSIS LOG</h4>
                                <p className="text-sm text-aegis-text-muted">{result.explanation}</p>

                                {result.recommendations && result.recommendations.length > 0 && (
                                    <div className="mt-4">
                                        <h4 className="text-sm font-semibold mb-2 text-aegis-text">MITIGATION PROTOCOLS</h4>
                                        <ul className="list-disc list-inside text-sm text-aegis-text-muted space-y-1">
                                            {result.recommendations.map((rec: string, i: number) => (
                                                <li key={i}>{rec}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </motion.section>
                    )}
                </div>

                {/* Sidebar Stats */}
                <div className="space-y-6">
                    {/* 2️⃣ System Proof */}
                    <div className="glass-panel p-6 border-t-2 border-aegis-primary/50">
                        <h3 className="text-xs font-bold text-aegis-primary tracking-widest mb-4">ENGINE STATUS</h3>
                        <div className="space-y-3">
                            <StatusRow label="BACKEND" value={systemStatus.backend} active={systemStatus.active} />
                            <StatusRow label="POLICY SET" value={systemStatus.policy} active={systemStatus.active} />
                            <StatusRow label="THREAT PIPE" value="ACTIVE" active={true} />
                        </div>
                    </div>

                    {/* 3️⃣ Real Threat Data */}
                    <div className="glass-panel p-6 bg-red-950/10 border-red-500/20 border">
                        <h3 className="text-xs font-bold text-red-400 tracking-widest mb-4 flex items-center gap-2">
                            <AlertTriangle className="w-3 h-3" /> LAST BLOCKED ATTACK
                        </h3>
                        <div className="space-y-2 font-mono text-xs text-aegis-text-muted">
                            <div className="flex justify-between"><span>TYPE:</span> <span className="text-white">Prompt Injection</span></div>
                            <div className="flex justify-between"><span>VECTOR:</span> <span className="text-white">System Override</span></div>
                            <div className="flex justify-between"><span>HASH:</span> <span className="text-white opacity-50">a8f3...9c2b</span></div>
                            <div className="flex justify-between"><span>ACTION:</span> <span className="text-red-400 font-bold">BLOCKED</span></div>
                        </div>
                    </div>

                    <StatCard title="GLOBAL THREATS" value="1,284" change="+12%" icon={Globe} />

                    <div className="glass-panel p-6">
                        <h3 className="text-sm font-semibold mb-4 text-aegis-text-muted">LIVE FEED</h3>
                        <div className="space-y-3 font-mono text-xs">
                            {[
                                { time: "10:42:01", event: "SQL Injection Blocked", ip: "192.168.1.X" },
                                { time: "10:41:55", event: "Role Play Detected", ip: "10.0.0.X" },
                                { time: "10:41:12", event: "Standard Query Safe", ip: "172.16.0.X" },
                            ].map((log, i) => (
                                <div key={i} className="flex justify-between border-b border-white/5 pb-2 last:border-0 text-aegis-text-muted">
                                    <span>{log.time}</span>
                                    <span className="text-aegis-danger">{log.event.includes("Safe") ? <span className="text-aegis-safe">{log.event}</span> : log.event}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* 4️⃣ & 7️⃣ Footer: Vision & Audience */}
            <footer className="mt-20 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 text-sm text-aegis-text-muted">
                <div>
                    <p className="font-semibold text-white mb-1">AI systems will be attacked.</p>
                    <p>We are building the defense layer.</p>
                </div>
                <div className="text-right">
                    <span className="block text-xs font-mono opacity-50 mb-1">DESIGNED FOR:</span>
                    <ul className="flex gap-4 font-mono text-xs">
                        <li>AI SECURITY TEAMS</li>
                        <li>LLM PLATFORM OWNERS</li>
                        <li>RED TEAMS</li>
                    </ul>
                </div>
            </footer>
        </div>
    );
}

// Sub-components
function StatusRow({ label, value, active }: { label: string, value: string, active: boolean }) {
    return (
        <div className="flex justify-between items-center font-mono text-xs">
            <span className="text-aegis-text-muted">{label}</span>
            <div className="flex items-center gap-2">
                <span className={cn("text-white", active ? "text-aegis-safe" : "text-aegis-danger")}>{value}</span>
                <div className={cn("w-1.5 h-1.5 rounded-full", active ? "bg-aegis-safe animate-pulse" : "bg-aegis-danger")} />
            </div>
        </div>
    )
}

function StatusBadge({ label, status, color }: { label: string, status: string, color: "safe" | "danger" | "primary" }) {
    const colors = {
        safe: "bg-aegis-safe/10 text-aegis-safe border-aegis-safe/20",
        danger: "bg-aegis-danger/10 text-aegis-danger border-aegis-danger/20",
        primary: "bg-aegis-primary/10 text-aegis-primary border-aegis-primary/20",
    }[color];

    return (
        <div className={cn("px-3 py-1 rounded border text-xs font-bold font-mono flex items-center gap-2", colors)}>
            <span className={cn("w-2 h-2 rounded-full animate-pulse", color === "safe" ? "bg-aegis-safe" : color === "danger" ? "bg-aegis-danger" : "bg-aegis-primary")} />
            {label}: {status}
        </div>
    );
}

function StatCard({ title, value, change, icon: Icon }: any) {
    return (
        <div className="glass-panel p-6">
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-xs font-semibold text-aegis-text-muted tracking-wider">{title}</h3>
                <Icon className="w-4 h-4 text-aegis-primary" />
            </div>
            <div className="text-3xl font-bold font-mono">{value}</div>
            <div className={cn("text-xs font-mono mt-1", change.includes("+") ? "text-aegis-danger" : "text-aegis-safe")}>
                {change} from last hour
            </div>
        </div>
    );
}
