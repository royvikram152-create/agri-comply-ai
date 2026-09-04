import React, { useEffect, useState } from 'react';
import { AppShell } from './components/AppShell';
import { Dashboard } from './pages/Dashboard';
import { ShipmentDetail } from './pages/ShipmentDetail';
import { CreateShipmentModal } from './components/CreateShipmentModal';
import { fetchShipments, fetchAgents } from './api/client';
import { Shipment, AgentInfo } from './types';
import { Bot, Scale, ExternalLink } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedShipmentId, setSelectedShipmentId] = useState<string | null>(null);
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewModal, setShowNewModal] = useState(false);

  const loadData = async () => {
    try {
      const list = await fetchShipments();
      const ags = await fetchAgents();
      setShipments(list);
      setAgents(ags);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectShipment = (id: string) => {
    setSelectedShipmentId(id);
  };

  const handleShipmentCreated = (newShipment: Shipment) => {
    setShipments(prev => [newShipment, ...prev]);
    setSelectedShipmentId(newShipment.id);
  };

  return (
    <AppShell
      activeTab={activeTab}
      setActiveTab={(tab) => {
        setActiveTab(tab);
        if (tab !== 'shipment-detail') setSelectedShipmentId(null);
      }}
      onNewShipmentClick={() => setShowNewModal(true)}
    >
      {selectedShipmentId ? (
        <ShipmentDetail
          shipmentId={selectedShipmentId}
          onBack={() => setSelectedShipmentId(null)}
        />
      ) : activeTab === 'dashboard' || activeTab === 'shipments' ? (
        <Dashboard
          shipments={shipments}
          onSelectShipment={handleSelectShipment}
          onNewShipmentClick={() => setShowNewModal(true)}
        />
      ) : activeTab === 'agents' ? (
        <div className="space-y-6 max-w-5xl mx-auto">
          <div className="p-6 bg-slate-950 border border-slate-800 rounded-2xl">
            <h2 className="text-xl font-bold text-slate-100 flex items-center">
              <Bot className="w-6 h-6 mr-2 text-emerald-400" />
              5 Specialized Agent Capabilities
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Autonomous agents parse, extract, retrieve, check farm records, and aggregate compliance gaps. All status determinations are strictly evaluated by the deterministic firewall.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((ag, idx) => (
              <div key={idx} className="p-5 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-100">{ag.name}</span>
                  <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold rounded-full">
                    {ag.type}
                  </span>
                </div>
                <p className="text-xs text-slate-300">{ag.description}</p>
                <div className="text-[10px] text-slate-500 font-mono">Role: {ag.role}</div>
              </div>
            ))}
          </div>
        </div>
      ) : activeTab === 'regulations' ? (
        <div className="space-y-6 max-w-5xl mx-auto">
          <div className="p-6 bg-slate-950 border border-slate-800 rounded-2xl">
            <h2 className="text-xl font-bold text-slate-100 flex items-center">
              <Scale className="w-6 h-6 mr-2 text-emerald-400" />
              Authoritative EU Regulatory Knowledge Base (RAG Corpus)
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Verified legal references for fresh mangoes (Mangifera indica L.) exported from India to the EU (*Regulation EC 396/2005 & EU 2019/2072*).
            </p>
          </div>

          <div className="space-y-4">
            {/* Regulation 1 */}
            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-slate-100">Regulation (EC) No 396/2005</span>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 border border-blue-500/40 text-[10px] font-bold rounded-full">
                    OFFICIAL SOURCE
                  </span>
                </div>
                <span className="text-xs font-mono text-emerald-400">Pesticide MRL Framework</span>
              </div>
              <p className="text-xs text-slate-300">
                EU harmonised MRL regulation for active substances. Unapproved substances default to the Limit of Quantification (0.01 mg/kg). Operational thresholds in demo evaluate against configured target limits.
              </p>
              <a
                href="https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/home"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center text-xs text-emerald-400 underline"
              >
                View EU Pesticides Database <ExternalLink className="w-3 h-3 ml-1" />
              </a>
            </div>

            {/* Regulation 2 */}
            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-slate-100">Regulation (EU) 2019/2072 (Annex VII, Point 59)</span>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 border border-blue-500/40 text-[10px] font-bold rounded-full">
                    OFFICIAL SOURCE
                  </span>
                </div>
                <span className="text-xs font-mono text-emerald-400">Phytosanitary Protocol</span>
              </div>
              <p className="text-xs text-slate-300">
                Mandatory official phytosanitary certificate issued by APEDA / Plant Quarantine India certifying that fruits have undergone official Vapour Heat Treatment (VHT) at 48°C for 60 min to eliminate <em>Bactrocera dorsalis</em>.
              </p>
              <a
                href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R2072"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center text-xs text-emerald-400 underline"
              >
                View EUR-Lex Regulation (EU) 2019/2072 <ExternalLink className="w-3 h-3 ml-1" />
              </a>
            </div>

            {/* Regulation 3 */}
            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-slate-100">Regulation (EU) 2017/625 (Article 89)</span>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 border border-blue-500/40 text-[10px] font-bold rounded-full">
                    OFFICIAL SOURCE
                  </span>
                </div>
                <span className="text-xs font-mono text-emerald-400">Official Customs Controls</span>
              </div>
              <p className="text-xs text-slate-300">
                Mandatory cross-document consistency checks for net weight, exporter registration, and consignee details across official phytosanitary certificates, packing lists, and commercial invoices.
              </p>
            </div>
          </div>
        </div>
      ) : null}

      <CreateShipmentModal
        isOpen={showNewModal}
        onClose={() => setShowNewModal(false)}
        onShipmentCreated={handleShipmentCreated}
      />
    </AppShell>
  );
}
