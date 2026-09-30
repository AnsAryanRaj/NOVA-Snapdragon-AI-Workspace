import React from 'react';
import {
  LayoutDashboard,
  FolderGit2,
  FileText,
  Eye,
  Mic,
  History,
  Cpu,
  Settings,
  ShieldCheck,
  type LucideIcon,
} from 'lucide-react';
import type { NavigationTab } from '../../types';

interface SidebarProps {
  activeTab: NavigationTab;
  onSelectTab: (tab: NavigationTab) => void;
}

interface NavSection {
  title: string;
  items: {
    id: NavigationTab;
    label: string;
    icon: LucideIcon;
    badge?: string;
  }[];
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onSelectTab }) => {
  const sections: NavSection[] = [
    {
      title: 'WORKSPACE',
      items: [
        { id: 'overview', label: 'Overview', icon: LayoutDashboard },
        { id: 'workspace', label: 'Workspace', icon: FolderGit2 },
        { id: 'documents', label: 'Documents', icon: FileText },
      ],
    },
    {
      title: 'INTELLIGENCE',
      items: [
        { id: 'vision', label: 'Vision', icon: Eye },
        { id: 'voice', label: 'Voice', icon: Mic },
      ],
    },
    {
      title: 'INSIGHTS',
      items: [
        { id: 'activity', label: 'Activity', icon: History },
        { id: 'performance', label: 'Performance', icon: Cpu, badge: 'NPU' },
      ],
    },
    {
      title: 'SYSTEM',
      items: [{ id: 'settings', label: 'Settings', icon: Settings }],
    },
  ];

  return (
    <aside className="w-60 bg-slate-50/70 border-r border-slate-200/80 flex flex-col justify-between p-4 select-none shrink-0">
      <div className="space-y-6">
        {/* Workspace Directory Selector */}
        <div className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center space-x-2 text-[11px] font-semibold text-slate-500">
            <FolderGit2 className="w-3.5 h-3.5 text-cyan-600 shrink-0" />
            <span>ACTIVE WORKSPACE</span>
          </div>
          <div className="text-xs font-mono font-medium text-slate-900 mt-1 truncate" title="d:\Nova Snapdragon">
            d:\Nova Snapdragon
          </div>
        </div>

        {/* Grouped Navigation */}
        <nav className="space-y-5">
          {sections.map((section) => (
            <div key={section.title} className="space-y-1">
              <div className="text-[10px] font-bold tracking-wider text-slate-400 uppercase px-3 mb-1.5">
                {section.title}
              </div>
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onSelectTab(item.id)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                      isActive
                        ? 'bg-slate-900 text-white font-semibold shadow-sm'
                        : 'text-slate-600 hover:bg-slate-200/60 hover:text-slate-900'
                    }`}
                  >
                    <div className="flex items-center space-x-2.5">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                      <span>{item.label}</span>
                    </div>
                    {item.badge && (
                      <span
                        className={`text-[9px] font-mono px-1.5 py-0.2 rounded-full font-semibold ${
                          isActive
                            ? 'bg-cyan-500/20 text-cyan-300'
                            : 'bg-slate-200 text-slate-600'
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </nav>
      </div>

      {/* Security & Privacy Notice */}
      <div className="pt-4 border-t border-slate-200/80 text-xs text-slate-500 space-y-1">
        <div className="flex items-center space-x-1.5 text-emerald-700 font-semibold text-[11px]">
          <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
          <span>Local On-Device Privacy</span>
        </div>
        <p className="text-[10px] text-slate-500 leading-tight">
          Your workspace data stays on this device.
        </p>
      </div>
    </aside>
  );
};
