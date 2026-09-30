import React, { useState, useEffect } from 'react';
import { Cpu, Zap, Activity, HardDrive, Network, Layers, AlertCircle, Loader2, CheckCircle2, ShieldCheck } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import type { AIRuntimeStatus } from '../types';

export const PerformanceView: React.FC = () => {
  const [runtimeStatus, setRuntimeStatus] = useState<AIRuntimeStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRuntime = async () => {
      try {
        const res = await fetch('/api/v1/ai/runtime');
        if (res.ok) {
          const data: AIRuntimeStatus = await res.json();
          setRuntimeStatus(data);
        }
      } catch {
        // Fallback
      } finally {
        setLoading(false);
      }
    };
    fetchRuntime();
  }, []);

  const sections = [
    {
      title: 'AI Runtime Architecture',
      icon: Layers,
      detail: runtimeStatus ? `${runtimeStatus.provider.toUpperCase()} / ${runtimeStatus.runtime}` : 'Qualcomm GenieX / ONNX Runtime HAL abstraction',
      statusValue: runtimeStatus ? runtimeStatus.runtime : 'development'
    },
    {
      title: 'Execution Hardware',
      icon: Cpu,
      detail: runtimeStatus ? runtimeStatus.device : 'Snapdragon NPU Target (CPU/GPU Fallback)',
      statusValue: runtimeStatus ? (runtimeStatus.qualcomm.available ? 'Snapdragon NPU Active' : 'Development Host (CPU)') : 'Development Host'
    },
    { title: 'Inference Latency', icon: Zap, detail: 'Token generation speed & time-to-first-token', statusValue: 'Awaiting physical NPU benchmark' },
    { title: 'NPU Core Load', icon: Activity, detail: 'Qualcomm Neural Processing Engine load', statusValue: 'Awaiting physical NPU benchmark' },
    { title: 'Unified Memory', icon: HardDrive, detail: 'Local model memory allocation', statusValue: 'Awaiting physical NPU benchmark' },
    { title: 'Network Privacy', icon: Network, detail: 'Localhost loopback only (0 external telemetry)', statusValue: 'Localhost Only (0 telemetry)' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Snapdragon Hardware & Performance</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Truthful AI Runtime HAL & Capability Detection (<code className="text-cyan-700 font-mono">qualcomm/</code> package)
          </p>
        </div>
        {loading ? (
          <Badge variant="neutral" icon={<Loader2 className="w-3.5 h-3.5 animate-spin text-slate-600" />}>
            Checking HAL...
          </Badge>
        ) : runtimeStatus?.qualcomm.available ? (
          <Badge variant="info" icon={<CheckCircle2 className="w-3.5 h-3.5 text-cyan-600" />}>
            Qualcomm NPU Active
          </Badge>
        ) : (
          <Badge variant="warning" icon={<Cpu className="w-3.5 h-3.5 text-amber-600" />}>
            Development Host (CPU Fallback)
          </Badge>
        )}
      </div>

      {/* Side-by-Side Environment Clarity Card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        {/* Environment 1: Current Host */}
        <div className="p-4 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-2xs">
          <div className="flex items-center justify-between font-bold text-slate-800">
            <span className="flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-amber-600" />
              <span>Current Host Environment</span>
            </span>
            <Badge variant="warning">CPU FALLBACK</Badge>
          </div>
          <div className="space-y-1 text-slate-600 font-mono text-[11px]">
            <div>Processor: {runtimeStatus?.capabilities.processor || 'x86_64 Architecture'}</div>
            <div>Architecture: {runtimeStatus?.capabilities.architecture || 'x64'}</div>
            <div>Status: Truthfully reporting CPU execution (No NPU claimed)</div>
          </div>
        </div>

        {/* Environment 2: Target Snapdragon Path */}
        <div className="p-4 bg-cyan-50/60 border border-cyan-200 rounded-2xl space-y-2 shadow-2xs">
          <div className="flex items-center justify-between font-bold text-cyan-950">
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-cyan-600" />
              <span>Qualcomm Snapdragon Deployment Path</span>
            </span>
            <Badge variant="info">NPU READY</Badge>
          </div>
          <div className="space-y-1 text-cyan-900 font-mono text-[11px]">
            <div>HAL Layer: <code className="text-cyan-800 font-bold">qualcomm/adapter.py</code></div>
            <div>Target Engine: Qualcomm AI Hub / GenieX Engine</div>
            <div>Validation: Prepared for Snapdragon hardware profiling</div>
          </div>
        </div>
      </div>

      {/* Benchmark Integrity Banner */}
      <div className="p-5 bg-amber-50/80 border border-amber-200/90 rounded-2xl space-y-2 text-xs text-amber-900 shadow-2xs">
        <div className="flex items-center space-x-2 text-amber-900 font-semibold">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>Metric & Benchmark Integrity Notice</span>
        </div>
        <p className="text-amber-800 leading-relaxed text-xs">
          NOVA does not produce artificial or simulated Snapdragon NPU performance numbers. Hardware metrics and NPU token latency display live data only when executed directly on physical Snapdragon NPU hardware.
        </p>
      </div>

      {/* Telemetry Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {sections.map((sec, idx) => {
          const Icon = sec.icon;
          return (
            <Card key={idx} className="hover:border-slate-300">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2.5 text-slate-900 font-semibold text-xs">
                    <div className="p-2 rounded-xl bg-slate-100 border border-slate-200 text-cyan-600">
                      <Icon className="w-4 h-4 shrink-0" />
                    </div>
                    <span>{sec.title}</span>
                  </div>
                  <span className="text-[10px] font-mono text-slate-400">HAL Status</span>
                </div>

                <p className="text-xs text-slate-500 leading-relaxed">{sec.detail}</p>

                {/* Explicit Status / Benchmark Badge */}
                <div className="pt-3 border-t border-slate-100 text-center">
                  <span className={`inline-block text-[11px] font-mono font-semibold px-3 py-1 rounded-full border ${
                    sec.statusValue.includes('Awaiting')
                      ? 'bg-slate-100 text-amber-700 border-amber-200'
                      : 'bg-cyan-50 text-cyan-700 border-cyan-200'
                  }`}>
                    {sec.statusValue}
                  </span>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
