import React from 'react';
import { AuditEvent } from '../types';
import { Clock, Bot, ShieldCheck, FileText, UserCheck, Activity } from 'lucide-react';

interface TimelineProps {
  events: AuditEvent[];
}

export const Timeline: React.FC<TimelineProps> = ({ events }) => {
  if (!events || events.length === 0) {
    return <div className="text-slate-400 text-xs py-4">No audit events recorded yet.</div>;
  }

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'AGENT_EXECUTION':
      case 'PIPELINE_EXECUTED':
        return <Bot className="w-4 h-4 text-emerald-400" />;
      case 'RULE_EVALUATION':
        return <ShieldCheck className="w-4 h-4 text-amber-400" />;
      case 'REMEDIATION_PERFORMED':
      case 'DOCUMENT_UPLOADED':
        return <FileText className="w-4 h-4 text-blue-400" />;
      case 'APPROVAL_PERFORMED':
        return <UserCheck className="w-4 h-4 text-indigo-400" />;
      default:
        return <Activity className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-700/60">
      {events.map((evt, idx) => (
        <div key={evt.id || idx} className="relative group">
          {/* Node circle icon */}
          <div className="absolute -left-[1.375rem] top-1 p-1 rounded-full bg-slate-900 border border-slate-700 shadow-md">
            {getEventIcon(evt.event_type)}
          </div>

          <div className="bg-slate-950/60 border border-slate-800 p-4 rounded-xl shadow-sm hover:border-slate-700 transition">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-200">{evt.title}</span>
              <span className="text-[10px] text-slate-400 flex items-center font-mono">
                <Clock className="w-3 h-3 mr-1" />
                {new Date(evt.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
            </div>

            {evt.agent_name && (
              <div className="mt-1 text-[11px] font-semibold text-emerald-400 flex items-center">
                <Bot className="w-3 h-3 mr-1" />
                {evt.agent_name}
              </div>
            )}

            <p className="mt-1.5 text-xs text-slate-300 leading-relaxed">{evt.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
