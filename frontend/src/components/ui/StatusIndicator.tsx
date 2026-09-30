import React from 'react';

interface StatusIndicatorProps {
  label: string;
  status?: 'active' | 'ready' | 'secure' | 'offline';
  className?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  label,
  status = 'active',
  className = '',
}) => {
  const dotColors = {
    active: 'bg-emerald-500',
    ready: 'bg-cyan-500',
    secure: 'bg-blue-500',
    offline: 'bg-amber-500',
  };

  return (
    <div className={`inline-flex items-center space-x-1.5 text-xs text-slate-600 font-medium ${className}`}>
      <span className={`w-2 h-2 rounded-full ${dotColors[status]}`} />
      <span>{label}</span>
    </div>
  );
};
