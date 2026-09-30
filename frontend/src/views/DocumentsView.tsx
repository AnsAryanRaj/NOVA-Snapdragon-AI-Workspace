import React, { useState, useEffect } from 'react';
import {
  FileText,
  UploadCloud,
  Search,
  AlertCircle,
  Eye,
  Loader2,
  RefreshCw,
  Layers,
  Database,
  CheckCircle2,
  FileCode,
  Sparkles
} from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { EmptyState } from '../components/ui/EmptyState';
import type {
  DocumentMetadataSchema,
  DocumentDetailSchema,
  DocumentSearchResultSchema,
  DocumentStatsSchema,
  IndexingSummarySchema,
  SearchMatchSchema
} from '../types';

export const DocumentsView: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [documentsList, setDocumentsList] = useState<DocumentMetadataSchema[]>([]);
  const [searchResults, setSearchResults] = useState<SearchMatchSchema[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<DocumentDetailSchema | null>(null);
  const [selectedMatch, setSelectedMatch] = useState<SearchMatchSchema | null>(null);
  const [stats, setStats] = useState<DocumentStatsSchema | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [indexing, setIndexing] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [indexingSummary, setIndexingSummary] = useState<IndexingSummarySchema | null>(null);
  const [previewMode, setPreviewMode] = useState<'chunks' | 'full'>('chunks');
  const [selectedLocalFiles, setSelectedLocalFiles] = useState<File[]>([]);
  const docFileInputRef = React.useRef<HTMLInputElement | null>(null);

  // Load document list and stats on mount
  const loadData = async () => {
    setLoading(true);
    try {
      const [listRes, statsRes] = await Promise.all([
        fetch('/api/v1/documents/list'),
        fetch('/api/v1/documents/stats')
      ]);

      if (listRes.ok) {
        const docs: DocumentMetadataSchema[] = await listRes.json();
        setDocumentsList(docs);
      }
      if (statsRes.ok) {
        const st: DocumentStatsSchema = await statsRes.json();
        setStats(st);
      }
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Handle lexical search query
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setSelectedMatch(null);
      return;
    }

    const timer = setTimeout(async () => {
      setSearchLoading(true);
      try {
        const res = await fetch(`/api/v1/documents/search?q=${encodeURIComponent(searchQuery.trim())}`);
        if (res.ok) {
          const data: DocumentSearchResultSchema = await res.json();
          setSearchResults(data.matches);
        }
      } catch {
        setSearchResults([]);
      } finally {
        setSearchLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Trigger workspace indexing
  const handleTriggerIndexing = async () => {
    setIndexing(true);
    setIndexingSummary(null);
    try {
      const res = await fetch('/api/v1/documents/index', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ force_reindex: false })
      });
      if (res.ok) {
        const summary: IndexingSummarySchema = await res.json();
        setIndexingSummary(summary);
        await loadData();
      }
    } catch {
      // Error handling
    } finally {
      setIndexing(false);
    }
  };

  // Select document to view metadata and chunks
  const handleSelectDoc = async (docId: string) => {
    setSelectedMatch(null);
    setDetailLoading(true);
    try {
      const res = await fetch(`/api/v1/documents/${encodeURIComponent(docId)}`);
      if (res.ok) {
        const detail: DocumentDetailSchema = await res.json();
        setSelectedDoc(detail);
      }
    } catch {
      setSelectedDoc(null);
    } finally {
      setDetailLoading(false);
    }
  };

  // Select search match
  const handleSelectMatch = async (match: SearchMatchSchema) => {
    setSelectedMatch(match);
    await handleSelectDoc(match.doc_id);
  };

  const formatBytes = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Document Workspace</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Local document extraction, deterministic chunking, and lexical search (`test_workspace`)
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleTriggerIndexing}
            disabled={indexing}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-2xs transition-all disabled:opacity-60 cursor-pointer"
          >
            {indexing ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-600" />
            ) : (
              <RefreshCw className="w-3.5 h-3.5 text-cyan-600" />
            )}
            <span>{indexing ? 'Indexing Workspace...' : 'Index Workspace'}</span>
          </button>

          <div className="relative w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3.5 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search document chunks & terms..."
              className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-cyan-500 shadow-2xs"
            />
            {searchLoading && (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-600 absolute right-3 top-2.5" />
            )}
          </div>
        </div>
      </div>

      {/* Index Summary Toast / Banner */}
      {indexingSummary && (
        <div className="p-3.5 bg-cyan-50/80 border border-cyan-200 rounded-2xl flex items-center justify-between text-xs text-cyan-950 shadow-2xs">
          <div className="flex items-center gap-2 font-medium">
            <CheckCircle2 className="w-4 h-4 text-cyan-600 shrink-0" />
            <span>
              Indexing Complete: Found {indexingSummary.total_found} files, indexed {indexingSummary.indexed_new} new, updated {indexingSummary.updated}, generated {indexingSummary.total_chunks} chunks in {indexingSummary.duration_ms}ms.
            </span>
          </div>
          <button
            onClick={() => setIndexingSummary(null)}
            className="text-[11px] text-cyan-700 hover:text-cyan-900 font-semibold underline cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Index Stats Bar */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="bg-white p-3.5 rounded-2xl border border-slate-200/80 flex items-center gap-3 shadow-2xs">
            <div className="p-2.5 rounded-xl bg-slate-100 text-slate-700">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[11px] font-medium text-slate-500">Indexed Documents</div>
              <div className="text-base font-bold text-slate-900 font-mono">{stats.total_documents}</div>
            </div>
          </div>

          <div className="bg-white p-3.5 rounded-2xl border border-slate-200/80 flex items-center gap-3 shadow-2xs">
            <div className="p-2.5 rounded-xl bg-cyan-50 text-cyan-600">
              <Layers className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[11px] font-medium text-slate-500">Total Chunks</div>
              <div className="text-base font-bold text-slate-900 font-mono">{stats.total_chunks}</div>
            </div>
          </div>

          <div className="bg-white p-3.5 rounded-2xl border border-slate-200/80 flex items-center gap-3 shadow-2xs">
            <div className="p-2.5 rounded-xl bg-slate-100 text-slate-700">
              <Database className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[11px] font-medium text-slate-500">Index Size</div>
              <div className="text-base font-bold text-slate-900 font-mono">{formatBytes(stats.total_size_bytes)}</div>
            </div>
          </div>

          <div className="bg-white p-3.5 rounded-2xl border border-slate-200/80 flex items-center gap-3 shadow-2xs">
            <div className="p-2.5 rounded-xl bg-cyan-50 text-cyan-600">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[11px] font-medium text-slate-500">File Formats</div>
              <div className="text-xs font-semibold text-slate-700 font-mono truncate">
                {Object.keys(stats.documents_by_type).join(', ') || 'None'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Upload Target Drop Zone & File Selector */}
      <input
        type="file"
        ref={docFileInputRef}
        onChange={(e) => {
          if (e.target.files && e.target.files.length > 0) {
            setSelectedLocalFiles(Array.from(e.target.files));
          }
        }}
        multiple
        className="hidden"
      />

      <div
        onClick={() => docFileInputRef.current?.click()}
        className="border-2 border-dashed border-slate-200 hover:border-cyan-500/60 rounded-2xl p-6 text-center bg-white/80 transition-all cursor-pointer space-y-2 shadow-2xs group"
      >
        <div className="p-3 rounded-2xl bg-cyan-50 text-cyan-600 inline-block border border-cyan-100 shadow-xs group-hover:scale-105 transition-transform">
          <UploadCloud className="w-6 h-6" />
        </div>
        <div className="space-y-0.5">
          <div className="text-xs font-semibold text-slate-900">
            Select Local Document / Workspace File
          </div>
          <div className="text-[11px] text-slate-500">
            Click to open native file browser. Supports PDF, Markdown, TXT, CSV, Python, and C++. 100% On-Device Privacy.
          </div>
        </div>
      </div>

      {selectedLocalFiles.length > 0 && (
        <div className="p-4 bg-white border border-slate-200/80 rounded-2xl space-y-3 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Selected Local Files ({selectedLocalFiles.length})
            </span>
            <button
              onClick={() => setSelectedLocalFiles([])}
              className="text-[11px] text-slate-500 hover:text-slate-800 font-semibold cursor-pointer"
            >
              Clear Selection
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {selectedLocalFiles.map((f, i) => (
              <div key={i} className="p-3 bg-slate-50 rounded-xl border border-slate-200/60 text-xs flex items-center justify-between">
                <div className="truncate pr-2">
                  <div className="font-semibold text-slate-900 truncate">{f.name}</div>
                  <div className="text-[10px] text-slate-500 font-mono">
                    {(f.size / 1024).toFixed(1)} KB • {f.type || 'local file'}
                  </div>
                </div>
                <Badge variant="info">Local</Badge>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-slate-500 italic">
            To make these documents searchable by NOVA, place them into <code className="font-mono bg-slate-100 px-1 py-0.5 rounded text-slate-800">test_workspace</code> and click "Index Workspace" above.
          </p>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Documents / Search Matches List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between px-1">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              {searchQuery.trim() ? `Search Matches (${searchResults.length})` : `Workspace Documents (${documentsList.length})`}
            </div>
            {searchQuery.trim() && (
              <button
                onClick={() => setSearchQuery('')}
                className="text-[11px] text-cyan-600 font-semibold hover:underline cursor-pointer"
              >
                Clear Search
              </button>
            )}
          </div>

          {loading ? (
            <div className="py-12 text-center text-slate-400 text-xs">
              <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2 text-cyan-600" />
              Loading workspace document index...
            </div>
          ) : searchQuery.trim() ? (
            /* Search Results List */
            searchResults.length > 0 ? (
              <div className="space-y-3">
                {searchResults.map((match) => (
                  <div
                    key={`${match.chunk_id}-${match.chunk_index}`}
                    onClick={() => handleSelectMatch(match)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer space-y-2 ${
                      selectedMatch?.chunk_id === match.chunk_id
                        ? 'bg-cyan-50/50 border-cyan-300 shadow-sm'
                        : 'bg-white border-slate-200/80 hover:border-slate-300 shadow-2xs'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 font-semibold text-xs text-slate-900">
                        <FileCode className="w-3.5 h-3.5 text-cyan-600 shrink-0" />
                        <span>{match.file_name}</span>
                        <span className="text-[11px] text-slate-400 font-mono">
                          (Chunk #{match.chunk_index}{match.page_number ? `, Page ${match.page_number}` : ''})
                        </span>
                      </div>
                      <Badge variant="info">Score: {match.score}</Badge>
                    </div>

                    <p className="text-xs text-slate-700 bg-slate-50 p-2.5 rounded-xl border border-slate-200/60 font-mono leading-relaxed">
                      {match.snippet}
                    </p>

                    <div className="text-[11px] text-slate-400 font-mono flex items-center justify-between">
                      <span>{match.relative_path}</span>
                      <span className="text-cyan-600 font-medium">View Chunks →</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Search}
                title="No Search Matches"
                description={`No document chunks matched the term '${searchQuery}'.`}
              />
            )
          ) : (
            /* Document Cards Grid */
            documentsList.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {documentsList.map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => handleSelectDoc(doc.id)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer space-y-3 ${
                      selectedDoc?.id === doc.id
                        ? 'bg-cyan-50/50 border-cyan-300 shadow-sm'
                        : 'bg-white border-slate-200/80 hover:border-slate-300 shadow-2xs'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="p-2.5 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 font-mono text-xs uppercase font-semibold">
                          {doc.file_extension.replace('.', '') || 'txt'}
                        </div>
                        <div>
                          <h4 className="font-semibold text-xs text-slate-900">{doc.file_name}</h4>
                          <p className="text-[11px] text-slate-500 font-mono">{formatBytes(doc.size_bytes)}</p>
                        </div>
                      </div>
                      <Badge variant={doc.extraction_status === 'SUCCESS' ? 'info' : 'warning'}>
                        {doc.chunk_count} Chunks
                      </Badge>
                    </div>

                    <p className="text-[11px] text-slate-600 line-clamp-2 leading-relaxed font-mono">
                      {doc.relative_path}
                    </p>

                    <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                      <span>{doc.page_count} {doc.page_count === 1 ? 'Page' : 'Pages'}</span>
                      <span className="text-cyan-600 font-medium hover:underline flex items-center gap-1">
                        <Eye className="w-3 h-3" /> Select Preview
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={FileText}
                title="No Indexed Documents"
                description="Click 'Index Workspace' above to scan and index workspace documents."
              />
            )
          )}
        </div>

        {/* Right Column: Document & Chunk Detail Panel */}
        <div>
          <Card title="Document & Semantic Reader">
            {detailLoading ? (
              <div className="py-12 text-center text-slate-400 text-xs">
                <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2 text-cyan-600" />
                Loading document details...
              </div>
            ) : selectedDoc ? (
              <div className="space-y-4 text-xs">
                {/* Metadata Header */}
                <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1.5">
                  <div className="font-semibold text-slate-900 flex items-center justify-between">
                    <span>{selectedDoc.file_name}</span>
                    <Badge variant="info">{selectedDoc.chunk_count} Chunks</Badge>
                  </div>
                  <div className="text-[11px] font-mono text-slate-500">Path: {selectedDoc.relative_path}</div>
                  <div className="text-[11px] text-slate-500 flex items-center justify-between">
                    <span>Size: {formatBytes(selectedDoc.size_bytes)}</span>
                    <span>Pages: {selectedDoc.page_count}</span>
                  </div>
                </div>

                {/* Security Badge */}
                <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl space-y-1 text-amber-900 text-xs">
                  <div className="flex items-center space-x-1.5 font-semibold">
                    <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>Safe On-Device Content Boundary</span>
                  </div>
                  <p className="text-amber-800 text-[11px] leading-relaxed">
                    Extracted text stored in local SQLite database. Untrusted data is isolated from direct shell execution.
                  </p>
                </div>

                {/* View Mode Switcher */}
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {previewMode === 'chunks' ? `Extracted Chunks (${selectedDoc.chunks.length})` : 'Full Extracted Text'}
                  </span>
                  <div className="flex items-center gap-1 bg-slate-100 p-0.5 rounded-lg text-[11px]">
                    <button
                      onClick={() => setPreviewMode('chunks')}
                      className={`px-2 py-0.5 rounded-md font-medium transition-all ${
                        previewMode === 'chunks' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'
                      }`}
                    >
                      Chunks
                    </button>
                    <button
                      onClick={() => setPreviewMode('full')}
                      className={`px-2 py-0.5 rounded-md font-medium transition-all ${
                        previewMode === 'full' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'
                      }`}
                    >
                      Full Text
                    </button>
                  </div>
                </div>

                {/* Content Reader */}
                {previewMode === 'chunks' ? (
                  <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
                    {selectedDoc.chunks.map((chk) => (
                      <div
                        key={chk.chunk_id}
                        className={`p-3 rounded-xl border text-[11px] space-y-1.5 font-mono ${
                          selectedMatch?.chunk_id === chk.chunk_id
                            ? 'bg-cyan-50/60 border-cyan-300'
                            : 'bg-white border-slate-200/80'
                        }`}
                      >
                        <div className="flex items-center justify-between text-slate-400 font-semibold">
                          <span>Chunk #{chk.chunk_index} {chk.page_number ? `• Page ${chk.page_number}` : ''}</span>
                          <span>{chk.token_count} tokens</span>
                        </div>
                        <p className="text-slate-800 leading-relaxed whitespace-pre-wrap">
                          {chk.content}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <pre className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-[11px] text-slate-700 font-mono whitespace-pre-wrap max-h-80 overflow-y-auto">
                    {selectedDoc.chunks.map(c => c.content).join('\n\n--- Chunk Boundary ---\n\n') || 'No content extracted.'}
                  </pre>
                )}
              </div>
            ) : (
              <EmptyState
                icon={FileText}
                title="No Document Selected"
                description="Click on any document card or search result match to read extracted chunks."
              />
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
