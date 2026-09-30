import React, { useState, useEffect } from 'react';
import { TitleBar } from './components/layout/TitleBar';
import { Sidebar } from './components/layout/Sidebar';
import { OverviewView } from './views/OverviewView';
import { WorkspaceView } from './views/WorkspaceView';
import { DocumentsView } from './views/DocumentsView';
import { VisionView } from './views/VisionView';
import { VoiceView } from './views/VoiceView';
import { ActivityView } from './views/ActivityView';
import { PerformanceView } from './views/PerformanceView';
import { SettingsView } from './views/SettingsView';
import type { NavigationTab } from './types';
import { motion, AnimatePresence } from 'framer-motion';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavigationTab>('overview');

  // Keyboard navigation shortcuts (Ctrl+1 to Ctrl+8)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey) {
        switch (e.key) {
          case '1':
            setActiveTab('overview');
            break;
          case '2':
            setActiveTab('workspace');
            break;
          case '3':
            setActiveTab('documents');
            break;
          case '4':
            setActiveTab('vision');
            break;
          case '5':
            setActiveTab('voice');
            break;
          case '6':
            setActiveTab('activity');
            break;
          case '7':
            setActiveTab('performance');
            break;
          case '8':
            setActiveTab('settings');
            break;
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const renderCurrentView = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewView onNavigate={(tab) => setActiveTab(tab)} />;
      case 'workspace':
        return <WorkspaceView />;
      case 'documents':
        return <DocumentsView />;
      case 'vision':
        return <VisionView />;
      case 'voice':
        return <VoiceView onNavigateToOverviewWithPrompt={() => setActiveTab('overview')} />;
      case 'activity':
        return <ActivityView />;
      case 'performance':
        return <PerformanceView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <OverviewView onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-50 text-slate-900 overflow-hidden font-sans select-none">
      {/* Light Premium Window Title Bar */}
      <TitleBar />

      {/* Main Workspace Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar activeTab={activeTab} onSelectTab={(tab) => setActiveTab(tab)} />

        {/* Dynamic Content View Area */}
        <main className="flex-1 bg-slate-50/70 overflow-y-auto p-8 scrollbar-thin">
          <div className="max-w-6xl mx-auto">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                transition={{ duration: 0.12 }}
              >
                {renderCurrentView()}
              </motion.div>
            </AnimatePresence>
          </div>
        </main>
      </div>

      {/* Footer Status Bar */}
      <footer className="h-6 bg-white border-t border-slate-200/80 flex items-center justify-between px-4 text-[10px] text-slate-500 select-none shrink-0 font-mono">
        <div className="flex items-center space-x-3">
          <span className="flex items-center space-x-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            <span>Strict Offline Policy Active</span>
          </span>
          <span className="text-slate-300">|</span>
          <span className="text-slate-600">Tool Guard: Enforced</span>
        </div>

        <div className="flex items-center space-x-4 text-slate-400">
          <span>Shortcuts: Ctrl+1..8</span>
          <span>Target: Windows x64 / Snapdragon NPU</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
