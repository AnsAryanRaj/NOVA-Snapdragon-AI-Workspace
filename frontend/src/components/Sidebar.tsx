import React from 'react';
import { LayoutDashboard, Shield, History, Cpu, FolderGit2 } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'overview', label: 'Workspace Overview', icon: LayoutDashboard },
    { id: 'security', label: 'Tool Security & Policies', icon: Shield },
    { id: 'audit', label: 'Audit Trail Ledger', icon: History },
    { id: 'qualcomm', label: 'Snapdragon NPU Isolation', icon: Cpu },
  ];

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between p-3 select-none">
      <div className="space-y-6">
        {/* Workspace Context Box */}
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-400 mb-1">
            <FolderGit2 className="w-4 h-4 text-cyan-400" />
            <span>Active Workspace</span>
          </div>
          <div className="text-xs text-slate-200 font-mono truncate" title="d:\Nova Snapdragon">
            d:\Nova Snapdragon
          </div>
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500">
            <span>Status: Clean</span>
            <span className="text-emerald-400 font-semibold">Indexed</span>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1">
          <div className="text-[10px] font-semibold tracking-wider text-slate-500 uppercase px-3 mb-2">
            Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-500 space-y-1">
        <div className="flex justify-between">
          <span>Security Architecture:</span>
          <span className="text-slate-400">Tool Registry</span>
        </div>
        <div className="flex justify-between">
          <span>Shell Command Execution:</span>
          <span className="text-rose-400 font-semibold">Blocked</span>
        </div>
      </div>
    </div>
  );
};
