import React, { useState, useEffect } from 'react';
import { Search, Filter, Folder, FileCode, Info, Shield, Hash, Loader2 } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { FileRow } from '../components/ui/FileRow';
import { PermissionModal } from '../components/ui/PermissionModal';
import type { WorkspaceFile, FileItemSchema, FileHashResponse } from '../types';

export const WorkspaceView: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'code' | 'document' | 'data'>('all');
  const [selectedFile, setSelectedFile] = useState<WorkspaceFile | null>(null);
  const [fileHash, setFileHash] = useState<string | null>(null);
  const [hashingLoading, setHashingLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [apiFiles, setApiFiles] = useState<WorkspaceFile[]>([]);
  const [showPermissionModal, setShowPermissionModal] = useState(false);
  const [pendingActionTitle] = useState('Workspace Read Operation');

  // Fetch workspace files from real backend API
  const fetchWorkspaceFiles = async (query: string = '') => {
    setLoading(true);
    try {
      let url = '/api/v1/workspace/files';
      if (query.trim()) {
        url = `/api/v1/workspace/search?q=${encodeURIComponent(query.trim())}`;
      }
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        const rawItems: FileItemSchema[] = query.trim() ? data.results : data.items;
        
        const mapped: WorkspaceFile[] = (rawItems || []).map((item, idx) => ({
          id: `file-${idx}-${item.name}`,
          name: item.name,
          path: item.relative_path,
          size: `${(item.size_bytes / 1024).toFixed(1)} KB`,
          type: (item.category.toLowerCase() as WorkspaceFile['type']) || 'code',
          lastModified: item.modified_time.split('T')[0],
          isIndexed: true,
        }));
        setApiFiles(mapped);
      }
    } catch {
      setApiFiles([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkspaceFiles(searchQuery);
  }, [searchQuery]);

  const filteredFiles = apiFiles.filter((file) => {
    if (selectedFilter === 'all') return true;
    return file.type === selectedFilter;
  });

  const handleCalculateHash = async () => {
    if (!selectedFile) return;
    setHashingLoading(true);
    setFileHash(null);
    try {
      const res = await fetch(`/api/v1/workspace/hash?path=${encodeURIComponent(selectedFile.path)}`);
      if (res.ok) {
        const data: FileHashResponse = await res.json();
        setFileHash(data.sha256_hash);
      } else {
        setFileHash('Failed to compute SHA256 (Directory or unsupported item)');
      }
    } catch {
      setFileHash('Network error computing SHA256');
    } fontFinally: {
      setHashingLoading(false);
    }
  };

  const [authorizedNotice, setAuthorizedNotice] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {/* Permission Modal */}
      {selectedFile && (
        <PermissionModal
          isOpen={showPermissionModal}
          onClose={() => setShowPermissionModal(false)}
          onConfirm={() => {
            setShowPermissionModal(false);
            setAuthorizedNotice(`Action '${pendingActionTitle}' authorized for '${selectedFile.name}' and logged to audit trail.`);
          }}
          actionTitle={pendingActionTitle}
          actionDescription={`Execute workspace action on '${selectedFile.name}'.`}
          targetPath={selectedFile.path}
        />
      )}

      {authorizedNotice && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-950 rounded-xl text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{authorizedNotice}</span>
          </div>
          <button
            onClick={() => setAuthorizedNotice(null)}
            className="text-[11px] text-emerald-700 font-semibold underline cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Header Info Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
        <div className="flex items-center space-x-3.5">
          <div className="p-3 rounded-xl bg-cyan-50 border border-cyan-100 text-cyan-600">
            <Folder className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Active Controlled Workspace</div>
            <div className="text-sm font-mono font-semibold text-slate-900">d:\Nova Snapdragon\test_workspace</div>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-600 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200/80">
          <Shield className="w-3.5 h-3.5 text-emerald-600" />
          <span>Strict Scope Validation Active</span>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search workspace files..."
            className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-cyan-500 shadow-2xs"
          />
        </div>

        <div className="flex items-center space-x-1.5 self-start sm:self-auto text-xs">
          <span className="text-slate-500 text-[11px] mr-1 flex items-center gap-1 font-medium">
            <Filter className="w-3 h-3" /> Filter:
          </span>
          {(['all', 'code', 'document', 'data'] as const).map((filter) => (
            <button
              key={filter}
              onClick={() => setSelectedFilter(filter)}
              className={`px-3 py-1 rounded-lg text-xs font-medium capitalize transition-colors cursor-pointer ${
                selectedFilter === filter
                  ? 'bg-slate-900 text-white font-semibold shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Main Files Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Files Table (2 cols) */}
        <div className="lg:col-span-2">
          <Card className="p-0 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 font-semibold uppercase text-[10px] border-b border-slate-200/80">
                  <tr>
                    <th className="px-5 py-3">File Name</th>
                    <th className="px-5 py-3">Relative Path</th>
                    <th className="px-5 py-3">Type</th>
                    <th className="px-5 py-3">Size</th>
                    <th className="px-5 py-3">Modified</th>
                    <th className="px-5 py-3 text-right">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={6} className="text-center py-8 text-slate-400 font-mono text-xs">
                        <Loader2 className="w-4 h-4 animate-spin inline mr-2 text-cyan-600" />
                        Scanning test_workspace directory...
                      </td>
                    </tr>
                  ) : filteredFiles.length > 0 ? (
                    filteredFiles.map((file) => (
                      <FileRow
                        key={file.id}
                        file={file}
                        isSelected={selectedFile?.id === file.id}
                        onSelect={(f) => {
                          setSelectedFile(f);
                          setFileHash(null);
                        }}
                      />
                    ))
                  ) : (
                    <tr>
                      <td colSpan={6} className="text-center py-8 text-slate-400 text-xs">
                        No workspace files matched query.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* Selected File Details & Real Actions Panel (1 col) */}
        <div>
          <Card title="File Details & SHA-256 Checksum">
            {selectedFile ? (
              <div className="space-y-4 text-xs">
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 space-y-2">
                  <div className="flex items-center space-x-2 font-semibold text-slate-900">
                    <FileCode className="w-4 h-4 text-cyan-600" />
                    <span>{selectedFile.name}</span>
                  </div>
                  <div className="space-y-1 text-[11px] text-slate-500 font-mono">
                    <div>Path: {selectedFile.path}</div>
                    <div>Size: {selectedFile.size}</div>
                    <div>Modified: {selectedFile.lastModified}</div>
                  </div>
                </div>

                {/* Real SHA256 Calculation Button */}
                <div className="space-y-2">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Security Verification Tool
                  </div>

                  <Button
                    variant="outline"
                    size="sm"
                    className="w-full justify-start text-slate-700"
                    icon={hashingLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-600" /> : <Hash className="w-3.5 h-3.5 text-cyan-600" />}
                    onClick={handleCalculateHash}
                    disabled={hashingLoading}
                  >
                    {hashingLoading ? 'Computing SHA-256 Hash...' : 'Calculate SHA-256 Checksum'}
                  </Button>

                  {fileHash && (
                    <div className="p-3 bg-slate-900 text-slate-100 rounded-xl font-mono text-[10px] break-all border border-slate-800">
                      <div className="text-cyan-400 font-semibold text-[9px] uppercase mb-1">SHA-256 Digest:</div>
                      {fileHash}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-slate-400 text-xs space-y-2">
                <Info className="w-6 h-6 mx-auto text-slate-400" />
                <p>Select a file from the workspace list to view details & calculate SHA-256.</p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
