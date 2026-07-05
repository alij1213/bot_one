import { useState } from "react";
import { BotSimulator } from "./components/BotSimulator";
import { CodeExplorer } from "./components/CodeExplorer";
import { Configurator } from "./components/Configurator";
import { 
  Shield, 
  Terminal, 
  BookOpen, 
  Cpu, 
  Settings, 
  Activity, 
  Download, 
  CheckCircle, 
  ExternalLink,
  Lock,
  MessageSquare,
  Sparkles
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<"simulator" | "explorer" | "env" | "guide">("simulator");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-slate-950 font-sans antialiased">
      
      {/* Decorative Blur Orbs */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Header Area */}
      <header className="border-b border-slate-900 bg-slate-950/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
              <Shield className="h-5 w-5 text-cyan-400" />
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-tight text-slate-100 flex items-center gap-1.5">
                Telegram Group Bot Suite
              </h1>
              <p className="text-[10px] text-slate-400 font-mono">v1.2.0 • aiogram 3.x</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <a 
              href="#env-configurator"
              onClick={() => setActiveTab("env")}
              className="text-xs text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1"
            >
              <span>Quick Config</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12 space-y-12">
        
        {/* Hero Section */}
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[10px] font-semibold uppercase tracking-wider font-mono">
            <Sparkles className="h-3.5 w-3.5" /> Enterprise-Grade Python System
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-100 leading-tight">
            Professional Group Moderation & Anti-Spam Bot
          </h2>
          <p className="text-sm sm:text-base text-slate-400 leading-relaxed">
            A production-ready, asynchronous Telegram Group management bot built with **Python 3.12** and **aiogram 3.x**. Features Redis caching for anti-flood limits, full Persian & English support, math verification captchas, media lock triggers, and structured SQLAlchemy schemas.
          </p>
        </div>

        {/* Highlight Stats Bento Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/40 border border-slate-900 rounded-2xl p-5 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Architecture</span>
            <div className="text-lg font-bold text-slate-200">Modular MVC</div>
            <div className="text-[10px] text-cyan-400 font-mono">SQLAlchemy + ORM</div>
          </div>
          <div className="bg-slate-900/40 border border-slate-900 rounded-2xl p-5 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Shield Engine</span>
            <div className="text-lg font-bold text-slate-200">Redis Cache</div>
            <div className="text-[10px] text-emerald-400 font-mono">Anti-Flood & Rate Limits</div>
          </div>
          <div className="bg-slate-900/40 border border-slate-900 rounded-2xl p-5 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Localization</span>
            <div className="text-lg font-bold text-slate-200">EN & FA (فارسی)</div>
            <div className="text-[10px] text-cyan-400 font-mono">Stored in Group Settings</div>
          </div>
          <div className="bg-slate-900/40 border border-slate-900 rounded-2xl p-5 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Security Filters</span>
            <div className="text-lg font-bold text-slate-200">Math Captcha</div>
            <div className="text-[10px] text-indigo-400 font-mono">16 Media Lock Handles</div>
          </div>
        </div>

        {/* Tab Selection Navigation */}
        <div className="flex border-b border-slate-900 pb-px overflow-x-auto gap-8">
          <button
            onClick={() => setActiveTab("simulator")}
            className={`pb-4 text-sm font-semibold tracking-wide transition-all border-b-2 flex items-center gap-2 whitespace-nowrap ${
              activeTab === "simulator"
                ? "border-cyan-500 text-cyan-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Terminal className="h-4 w-4" />
            <span>Interactive Bot Simulator</span>
          </button>

          <button
            onClick={() => setActiveTab("explorer")}
            className={`pb-4 text-sm font-semibold tracking-wide transition-all border-b-2 flex items-center gap-2 whitespace-nowrap ${
              activeTab === "explorer"
                ? "border-cyan-500 text-cyan-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <BookOpen className="h-4 w-4" />
            <span>Project Source Code</span>
          </button>

          <button
            onClick={() => setActiveTab("env")}
            className={`pb-4 text-sm font-semibold tracking-wide transition-all border-b-2 flex items-center gap-2 whitespace-nowrap ${
              activeTab === "env"
                ? "border-cyan-500 text-cyan-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Settings className="h-4 w-4" />
            <span>Environment Configurator</span>
          </button>

          <button
            onClick={() => setActiveTab("guide")}
            className={`pb-4 text-sm font-semibold tracking-wide transition-all border-b-2 flex items-center gap-2 whitespace-nowrap ${
              activeTab === "guide"
                ? "border-cyan-500 text-cyan-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Cpu className="h-4 w-4" />
            <span>Deployment Guide</span>
          </button>
        </div>

        {/* Tab Contents */}
        <div className="min-h-[400px]">
          {activeTab === "simulator" && (
            <div className="space-y-6">
              <div className="space-y-1">
                <h3 className="text-lg font-bold text-slate-200">Chat & Commands Playground</h3>
                <p className="text-xs text-slate-400">
                  Simulate typical group administrator interactions and test message rendering in English and Farsi.
                </p>
              </div>
              <BotSimulator />
            </div>
          )}

          {activeTab === "explorer" && (
            <div className="space-y-6">
              <div className="space-y-1">
                <h3 className="text-lg font-bold text-slate-200">Source Code Repository</h3>
                <p className="text-xs text-slate-400">
                  Browse and review the production-ready modular Python files created in your workspace folder.
                </p>
              </div>
              <CodeExplorer />
            </div>
          )}

          {activeTab === "env" && (
            <div className="space-y-6">
              <div className="space-y-1">
                <h3 className="text-lg font-bold text-slate-200">Environment Builder</h3>
                <p className="text-xs text-slate-400">
                  Compose, review, and export your production variables configurations.
                </p>
              </div>
              <Configurator />
            </div>
          )}

          {activeTab === "guide" && (
            <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-8 max-w-4xl">
              <div className="space-y-2">
                <h3 className="text-lg font-bold text-slate-100">Step-by-Step Production Hosting Guide</h3>
                <p className="text-xs text-slate-400">
                  Follow these instructions to run the bot on any Linux VPS or server cluster.
                </p>
              </div>

              <div className="space-y-6 text-sm">
                <div className="flex gap-4">
                  <div className="h-7 w-7 bg-cyan-500/10 rounded-lg flex items-center justify-center font-bold text-cyan-400 shrink-0 font-mono text-xs">
                    1
                  </div>
                  <div className="space-y-1.5">
                    <h4 className="font-semibold text-slate-200">Export Code Folder</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Download the codebase from this workspace. If you use AI Studio export, you can extract the <code className="bg-slate-950 px-1 py-0.5 rounded text-cyan-400 font-mono text-[10px]">bot/</code> directory.
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="h-7 w-7 bg-cyan-500/10 rounded-lg flex items-center justify-center font-bold text-cyan-400 shrink-0 font-mono text-xs">
                    2
                  </div>
                  <div className="space-y-1.5">
                    <h4 className="font-semibold text-slate-200">Setup credentials in .env</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Create a file named <code className="bg-slate-950 px-1 py-0.5 rounded text-cyan-400 font-mono text-[10px]">.env</code> in the project directory using the generator in the third tab, supplying your secret token and Owner numerical ID.
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="h-7 w-7 bg-cyan-500/10 rounded-lg flex items-center justify-center font-bold text-cyan-400 shrink-0 font-mono text-xs">
                    3
                  </div>
                  <div className="space-y-1.5">
                    <h4 className="font-semibold text-slate-200">Deploy via Docker Compose</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Boot up both the bot polling cycle and the automated Redis caching service in one command:
                    </p>
                    <pre className="bg-slate-950 p-3 rounded-lg text-xs font-mono text-cyan-400 border border-slate-800">
                      docker-compose up -d --build
                    </pre>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="h-7 w-7 bg-cyan-500/10 rounded-lg flex items-center justify-center font-bold text-cyan-400 shrink-0 font-mono text-xs">
                    4
                  </div>
                  <div className="space-y-1.5">
                    <h4 className="font-semibold text-slate-200">Upgrade to PostgreSQL (Optional)</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      If you grow to host thousands of groups, switch the db string in <code className="bg-slate-950 px-1 py-0.5 rounded text-cyan-400 font-mono text-[10px]">.env</code> to point to any host PostgreSQL cluster. The database adapters handle the schema mapping automatically without modifications.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

      </main>

      <footer className="border-t border-slate-900 bg-slate-950 mt-20 py-8 text-center text-xs text-slate-500 font-mono">
        <p>© 2026 Enterprise Group Management Suite. Built with Python & React.</p>
      </footer>
    </div>
  );
}
