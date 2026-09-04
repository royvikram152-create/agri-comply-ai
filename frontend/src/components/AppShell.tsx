import React, { ReactNode } from 'react';
import { ShieldCheck, LayoutDashboard, Package, Scale, Bot, Sparkles, BookOpen, PlusCircle } from 'lucide-react';

interface AppShellProps {
  children: ReactNode;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onNewShipmentClick?: () => void;
}

export const AppShell: React.FC<AppShellProps> = ({
  children,
  activeTab,
  setActiveTab,
  onNewShipmentClick,
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Compliance Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { id: 'shipments', label: 'Shipments', icon: <Package className="w-4 h-4" /> },
    { id: 'agents', label: 'Specialized Agents (5)', icon: <Bot className="w-4 h-4" /> },
    { id: 'regulations', label: 'EU Regulations RAG', icon: <Scale className="w-4 h-4" /> },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-900 text-slate-100">
      {/* Top Header */}
      <header className="h-16 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-brand-600 to-emerald-400 text-white shadow-lg shadow-brand-900/40">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-black text-lg text-slate-100 tracking-tight">AGRICOMPLY AI</h1>
              <span className="px-2 py-0.5 bg-brand-500/20 text-brand-400 border border-brand-500/30 text-[10px] font-extrabold rounded-full uppercase tracking-widest">
                COPILOT
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">Agentic Export Documentation & Deterministic Compliance Engine</p>
          </div>
        </div>

        {/* Header Right Actions */}
        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-xl text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="text-slate-300 font-medium">Demo Mode: Zero-Cost Local/Serverless</span>
          </div>

          {onNewShipmentClick && (
            <button
              onClick={onNewShipmentClick}
              className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-brand-900/40 flex items-center space-x-1.5 transition"
            >
              <PlusCircle className="w-4 h-4" />
              <span>New Export Shipment</span>
            </button>
          )}
        </div>
      </header>

      {/* Main Layout Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 bg-slate-950/40 p-4 space-y-6 flex-shrink-0 hidden md:block">
          <div>
            <div className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest px-3 mb-2">Main Menu</div>
            <nav className="space-y-1">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                    activeTab === item.id
                      ? 'bg-slate-800 text-brand-400 border border-slate-700 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Primary Demo Card */}
          <div className="p-4 bg-gradient-to-br from-slate-900 to-slate-950 border border-emerald-500/20 rounded-2xl space-y-2">
            <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold">
              <Sparkles className="w-4 h-4" />
              <span>Primary Demo Scenario</span>
            </div>
            <div className="text-xs text-slate-300 font-medium">
              <div><strong className="text-slate-100">Crop:</strong> Mango (Alphonso)</div>
              <div><strong className="text-slate-100">Route:</strong> India → EU</div>
              <div><strong className="text-slate-100">Deadline:</strong> 7 Days</div>
              <div><strong className="text-slate-100">ID:</strong> SHP-MANGO-001</div>
            </div>
          </div>
        </aside>

        {/* Content View */}
        <main className="flex-1 overflow-y-auto p-6 bg-slate-900">
          {children}
        </main>
      </div>
    </div>
  );
};
