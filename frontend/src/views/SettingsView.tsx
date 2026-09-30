import React, { useState } from 'react';
import { Shield, Lock, Cpu, Palette, Bell, Info, Terminal } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const SettingsView: React.FC = () => {
  const [activeSection, setActiveSection] = useState<
    'privacy' | 'permissions' | 'runtime' | 'appearance' | 'notifications' | 'about'
  >('privacy');

  const navTabs = [
    { id: 'privacy', label: 'Privacy', icon: Shield },
    { id: 'permissions', label: 'Permissions', icon: Lock },
    { id: 'runtime', label: 'AI Runtime', icon: Cpu },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'about', label: 'About NOVA', icon: Info },
  ] as const;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Settings & Preferences</h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Manage local privacy options, tool authorization policies, and application settings
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Settings Navigation Tabs (1 col) */}
        <div className="space-y-1">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeSection === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveSection(tab.id)}
                className={`w-full flex items-center space-x-2.5 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                  isActive
                    ? 'bg-slate-900 text-white font-semibold shadow-xs'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Settings Content Panel (3 cols) */}
        <div className="md:col-span-3 space-y-4">
          {activeSection === 'privacy' && (
            <Card title="Privacy Settings">
              <div className="space-y-4 text-xs">
                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Strict Offline Mode</div>
                    <div className="text-[11px] text-slate-500">
                      Disable all remote network requests. All inference remains 100% on-device.
                    </div>
                  </div>
                  <Badge variant="success">ALWAYS ENFORCED</Badge>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Workspace Telemetry</div>
                    <div className="text-[11px] text-slate-500">
                      Zero telemetry or user workspace files are sent to external servers.
                    </div>
                  </div>
                  <Badge variant="neutral">DISABLED</Badge>
                </div>
              </div>
            </Card>
          )}

          {activeSection === 'permissions' && (
            <Card title="Tool Permissions & Guard Policies">
              <div className="space-y-4 text-xs">
                <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl flex items-start space-x-3 text-rose-900">
                  <Terminal className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <div className="font-semibold text-rose-900">Arbitrary Shell Execution Disabled</div>
                    <p className="text-rose-800 leading-relaxed text-[11px]">
                      The AI assistant is hard-blocked from invoking raw PowerShell or CMD scripts directly on your host machine.
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Mandatory User Confirmation</div>
                    <div className="text-[11px] text-slate-500">
                      Sensitive actions (file writes, deletes, registered app launchers) require human authorization.
                    </div>
                  </div>
                  <Badge variant="info">ENABLED</Badge>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Immutable Audit Logging</div>
                    <div className="text-[11px] text-slate-500">
                      Every tool request and validation result is logged to local SQLite DB (<code className="text-cyan-700">nova_workspace.db</code>).
                    </div>
                  </div>
                  <Badge variant="success">ACTIVE</Badge>
                </div>
              </div>
            </Card>
          )}

          {activeSection === 'runtime' && (
            <Card title="AI Runtime & Snapdragon Acceleration">
              <div className="space-y-4 text-xs">
                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Qualcomm Snapdragon NPU Target</div>
                    <div className="text-[11px] text-slate-500">
                      Architectural isolation in <code className="text-amber-700 font-mono">qualcomm/</code> package.
                    </div>
                  </div>
                  <Badge variant="warning">ISOLATED FALLBACK</Badge>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Development Fallback Engine</div>
                    <div className="text-[11px] text-slate-500">
                      Allows NOVA to remain fully functional during local development without physical Snapdragon NPU hardware.
                    </div>
                  </div>
                  <Badge variant="success">READY</Badge>
                </div>
              </div>
            </Card>
          )}

          {activeSection === 'appearance' && (
            <Card title="Appearance & Visual Theme">
              <div className="space-y-4 text-xs">
                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Desktop Product Theme</div>
                    <div className="text-[11px] text-slate-500">
                      Light Premium AI Product Theme (Soft Slate / Cyan accents).
                    </div>
                  </div>
                  <Badge variant="info">LIGHT PREMIUM (DEFAULT)</Badge>
                </div>
              </div>
            </Card>
          )}

          {activeSection === 'notifications' && (
            <Card title="System Notifications">
              <div className="space-y-4 text-xs">
                <div className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-900">Permission Action Dialogs</div>
                    <div className="text-[11px] text-slate-500">
                      Display authorization modal whenever a sensitive workspace tool is requested.
                    </div>
                  </div>
                  <Badge variant="success">ENABLED</Badge>
                </div>
              </div>
            </Card>
          )}

          {activeSection === 'about' && (
            <Card title="About NOVA Workspace Assistant">
              <div className="space-y-4 text-xs">
                <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2">
                  <div className="flex items-center space-x-2.5">
                    <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xs shadow-xs">
                      N
                    </div>
                    <span className="font-bold text-base text-slate-900">NOVA Workspace Assistant</span>
                    <span className="text-[10px] font-mono bg-white text-cyan-700 px-2 py-0.5 rounded-full border border-cyan-200">
                      v0.1.0-dev
                    </span>
                  </div>
                  <p className="text-slate-600 leading-relaxed text-xs">
                    Built for the <strong>Snapdragon AI Lab Build & Present Challenge</strong>. NOVA is a privacy-first, on-device AI workspace assistant designed for Windows desktop productivity.
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-3 font-mono text-[11px] text-slate-500">
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    Target OS: Windows 11 / x64 / ARM64
                  </div>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    Backend: Python FastAPI + SQLite
                  </div>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
