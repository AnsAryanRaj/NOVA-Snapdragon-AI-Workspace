import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle2, AlertCircle, Server } from 'lucide-react';
import type { HealthResponse } from '../types';

interface HealthCardProps {
  onStatusUpdate: (connected: boolean, qualcommIsolation: string) => void;
}

export const HealthCard: React.FC<HealthCardProps> = ({ onStatusUpdate }) => {
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [latency, setLatency] = useState<number | null>(null);

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    const startTime = performance.now();
    try {
      const res = await fetch('/api/health');
      const duration = Math.round(performance.now() - startTime);
      setLatency(duration);

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }

      const data: HealthResponse = await res.json();
      setHealthData(data);
      onStatusUpdate(true, data.qualcomm_isolation);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend server');
      setHealthData(null);
      onStatusUpdate(false, 'offline');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 15000); // refresh every 15s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-sm">Backend Health Status</h3>
            <p className="text-xs text-slate-400">Live API check endpoint: GET /api/health</p>
          </div>
        </div>

        <button
          onClick={fetchHealth}
          disabled={loading}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg transition-colors border border-slate-700 disabled:opacity-50 cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-cyan-400' : ''}`} />
          <span>{loading ? 'Pinging...' : 'Check Endpoint'}</span>
        </button>
      </div>

      {error ? (
        <div className="p-4 bg-rose-950/40 border border-rose-800/50 rounded-lg text-rose-300 flex items-start space-x-3 text-xs">
          <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <div className="font-semibold">Connection Error</div>
            <div className="text-rose-400/90 mt-0.5">{error}</div>
            <div className="mt-2 text-slate-400">
              Ensure FastAPI backend is running on <code className="bg-slate-900 px-1 py-0.5 rounded border border-slate-800">http://127.0.0.1:8000</code>.
            </div>
          </div>
        </div>
      ) : healthData ? (
        <div className="space-y-4">
          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block mb-1">API Status</span>
              <span className="font-semibold text-emerald-400 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span className="capitalize">{healthData.status}</span>
              </span>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block mb-1">Service & Version</span>
              <span className="font-semibold text-slate-200">{healthData.version}</span>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block mb-1">Privacy Guarantee</span>
              <span className="font-semibold text-cyan-400">{healthData.privacy_mode}</span>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block mb-1">Response Latency</span>
              <span className="font-mono text-amber-400 font-semibold">{latency} ms</span>
            </div>
          </div>

          {/* Raw JSON Payload */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-[11px] text-slate-400 px-1">
              <span>Raw Health Response</span>
              <span className="font-mono">{healthData.timestamp}</span>
            </div>
            <pre className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-[11px] font-mono text-cyan-300/90 overflow-x-auto max-h-48 scrollbar-thin">
              {JSON.stringify(healthData, null, 2)}
            </pre>
          </div>
        </div>
      ) : null}
    </div>
  );
};
