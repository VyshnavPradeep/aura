// API Response Types
export interface UploadResponse {
  status: string
  message: string
  project_id: string
  filename: string
  extraction: {
    total_files: number
    code_files: number
    project_dir: string
  }
  detection: {
    language: string
    confidence: number
    framework: string
    dependencies: number
  }
  parsing: {
    files_parsed: number
    total_functions: number
    total_classes: number
    total_lines: number
    summary: {
      file_count: number
      complexity_estimate: string
    }
  }
  embeddings: {
    chunks_created: number
    index_created: boolean
  }
  next_steps: string[]
}

export interface Finding {
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  title: string
  description: string
  agent: string
  location?: {
    file: string
    line: number
  }
  file_path?: string
  line_number?: number
  code_snippet?: string
  recommendation: string
  metadata?: {
    confidence?: number
    category?: string
  }
}

export interface AgentResult {
  status: string
  agent: string
  findings_count: number
  findings: Finding[]
  duration_seconds: number
  [key: string]: any
}

export interface AnalysisResponse {
  project_id: string
  timestamp: string
  agent_results: {
    SecurityAgent?: AgentResult
    TestGeneratorAgent?: AgentResult
    ScalabilityAgent?: AgentResult
    DatabaseAgent?: AgentResult
  }
  summary: {
    total_findings: number
    critical_count: number
    high_count: number
    medium_count: number
    low_count: number
  }
  analysis_duration_seconds: number
}

export interface ProjectInfo {
  project_id: string
  created_at?: string
  filename?: string
  language?: string
  framework?: string
}

export interface RAGSearchRequest {
  query: string
  project_id: string
  strategy?: 'standard' | 'multi_query' | 'hyde'
  top_k?: number
  filters?: {
    chunk_type?: string[]
  }
  use_reranking?: boolean
  include_context?: boolean
}

export interface RAGSearchResult {
  chunk_id: string
  file: string
  content: string
  score: number
  chunk_type?: string
  context?: {
    before: string
    after: string
  }
}

export interface RAGSearchResponse {
  success: boolean
  query: string
  strategy: string
  results_count: number
  results: RAGSearchResult[]
  metadata?: {
    enhanced_queries?: string[]
    reranked?: boolean
  }
}

export interface AgentInfo {
  agent: string
  description: string
  total_runs: number
  avg_duration_seconds: number
  avg_findings: number
  last_run: string
}
