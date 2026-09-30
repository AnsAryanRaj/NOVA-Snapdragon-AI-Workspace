import React from 'react';
import { ShieldAlert, Terminal, FileCheck, Lock, ScrollText } from 'lucide-react';

export const SecurityCard: React.FC = () => {
  const principles = [
    {
      title: '1. Privacy-First & Offline-First',
      desc: 'NOVA runs entirely on-device. Zero workspace telemetry or sensitive context is sent to remote servers.',
      status: 'ENFORCED',
      statusColor: 'text-emerald-400 bg-emerald-950/60 border-emerald-800',
      icon: Lock,
    },
    {
      title: '2. Arbitrary Shell Execution Disabled',
      desc: 'The AI model is hard-blocked from invoking raw PowerShell/cmd processes directly on your host machine.',
      status: 'STRICT BLOCK',
      statusColor: 'text-rose-400 bg-rose-950/60 border-rose-800',
      icon: Terminal,
    },
    {
      title: '3. Explicit Tool Registry System',
      desc: 'All host operations (file reads, document indexing, system utilities) must be registered with typed schemas.',
      status: 'ACTIVE',
      statusColor: 'text-cyan-400 bg-cyan-950/60 border-cyan-800',
      icon: FileCheck,
    },
    {
      title: '4. Mandatory User Confirmation',
      desc: 'Any action that writes, alters, or deletes files or system state requires human approval.',
      status: 'REQUIRED',
      statusColor: 'text-amber-400 bg-amber-950/60 border-amber-800',
      icon: ShieldAlert,
    },
    {
      title: '5. Immutable Audit Trail',
      desc: 'Every tool request, validation check, user decision, and result is recorded into a local SQLite audit log.',
      status: 'LOGGING',
      statusColor: 'text-indigo-400 bg-indigo-950/60 border-indigo-800',
      icon: ScrollText,
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex items-center space-x-3 border-b border-slate-800 pb-3">
        <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-semibold text-slate-100 text-sm">Security & Governance Architecture</h3>
          <p className="text-xs text-slate-400">Core guardrails enforcing safe workspace interaction</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {principles.map((p, idx) => {
          const Icon = p.icon;
          return (
            <div key={idx} className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2 flex flex-col justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-slate-200 font-semibold text-xs">
                    <Icon className="w-4 h-4 text-cyan-400 shrink-0" />
                    <span>{p.title}</span>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded border font-mono font-semibold ${p.statusColor}`}>
                    {p.status}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{p.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
