import React from 'react';
import type { ActivityItem } from '../../types';
import { Badge } from './Badge';
import { CheckCircle2, ShieldAlert, Lock, AlertCircle } from 'lucide-react';

interface ActivityRowProps {
  activity: ActivityItem;
}

export const ActivityRow: React.FC<ActivityRowProps> = ({ activity }) => {
  const getStatusBadge = (status: ActivityItem['status']) => {
    switch (status) {
      case 'ALLOWED':
      case 'CONFIRMED':
        return (
          <Badge variant="success" icon={<CheckCircle2 className="w-3 h-3" />}>
            {status}
          </Badge>
        );
      case 'BLOCKED':
        return (
          <Badge variant="danger" icon={<ShieldAlert className="w-3 h-3" />}>
            BLOCKED BY GUARD
          </Badge>
        );
      case 'REQUIRES_CONFIRMATION':
        return (
          <Badge variant="warning" icon={<AlertCircle className="w-3 h-3" />}>
            NEEDS PERMISSION
          </Badge>
        );
      default:
        return <Badge variant="neutral">{status}</Badge>;
    }
  };

  const getPermissionBadge = (permission: ActivityItem['permissionLevel']) => {
    switch (permission) {
      case 'AUTO':
        return (
          <span className="text-[10px] font-mono text-cyan-700 bg-cyan-50 px-2.5 py-0.5 rounded-full border border-cyan-200">
            AUTO ALLOWED
          </span>
        );
      case 'USER_CONFIRMED':
        return (
          <span className="text-[10px] font-mono text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
            USER CONFIRMED
          </span>
        );
      case 'SECURITY_BLOCKED':
        return (
          <span className="text-[10px] font-mono text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
            SECURITY BLOCKED
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <tr className="hover:bg-slate-50/80 transition-colors border-b border-slate-100 text-xs">
      <td className="px-5 py-4 font-medium text-slate-900">
        <div className="space-y-0.5">
          <div className="font-semibold text-slate-900">{activity.action}</div>
          <div className="text-[11px] text-slate-500 font-mono flex items-center space-x-1">
            <Lock className="w-3 h-3 text-cyan-600" />
            <span>{activity.toolName}</span>
          </div>
        </div>
      </td>
      <td className="px-5 py-4 text-slate-500 font-mono text-[11px]">{activity.timestamp}</td>
      <td className="px-5 py-4">{getStatusBadge(activity.status)}</td>
      <td className="px-5 py-4">{getPermissionBadge(activity.permissionLevel)}</td>
      <td className="px-5 py-4 text-slate-600 font-mono text-[11px] max-w-xs truncate" title={activity.result}>
        {activity.result}
      </td>
    </tr>
  );
};
