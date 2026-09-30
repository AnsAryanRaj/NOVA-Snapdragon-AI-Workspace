import React from 'react';
import { type LucideIcon } from 'lucide-react';
import { Button } from './Button';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  badgeText?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  badgeText,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center bg-slate-50/60 rounded-2xl border border-dashed border-slate-200 space-y-3">
      <div className="p-3 rounded-2xl bg-white border border-slate-200/80 text-cyan-600 shadow-xs">
        <Icon className="w-6 h-6" />
      </div>

      <div className="space-y-1 max-w-sm">
        <h4 className="font-semibold text-slate-900 text-sm">{title}</h4>
        <p className="text-xs text-slate-500 leading-relaxed">{description}</p>
      </div>

      {badgeText && (
        <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
          {badgeText}
        </span>
      )}

      {actionLabel && onAction && (
        <Button variant="outline" size="sm" onClick={onAction} className="mt-1">
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
