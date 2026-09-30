import React from 'react';
import { Wrench, CheckCircle, AlertTriangle } from 'lucide-react';
import type { ToolDefinition } from '../types';

export const ToolRegistryCard: React.FC = () => {
  const registeredTools: ToolDefinition[] = [
    {
      id: 'tool_workspace_index',
      name: 'Workspace File Indexer',
      category: 'file',
      description: 'Scans and indexes workspace document metadata for local semantic search.',
      is_destructive: false,
      requires_confirmation: false,
      status: 'registered',
    },
    {
      id: 'tool_doc_parser',
      name: 'Document Content Reader',
      category: 'document',
      description: 'Parses local markdown, text, and PDF files within permitted workspace scope.',
      is_destructive: false,
      requires_confirmation: false,
      status: 'registered',
    },
    {
      id: 'tool_file_writer',
      name: 'Workspace File Writer',
      category: 'file',
      description: 'Creates or edits files inside the explicit user workspace boundary.',
      is_destructive: true,
      requires_confirmation: true,
      status: 'registered',
    },
    {
      id: 'tool_sys_util',
      name: 'Windows App Launcher (Registered)',
      category: 'system',
      description: 'Launches specific whitelisted Windows applications via registered handler.',
      is_destructive: false,
      requires_confirmation: true,
      status: 'registered',
    },
    {
      id: 'tool_whisper_voice',
      name: 'Whisper Local Speech Transcriber',
      category: 'voice',
      description: 'Speech-to-text processing using local Whisper engine (isolated setup).',
      is_destructive: false,
      requires_confirmation: false,
      status: 'isolated',
    },
    {
      id: 'tool_qualcomm_npu',
      name: 'Qualcomm GenieX NPU Adapter',
      category: 'qualcomm',
      description: 'Snapdragon NPU hardware inference adapter (Architecturally isolated).',
      is_destructive: false,
      requires_confirmation: false,
      status: 'isolated',
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            <Wrench className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-sm">Tool Action Registry Ledger</h3>
            <p className="text-xs text-slate-400">Explicit allowed action definitions (Arbitrary shell execution is forbidden)</p>
          </div>
        </div>

        <span className="text-xs bg-slate-950 px-2.5 py-1 rounded-md border border-slate-800 text-slate-400">
          Total Tools: <span className="text-cyan-400 font-semibold">{registeredTools.length}</span>
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950 text-slate-400 font-semibold uppercase text-[10px] border-b border-slate-800">
            <tr>
              <th className="px-3 py-2">Tool Name</th>
              <th className="px-3 py-2">Category</th>
              <th className="px-3 py-2">Description</th>
              <th className="px-3 py-2 text-center">Confirmation Policy</th>
              <th className="px-3 py-2 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
            {registeredTools.map((t) => (
              <tr key={t.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="px-3 py-2.5 font-semibold text-slate-200">
                  <div className="flex items-center space-x-1.5 font-sans">
                    <span>{t.name}</span>
                  </div>
                </td>
                <td className="px-3 py-2.5 text-slate-400 capitalize">{t.category}</td>
                <td className="px-3 py-2.5 text-slate-400 font-sans text-xs max-w-xs truncate" title={t.description}>
                  {t.description}
                </td>
                <td className="px-3 py-2.5 text-center font-sans">
                  {t.requires_confirmation ? (
                    <span className="inline-flex items-center space-x-1 text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded text-[10px] border border-amber-800/50">
                      <AlertTriangle className="w-3 h-3" />
                      <span>Confirmation Required</span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center space-x-1 text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded text-[10px] border border-emerald-800/50">
                      <CheckCircle className="w-3 h-3" />
                      <span>Auto-Allowed</span>
                    </span>
                  )}
                </td>
                <td className="px-3 py-2.5 text-center font-sans">
                  {t.status === 'registered' ? (
                    <span className="text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded text-[10px] border border-cyan-800/50">
                      Registered
                    </span>
                  ) : (
                    <span className="text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded text-[10px] border border-amber-800/50">
                      Architecturally Isolated
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
