import React, { useState, useRef } from 'react';
import { Eye, Camera, Sparkles, AlertCircle, Image as ImageIcon, X, ShieldCheck } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';

export const VisionView: React.FC = () => {
  const [capturedImageUrl, setCapturedImageUrl] = useState<string | null>(null);
  const [capturedImageName, setCapturedImageName] = useState<string | null>(null);
  const [analysisStatus, setAnalysisStatus] = useState<string>('Awaiting Image Input');
  const [captureError, setCaptureError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // 1. Screen Capture via Browser getDisplayMedia API
  const handleCaptureScreenshot = async () => {
    setCaptureError(null);
    if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
      setCaptureError('Screen capture API is not supported in this browser.');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
      const video = document.createElement('video');
      video.srcObject = stream;
      await video.play();

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 1280;
      canvas.height = video.videoHeight || 720;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/png');
        setCapturedImageUrl(dataUrl);
        setCapturedImageName(`nova-vision-${Date.now()}.png`);
        setAnalysisStatus('Desktop Screen Frame Captured');
      }

      // Stop stream video tracks immediately
      stream.getTracks().forEach((track) => track.stop());
    } catch (err: any) {
      if (err.name !== 'NotAllowedError') {
        setCaptureError(err.message || 'Failed to capture desktop screen.');
      }
    }
  };

  // 2. File Upload Dropzone
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setCapturedImageUrl(event.target.result as string);
          setCapturedImageName(file.name);
          setAnalysisStatus(`Loaded Local Image: ${file.name}`);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyzeClick = () => {
    if (!capturedImageUrl) return;
    setAnalysisStatus('Local Visual Pixels Ready (Pending On-Device VLM weight initialization)');
  };

  return (
    <div className="space-y-6">
      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept="image/png,image/jpeg,image/webp"
        className="hidden"
      />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Visual Intelligence Workspace</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            On-device vision analysis for local screen frames and workspace images (100% On-Device Privacy)
          </p>
        </div>
        <Badge variant="neutral" icon={<Eye className="w-3.5 h-3.5 text-cyan-600" />}>
          Local VLM Interface
        </Badge>
      </div>

      {/* Capture Error Toast */}
      {captureError && (
        <div className="p-3.5 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-center justify-between">
          <span className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
            <span>{captureError}</span>
          </span>
          <button
            onClick={() => setCaptureError(null)}
            className="text-red-700 font-bold hover:underline cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Dropzone & Image Canvas */}
        <Card title="Image & Screen Frame Input">
          <div className="space-y-4">
            <div
              onClick={handleCaptureScreenshot}
              className="border-2 border-dashed border-slate-200 hover:border-cyan-500/60 rounded-2xl p-8 text-center bg-slate-50/60 transition-all cursor-pointer space-y-3"
            >
              <div className="p-3 rounded-2xl bg-white border border-slate-200 text-cyan-600 inline-block shadow-xs">
                <Camera className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <div className="text-xs font-semibold text-slate-900">
                  Click to capture desktop screen frame via browser API
                </div>
                <div className="text-[11px] text-slate-500">
                  Supports PNG, JPG, WebP. Images remain 100% on local device memory.
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs pt-1">
              <span className="text-slate-500 font-medium">Alternative file input:</span>
              <Button
                variant="outline"
                size="sm"
                icon={<ImageIcon className="w-3.5 h-3.5 text-cyan-600" />}
                onClick={() => fileInputRef.current?.click()}
              >
                Select Local Image File
              </Button>
            </div>

            {capturedImageUrl && (
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-slate-900 truncate">Preview: {capturedImageName}</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    icon={<X className="w-3.5 h-3.5" />}
                    onClick={() => {
                      setCapturedImageUrl(null);
                      setCapturedImageName(null);
                      setAnalysisStatus('Awaiting Image Input');
                    }}
                  >
                    Remove
                  </Button>
                </div>

                <div className="p-2 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-center">
                  <img
                    src={capturedImageUrl}
                    alt="Captured or uploaded workspace image"
                    className="max-h-56 object-contain rounded-lg"
                  />
                </div>

                <Button
                  variant="gradient"
                  size="md"
                  className="w-full"
                  icon={<Sparkles className="w-4 h-4" />}
                  onClick={handleAnalyzeClick}
                >
                  Inspect Visual Frame
                </Button>
              </div>
            )}
          </div>
        </Card>

        {/* Right Column: Analysis Output Panel */}
        <Card title="Vision Inspection Panel">
          <div className="space-y-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 flex items-center justify-between">
              <span className="text-slate-500">Analysis Status:</span>
              <span className="font-mono font-semibold text-cyan-800">{analysisStatus}</span>
            </div>

            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-1.5 text-xs text-emerald-950">
              <div className="flex items-center space-x-2 font-semibold text-emerald-900">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>On-Device Privacy Preserved</span>
              </div>
              <p className="text-emerald-800 text-[11px] leading-relaxed">
                Screen pixels are processed strictly in local browser memory. Zero images or desktop telemetry leave your machine.
              </p>
            </div>

            <div className="space-y-2">
              <div className="text-slate-500 font-bold text-[10px] uppercase tracking-wider">
                Visual Inspection Metadata
              </div>
              <div className="p-4 bg-slate-900 text-slate-100 rounded-xl border border-slate-800 text-[11px] font-mono space-y-1">
                <div>&#123;</div>
                <div className="pl-4">"source": "{capturedImageName || 'No image loaded'}",</div>
                <div className="pl-4">"status": "{analysisStatus}",</div>
                <div className="pl-4">"local_privacy": "100% On-Device",</div>
                <div className="pl-4">"vlm_target": "Snapdragon Local VLM Adapter"</div>
                <div>&#125;</div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
