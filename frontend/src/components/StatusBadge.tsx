import React from 'react';
import { ShipmentStatus } from '../types';
import { AlertTriangle, CheckCircle, Clock, ShieldAlert, XCircle, FileSearch } from 'lucide-react';

interface StatusBadgeProps {
  status: ShipmentStatus | string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const normalized = status.toUpperCase();

  let bgColor = 'bg-slate-800 text-slate-300 border-slate-700';
  let icon = <Clock className="w-4 h-4 mr-1.5" />;
  let label = status;

  switch (normalized) {
    case 'HOLD':
      bgColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30 font-semibold animate-pulse';
      icon = <ShieldAlert className="w-4 h-4 mr-1.5 text-rose-400" />;
      label = '⚠ HOLD (CRITICAL GAPS)';
      break;
    case 'REVIEW_REQUIRED':
    case 'REVIEW':
      bgColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30 font-semibold';
      icon = <AlertTriangle className="w-4 h-4 mr-1.5 text-amber-400" />;
      label = 'REVIEW REQUIRED';
      break;
    case 'READY_FOR_APPROVAL':
    case 'READY':
      bgColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 font-semibold';
      icon = <CheckCircle className="w-4 h-4 mr-1.5 text-emerald-400" />;
      label = 'READY FOR APPROVAL';
      break;
    case 'APPROVED':
      bgColor = 'bg-blue-500/10 text-blue-400 border-blue-500/30 font-bold';
      icon = <CheckCircle className="w-4 h-4 mr-1.5 text-blue-400" />;
      label = 'APPROVED FOR EXPORT';
      break;
    case 'REJECTED':
      bgColor = 'bg-red-500/20 text-red-500 border-red-500/40 font-bold';
      icon = <XCircle className="w-4 h-4 mr-1.5 text-red-400" />;
      label = 'SHIPMENT REJECTED';
      break;
    case 'ANALYZING':
      bgColor = 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
      icon = <FileSearch className="w-4 h-4 mr-1.5 text-indigo-400 animate-spin" />;
      label = 'ANALYZING';
      break;
  }

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-1.5 font-bold',
  };

  return (
    <span className={`inline-flex items-center rounded-full border ${bgColor} ${sizeClasses[size]}`}>
      {icon}
      {label}
    </span>
  );
};
