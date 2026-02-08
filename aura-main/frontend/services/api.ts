import axios from 'axios'
import type {
  UploadResponse,
  AnalysisResponse,
  ProjectInfo,
  RAGSearchRequest,
  RAGSearchResponse,
  AgentInfo,
} from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Health Check
export const checkHealth = async () => {
  const response = await api.get('/')
  return response.data
}

// Upload Code
export const uploadCode = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// List Projects
export const listProjects = async (): Promise<{ projects: string[]; count: number }> => {
  const response = await api.get('/upload/projects')
  return response.data
}

// Delete Project
export const deleteProject = async (projectId: string): Promise<{ message: string }> => {
  const response = await api.delete(`/upload/projects/${projectId}`)
  return response.data
}

// Run Analysis
export const runAnalysis = async (
  projectId: string,
  agents?: string[]
): Promise<AnalysisResponse> => {
  const params = agents ? { agents: agents.join(',') } : {}
  const response = await api.post(`/analyze/${projectId}`, null, { params })
  return response.data
}

// Get Analysis Results
export const getAnalysisResults = async (projectId: string): Promise<AnalysisResponse> => {
  const response = await api.get(`/analyze/${projectId}/results`)
  return response.data
}

// Get Analysis Summary
export const getAnalysisSummary = async (projectId: string) => {
  const response = await api.get(`/analyze/${projectId}/summary`)
  return response.data
}

// List Available Agents
export const listAgents = async (): Promise<{ agents: AgentInfo[]; total_agents: number }> => {
  const response = await api.get('/analyze/agents')
  return response.data
}

// RAG: Index Codebase
export const indexCodebase = async (data: {
  project_dir: string
  project_id: string
  file_extensions?: string[]
  exclude_dirs?: string[]
}) => {
  const response = await api.post('/rag/index', data)
  return response.data
}

// RAG: Search Code
export const searchCode = async (data: RAGSearchRequest): Promise<RAGSearchResponse> => {
  const response = await api.post('/rag/search', data)
  return response.data
}

// RAG: Get Statistics
export const getRAGStatistics = async (projectId: string) => {
  const response = await api.get(`/rag/statistics/${projectId}`)
  return response.data
}

// RAG: Health Check
export const checkRAGHealth = async () => {
  const response = await api.get('/rag/health')
  return response.data
}

export default api
