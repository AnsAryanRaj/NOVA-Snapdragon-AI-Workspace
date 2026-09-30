export type NavigationTab = 
  | 'overview'
  | 'workspace'
  | 'documents'
  | 'vision'
  | 'voice'
  | 'activity'
  | 'performance'
  | 'settings';

export interface SecurityPolicy {
  shell_execution_blocked: boolean;
  tool_registry_enforced: boolean;
  user_confirmation_required: boolean;
  audit_logging_active: boolean;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  privacy_mode: string;
  qualcomm_isolation: string;
  environment: string;
  timestamp: string;
  security_policy: SecurityPolicy;
}

export interface ToolDefinition {
  id: string;
  name: string;
  category: 'file' | 'document' | 'system' | 'voice' | 'vision' | 'qualcomm';
  description: string;
  is_destructive: boolean;
  requires_confirmation: boolean;
  status: 'available' | 'registered' | 'isolated' | 'disabled';
}

export interface AuditLogItem {
  id: string;
  timestamp: string;
  action_name: string;
  tool_name: string;
  status: 'SUCCESS' | 'BLOCKED' | 'PENDING_CONFIRMATION';
  execution_time_ms: number;
}

export interface FileItemSchema {
  name: string;
  relative_path: string;
  item_type: 'file' | 'directory';
  size_bytes: number;
  modified_time: string;
  extension: string;
  category: 'Code' | 'Document' | 'Data' | 'Image' | 'Other' | 'Folder';
}

export interface DirectoryListingResponse {
  path: string;
  items: FileItemSchema[];
  total_count: number;
}

export interface FileMetadataResponse {
  name: string;
  relative_path: string;
  extension: string;
  size_bytes: number;
  created_time: string;
  modified_time: string;
  item_type: string;
  category: string;
}

export interface FileHashResponse {
  relative_path: string;
  sha256_hash: string;
  size_bytes: number;
}

export interface TextContentResponse {
  relative_path: string;
  content: string;
  size_bytes: number;
  max_bytes_read: number;
  is_truncated: boolean;
}

export interface WorkspaceStatsResponse {
  total_files: number;
  total_directories: number;
  total_size_bytes: number;
  code_count: number;
  document_count: number;
  data_count: number;
  image_count: number;
  other_count: number;
  recent_files: FileItemSchema[];
}

export interface WorkspaceFile {
  id: string;
  name: string;
  path: string;
  size: string;
  type: 'code' | 'document' | 'image' | 'audio' | 'data';
  lastModified: string;
  isIndexed: boolean;
}

export interface DocumentItem {
  id: string;
  title: string;
  path: string;
  format: 'pdf' | 'docx' | 'md' | 'txt';
  pages?: number;
  size: string;
  updatedAt: string;
  status: 'Ready for Analysis' | 'Indexed' | 'Pending';
  snippet?: string;
}

export interface ActivityItem {
  id: string;
  action: string;
  toolName: string;
  timestamp: string;
  status: 'ALLOWED' | 'BLOCKED' | 'CONFIRMED' | 'REQUIRES_CONFIRMATION';
  permissionLevel: 'AUTO' | 'USER_CONFIRMED' | 'SECURITY_BLOCKED';
  result: string;
}

export interface SystemStatus {
  localMode: boolean;
  aiEngineStatus: 'Idle (Local Fallback)' | 'Ready' | 'Inference Active';
  securityStatus: 'Strict Tool Registry Enforced';
  qualcommNpuStatus: 'Awaiting Hardware Benchmark';
}

export interface DocumentMetadataSchema {
  id: string;
  relative_path: string;
  file_name: string;
  file_extension: string;
  mime_type: string;
  size_bytes: number;
  content_hash: string;
  page_count: number;
  chunk_count: number;
  extraction_status: string;
  error_message?: string;
  indexed_at: string;
  last_modified: string;
}

export interface DocumentChunkSchema {
  chunk_id: string;
  doc_id: string;
  chunk_index: number;
  content: string;
  start_char: number;
  end_char: number;
  page_number?: number;
  token_count: number;
  created_at: string;
}

export interface DocumentDetailSchema extends DocumentMetadataSchema {
  chunks: DocumentChunkSchema[];
}

export interface SearchMatchSchema {
  doc_id: string;
  relative_path: string;
  file_name: string;
  file_extension: string;
  chunk_id: string;
  chunk_index: number;
  snippet: string;
  full_chunk_text: string;
  page_number?: number;
  score: number;
  matched_terms: string[];
}

export interface DocumentSearchResultSchema {
  query: string;
  total_matches: number;
  matches: SearchMatchSchema[];
}

export interface IndexingSummarySchema {
  total_found: number;
  indexed_new: number;
  updated: number;
  skipped_unchanged: number;
  failed: number;
  pruned_deleted: number;
  total_chunks: number;
  duration_ms: number;
}

export interface DocumentStatsSchema {
  total_documents: number;
  total_chunks: number;
  total_size_bytes: number;
  documents_by_type: Record<string, number>;
  extraction_statuses: Record<string, number>;
}

export interface QualcommRuntimeInfo {
  available: boolean;
  runtime: string;
  reason: string;
  compute_unit: string;
  has_api_token: boolean;
  redacted_token: string;
}

export interface ModelConfigSpec {
  name: string;
  provider: string;
  runtime: string;
  modality: string;
  precision: string;
  quantization: string;
  target_compute_unit: string;
  is_verified: boolean;
}

export interface SystemCapabilitiesSpec {
  os_name: string;
  processor: string;
  architecture: string;
  is_snapdragon_hardware: boolean;
  available_compute_units: string[];
}

export interface AIRuntimeStatus {
  provider: string;
  runtime: string;
  available: boolean;
  device: string;
  qualcomm: QualcommRuntimeInfo;
  active_model: ModelConfigSpec;
  capabilities: SystemCapabilitiesSpec;
}

export interface PlanStepSchema {
  step_index: number;
  tool_name: string;
  arguments: Record<string, any>;
  description: string;
}

export interface AgentPlanSchema {
  plan_id: string;
  request: string;
  intent: string;
  steps: PlanStepSchema[];
  requires_confirmation: boolean;
  risk_level: string;
  reasoning: string;
  is_supported: boolean;
}

export interface StepExecutionResultSchema {
  step_index: number;
  tool_name: string;
  arguments: Record<string, any>;
  status: string;
  output: Record<string, any>;
  execution_time_ms: number;
  error_message?: string;
}

export interface AgentExecutionResultSchema {
  plan_id: string;
  request: string;
  intent: string;
  status: string;
  step_results: StepExecutionResultSchema[];
  summary_text: string;
  audit_log_id?: number;
  total_duration_ms: number;
}


