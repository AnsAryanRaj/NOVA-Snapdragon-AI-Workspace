import React from 'react';
import { ShieldAlert, AlertTriangle } from 'lucide-react';
import { Modal } from './Modal';
import { Button } from './Button';

interface PermissionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  actionTitle: string;
  actionDescription: string;
  targetPath?: string;
}

export const PermissionModal: React.FC<PermissionModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  actionTitle,
  actionDescription,
  targetPath,
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Security Authorization Required"
      footer={
        <>
          <Button variant="ghost" size="sm" onClick={onClose}>
            Deny Request
          </Button>
          <Button variant="primary" size="sm" onClick={onConfirm}>
            Authorize Action
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        <div className="p-4 bg-amber-50 border border-amber-200/80 rounded-xl flex items-start space-x-3 text-amber-900">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1 text-xs">
            <div className="font-semibold text-amber-900">Action Confirmation Request</div>
            <p className="text-amber-800 leading-relaxed text-[11px]">
              NOVA requires explicit user authorization before executing state-modifying workspace tools.
            </p>
          </div>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/80 space-y-2 text-xs">
          <div className="flex justify-between text-slate-500">
            <span>Requested Action:</span>
            <span className="font-semibold text-slate-900 font-mono">{actionTitle}</span>
          </div>
          <div className="text-slate-600 leading-relaxed">{actionDescription}</div>
          {targetPath && (
            <div className="pt-2 border-t border-slate-200 flex justify-between text-[11px]">
              <span className="text-slate-500">Target Path:</span>
              <span className="text-cyan-700 font-mono truncate max-w-xs">{targetPath}</span>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2 text-[11px] text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-200/80">
          <ShieldAlert className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>Authorization status will be logged to local SQLite Audit Trail.</span>
        </div>
      </div>
    </Modal>
  );
};
