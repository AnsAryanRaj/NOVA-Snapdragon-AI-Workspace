import React from 'react';
import { History, Lock } from 'lucide-react';
import type { AuditLogItem } from '../types';

export const AuditLogCard: React.FC = () => {
  const sampleAuditLogs: AuditLogItem[] = [
    {
      id: 'log-101',
      timestamp: '2026-09-24 13:51:51',
      action_name: 'GET /api/health',
      tool_name: 'System Health Check',
      status: 'SUCCESS',
      execution_time_ms: 12,
    },
    {
      id: 'log-102',
      timestamp: '2026-09-24 13:50:00',
      action_name: 'Shell Execution Attempt',
      tool_name: 'Arbitrary Command Guard',
      status: 'BLOCKED',
      execution_time_ms: 1,
    },
    {
      id: 'log-103',
      timestamp: '2026-09-24 13:48:30',
      action_name: 'Index Workspace Files',
      tool_name: 'Workspace File Indexer',
      status: 'SUCCESS',
      execution_time_ms: 45,
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-sm">Action Audit Log Stream</h3>
            <p className="text-xs text-slate-400">Immutable execution history stored in SQLite `nova_workspace.db`</p>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 text-xs text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800/50">
          <Lock className="w-3.5 h-3.5" />
          <span>Audit Logging Active</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950 text-slate-400 font-semibold uppercase text-[10px] border-b border-slate-800">
            <tr>
              <th className="px-3 py-2">Timestamp</th>
              <th className="px-3 py-2">Action / Endpoint</th>
              <th className="px-3 py-2">Tool Handler</th>
              <th className="px-3 py-2 text-center">Security Result</th>
              <th className="px-3 py-2 text-right">Latency</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
            {sampleAuditLogs.map((log) => (
              <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="px-3 py-2.5 text-slate-400">{log.timestamp}</td>
                <td className="px-3 py-2.5 font-semibold text-slate-200">{log.action_name}</td>
                <td className="px-3 py-2.5 text-slate-400">{log.tool_name}</td>
                <td className="px-3 py-2.5 text-center font-sans">
                  {log.status === 'SUCCESS' ? (
                    <span className="text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded text-[10px] border border-emerald-800/50">
                      SUCCESS
                    </span>
                  ) : (
                    <span className="text-rose-400 bg-rose-950/40 px-2 py-0.5 rounded text-[10px] border border-rose-800/50">
                      BLOCKED BY SECURITY
                    </span>
                  )}
                </td>
                <td className="px-3 py-2.5 text-right text-amber-400">{log.execution_time_ms} ms</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
