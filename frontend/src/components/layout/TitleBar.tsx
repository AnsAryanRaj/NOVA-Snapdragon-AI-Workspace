import React from 'react';
import { Minus, Square, X, ShieldCheck } from 'lucide-react';
import { StatusIndicator } from '../ui/StatusIndicator';

interface TitleBarProps {}

export const TitleBar: React.FC<TitleBarProps> = () => {
  return (
    <div className="h-11 bg-white/90 backdrop-blur-md border-b border-slate-200/80 flex items-center justify-between px-4 text-xs select-none shrink-0 z-40">
      {/* App Branding & NOVA Identity */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2.5">
          <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xs shadow-xs">
            N
          </div>
          <span className="font-bold text-slate-900 text-sm tracking-tight">NOVA</span>
          <span className="text-slate-300 hidden sm:inline">•</span>
          <span className="text-slate-500 text-[11px] font-medium hidden sm:inline">
            Privacy-first workspace assistant
          </span>
        </div>

        <div className="h-3.5 w-px bg-slate-200 hidden md:block" />

        {/* Visually Subtle Status Indicators */}
        <div className="hidden md:flex items-center space-x-3">
          <StatusIndicator label="Local" status="active" />
          <span className="text-slate-300">/</span>
          <StatusIndicator label="Secure" status="secure" />
          <span className="text-slate-300">/</span>
          <StatusIndicator label="AI Ready" status="ready" />
        </div>
      </div>

      {/* Right Controls & Window Actions */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-1.5 text-slate-600 text-[11px] bg-slate-100/80 px-2.5 py-1 rounded-full border border-slate-200/60">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span className="font-medium text-slate-700">Offline Guard Active</span>
        </div>

        <div className="h-3.5 w-px bg-slate-200" />

        {/* Native Windows Window Actions */}
        <div className="flex items-center space-x-0.5 text-slate-500">
          <button className="p-1.5 hover:bg-slate-100 hover:text-slate-900 rounded-lg transition-colors" title="Minimize">
            <Minus className="w-3.5 h-3.5" />
          </button>
          <button className="p-1.5 hover:bg-slate-100 hover:text-slate-900 rounded-lg transition-colors" title="Maximize">
            <Square className="w-3 h-3" />
          </button>
          <button className="p-1.5 hover:bg-rose-50 hover:text-rose-600 rounded-lg transition-colors" title="Close">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
