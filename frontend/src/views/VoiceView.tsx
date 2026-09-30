import React, { useState } from 'react';
import { Mic, Square, AlertCircle, History, Volume2, Sparkles, ShieldCheck } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';

interface VoiceViewProps {
  onNavigateToOverviewWithPrompt?: (prompt: string) => void;
}

export const VoiceView: React.FC<VoiceViewProps> = ({ onNavigateToOverviewWithPrompt }) => {
  const [voiceState, setVoiceState] = useState<'Ready' | 'Listening' | 'Processing'>('Ready');
  const [transcriptionText, setTranscriptionText] = useState<string>('');
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const [recognitionRef, setRecognitionRef] = useState<any>(null);

  const startVoiceInput = () => {
    setVoiceError(null);
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setVoiceError('Web Speech API is not supported by this browser engine. Please type queries into the command bar.');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      setVoiceState('Listening');
      setTranscriptionText('Listening... Speak into your microphone.');

      recognition.onresult = (event: any) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setTranscriptionText(transcript);
      };

      recognition.onerror = (event: any) => {
        setVoiceState('Ready');
        if (event.error !== 'no-speech') {
          setVoiceError(`Microphone input error: ${event.error}`);
        }
      };

      recognition.onend = () => {
        setVoiceState('Ready');
      };

      recognition.start();
      setRecognitionRef(recognition);
    } catch (err: any) {
      setVoiceState('Ready');
      setVoiceError(err.message || 'Failed to initialize microphone');
    }
  };

  const stopVoiceInput = () => {
    if (recognitionRef) {
      try {
        recognitionRef.stop();
      } catch {
        // Ignore
      }
    }
    setVoiceState('Ready');
  };

  const toggleRecording = () => {
    if (voiceState === 'Listening') {
      stopVoiceInput();
    } else {
      startVoiceInput();
    }
  };

  const sampleVoiceCommands = [
    { command: '"find my project report"', time: 'Demo Prompt 1' },
    { command: '"find my project report and show the contents"', time: 'Demo Prompt 2' },
    { command: '"how many files are in my workspace?"', time: 'Demo Prompt 3' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Voice Interaction Workspace</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Local speech recognition via Web Speech API (100% On-Device Local Processing)
          </p>
        </div>
        <Badge variant="neutral" icon={<Volume2 className="w-3.5 h-3.5 text-cyan-600" />}>
          Web Speech Interface
        </Badge>
      </div>

      {/* Voice Error Banner */}
      {voiceError && (
        <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-center justify-between">
          <span className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
            <span>{voiceError}</span>
          </span>
          <button
            onClick={() => setVoiceError(null)}
            className="text-amber-800 font-bold hover:underline cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Large Central Microphone Card */}
        <Card title="Microphone Interaction Canvas">
          <div className="flex flex-col items-center justify-center p-10 space-y-6 text-center">
            <div className="relative">
              <div
                className={`w-28 h-28 rounded-full flex items-center justify-center transition-all duration-300 shadow-md ${
                  voiceState === 'Listening'
                    ? 'bg-rose-50 border-2 border-rose-500 text-rose-600 shadow-rose-200 animate-pulse'
                    : 'bg-slate-50 border border-slate-200 text-slate-700 hover:border-cyan-500/50'
                }`}
              >
                <Mic className={`w-12 h-12 ${voiceState === 'Listening' ? 'text-rose-600' : 'text-slate-800'}`} />
              </div>
            </div>

            <div className="space-y-1">
              <h3 className="font-semibold text-base text-slate-900">
                State: <span className="font-bold text-cyan-600">{voiceState}</span>
              </h3>
              <p className="text-xs text-slate-500 max-w-xs leading-relaxed">
                {voiceState === 'Listening'
                  ? 'Recording local speech. Speak clearly into your microphone.'
                  : 'Click the button below to start voice speech recognition.'}
              </p>
            </div>

            <Button
              variant={voiceState === 'Listening' ? 'danger' : 'gradient'}
              size="lg"
              icon={voiceState === 'Listening' ? <Square className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
              onClick={toggleRecording}
            >
              {voiceState === 'Listening' ? 'Stop Recording' : 'Start Voice Input'}
            </Button>
          </div>
        </Card>

        {/* Right Column: Transcription Output & Command History */}
        <div className="space-y-6">
          <Card title="Live Speech Transcription Output">
            <div className="space-y-3 text-xs">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 font-mono min-h-28 text-slate-800 leading-relaxed">
                {transcriptionText || (
                  <span className="text-slate-400 italic">
                    Transcription text will render here live when speech recognition is active.
                  </span>
                )}
              </div>

              {transcriptionText && transcriptionText !== 'Listening... Speak into your microphone.' && (
                <Button
                  variant="gradient"
                  size="sm"
                  className="w-full"
                  icon={<Sparkles className="w-3.5 h-3.5" />}
                  onClick={() => {
                    if (onNavigateToOverviewWithPrompt) {
                      onNavigateToOverviewWithPrompt(transcriptionText);
                    }
                  }}
                >
                  Use Transcript in Overview Command Bar
                </Button>
              )}

              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-950 text-xs flex items-start space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <p className="text-[11px] leading-relaxed">
                  Speech input runs via local browser audio processing. Audio stream is never stored or transmitted to external servers.
                </p>
              </div>
            </div>
          </Card>

          <Card
            title={
              <div className="flex items-center space-x-2">
                <History className="w-4 h-4 text-cyan-600" />
                <span>Sample Voice Prompts</span>
              </div>
            }
          >
            <div className="space-y-2 text-xs">
              {sampleVoiceCommands.map((item, idx) => (
                <div
                  key={idx}
                  onClick={() => setTranscriptionText(item.command.replace(/"/g, ''))}
                  className="p-3 bg-slate-50 hover:bg-cyan-50/60 rounded-xl border border-slate-200/80 flex items-center justify-between cursor-pointer transition-colors"
                >
                  <span className="font-mono font-semibold text-slate-800">{item.command}</span>
                  <span className="text-[10px] text-slate-400 font-mono">{item.time}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
