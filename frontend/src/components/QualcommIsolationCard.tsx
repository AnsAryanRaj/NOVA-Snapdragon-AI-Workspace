import React from 'react';
import { Cpu, Layers, CheckCircle, Info } from 'lucide-react';

export const QualcommIsolationCard: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex items-center space-x-3 border-b border-slate-800 pb-3">
        <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
          <Cpu className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-semibold text-slate-100 text-sm">Qualcomm Snapdragon NPU Isolation Architecture</h3>
          <p className="text-xs text-slate-400">Hardware Abstraction Layer isolating AI Hub & GenieX bindings</p>
        </div>
      </div>

      <div className="space-y-3 text-xs text-slate-300">
        <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-amber-400 font-semibold">
            <Layers className="w-4 h-4" />
            <span>Architectural Isolation Boundary (`qualcomm/` directory)</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            All Qualcomm Snapdragon AI Hub, GenieX runtime bindings, NPU memory management, and ONNX/QNN model loaders reside in the isolated <code className="text-amber-300 bg-slate-900 px-1 py-0.5 rounded border border-slate-800">qualcomm/</code> package. Core workspace logic interacts solely via abstract interfaces.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 space-y-1">
            <div className="flex items-center space-x-1.5 text-emerald-400 font-semibold">
              <CheckCircle className="w-4 h-4" />
              <span>Development Fallback Support</span>
            </div>
            <p className="text-slate-400 text-[11px]">
              The application remains fully functional during local development when Qualcomm NPU hardware or GenieX runtimes are not present.
            </p>
          </div>

          <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 space-y-1">
            <div className="flex items-center space-x-1.5 text-cyan-400 font-semibold">
              <Info className="w-4 h-4" />
              <span>Metrics & Benchmarks Integrity</span>
            </div>
            <p className="text-slate-400 text-[11px]">
              No artificial or fake Snapdragon NPU performance metrics are produced. Benchmarks are reported only when measured live on physical NPU hardware.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
