import React from 'react';
import { ShieldCheck, Cpu, Minus, Square, X } from 'lucide-react';

interface TitleBarProps {
  backendConnected: boolean;
  qualcommStatus: string;
}

export const TitleBar: React.FC<TitleBarProps> = ({ backendConnected, qualcommStatus }) => {
  return (
    <div className="h-10 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-3 text-xs select-none">
      {/* App Branding */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 font-semibold text-slate-200">
          <div className="w-5 h-5 rounded bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold text-xs">
            N
          </div>
          <span>NOVA Workspace Assistant</span>
          <span className="text-[10px] bg-slate-800 text-cyan-400 px-1.5 py-0.5 rounded border border-slate-700">
            v0.1.0-dev
          </span>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Privacy Shield Badge */}
        <div className="flex items-center space-x-1.5 text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Offline Privacy Guard Active</span>
        </div>

        {/* Qualcomm NPU Status */}
        <div className="flex items-center space-x-1.5 text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/50">
          <Cpu className="w-3.5 h-3.5" />
          <span>NPU Isolation: {qualcommStatus}</span>
        </div>
      </div>

      {/* Connection & Window Controls */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 text-slate-400">
          <span className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
          <span className="text-[11px] font-mono">
            {backendConnected ? 'Backend Connected' : 'Backend Disconnected'}
          </span>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Simulated Native Windows Action Buttons */}
        <div className="flex items-center space-x-1 text-slate-400">
          <button className="p-1 hover:bg-slate-800 rounded transition-colors" title="Minimize">
            <Minus className="w-3.5 h-3.5" />
          </button>
          <button className="p-1 hover:bg-slate-800 rounded transition-colors" title="Maximize">
            <Square className="w-3 h-3" />
          </button>
          <button className="p-1 hover:bg-rose-900/50 hover:text-rose-300 rounded transition-colors" title="Close">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
