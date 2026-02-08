'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { ArrowLeft, Shield, TestTube, Zap, Database, Play, Loader, AlertCircle, CheckCircle, Search, Download, BarChart2, TrendingUp } from 'lucide-react'
import { runAnalysis, getAnalysisResults } from '@/services/api'
import type { AnalysisResponse, Finding } from '@/types'
import FindingsTable from '@/components/FindingsTable'
import CodeViewer from '@/components/CodeViewer'

export default function DashboardPage() {
  const router = useRouter()
  const params = useParams()
  const projectId = params.projectId as string

  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState<AnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<string>('all')
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null)

  useEffect(() => {
    loadExistingResults()
  }, [projectId])

  const loadExistingResults = async () => {
    try {
      const data = await getAnalysisResults(projectId)
      setResults(data)
    } catch (err) {
      console.log('No existing results found')
    }
  }

  const handleRunAnalysis = async () => {
    setAnalyzing(true)
    setError(null)

    try {
      const data = await runAnalysis(projectId)
      setResults(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
    } finally {
      setAnalyzing(false)
    }
  }

  const getAgentIcon = (agent: string) => {
    switch (agent) {
      case 'SecurityAgent': return Shield
      case 'TestGeneratorAgent': return TestTube
      case 'ScalabilityAgent': return Zap
      case 'DatabaseAgent': return Database
      default: return CheckCircle
    }
  }

  const getAgentColor = (agent: string) => {
    return '#0f62fe' // IBM Blue for all agents
  }

  const getAllFindings = (): Finding[] => {
    if (!results?.agent_results) return []

    const findings: Finding[] = []
    Object.values(results.agent_results).forEach(agentResult => {
      if (agentResult?.findings) {
        findings.push(...agentResult.findings)
      }
    })
    return findings
  }

  const getFilteredFindings = (): Finding[] => {
    const allFindings = getAllFindings()
    if (selectedAgent === 'all') return allFindings
    return allFindings.filter(f => f.agent === selectedAgent)
  }

  const exportResults = () => {
    if (!results) return

    const dataStr = JSON.stringify(results, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `aura-analysis-${projectId}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const getSeverityPercentage = (count: number, total: number) => {
    return total > 0 ? (count / total) * 100 : 0
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header - Consistent with Homepage */}
      <header className="bg-gray-100 border-b border-gray-20 sticky top-0 z-50">
        <div className="container mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <button
                onClick={() => router.push('/')}
                className="flex items-center space-x-3"
              >
                <Shield className="w-7 h-7" style={{ color: '#0f62fe' }} />
                <h1 className="text-xl font-semibold" style={{ color: '#161616' }}>AURA</h1>
              </button>
              <button
                onClick={() => router.push('/projects')}
                className="flex items-center space-x-2 text-sm font-medium hover:bg-gray-10 px-3 py-2 transition-colors"
                style={{ color: '#161616' }}
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back to projects</span>
              </button>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => router.push(`/search/${projectId}`)}
                className="px-4 py-2 text-sm font-medium hover:bg-gray-10 transition-colors flex items-center space-x-2"
                style={{ color: '#0f62fe' }}
              >
                <Search className="w-4 h-4" />
                <span>RAG Search</span>
              </button>
              {results && (
                <button
                  onClick={exportResults}
                  className="px-4 py-2 text-sm font-medium hover:bg-gray-10 transition-colors flex items-center space-x-2"
                  style={{ color: '#161616' }}
                >
                  <Download className="w-4 h-4" />
                  <span>Export</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-12 max-w-7xl">
        {/* Page Header */}
        <div className="mb-12 pb-8 border-b" style={{ borderColor: '#e0e0e0' }}>
          <h1 className="text-5xl font-light mb-4" style={{ color: '#161616' }}>
            Analysis Report
          </h1>
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium" style={{ color: '#525252' }}>Project ID:</span>
            <span className="font-mono text-sm px-3 py-1" style={{ backgroundColor: '#f4f4f4', color: '#161616' }}>{projectId}</span>
          </div>
        </div>

        {/* Run Analysis Section */}
        {!results && !analyzing && (
          <div className="border p-12 text-center mb-12" style={{ borderColor: '#e0e0e0' }}>
            <div className="w-20 h-20 mx-auto mb-6 flex items-center justify-center" style={{ backgroundColor: '#f4f4f4' }}>
              <Play className="w-10 h-10" style={{ color: '#0f62fe' }} />
            </div>
            <h2 className="text-3xl font-semibold mb-3" style={{ color: '#161616' }}>Ready to analyze</h2>
            <p className="mb-8 text-lg" style={{ color: '#525252' }}>
              Run AI-powered analysis with 4 specialized agents
            </p>
            <button
              onClick={handleRunAnalysis}
              className="px-8 py-3 text-sm font-medium text-white transition-colors"
              style={{ backgroundColor: '#0f62fe' }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
            >
              Start analysis
            </button>
          </div>
        )}

        {/* Analyzing State */}
        {analyzing && (
          <div className="border p-16 text-center mb-12" style={{ borderColor: '#e0e0e0' }}>
            <Loader className="w-16 h-16 animate-spin mx-auto mb-6" style={{ color: '#0f62fe' }} />
            <h2 className="text-3xl font-semibold mb-3" style={{ color: '#161616' }}>Analyzing your code</h2>
            <p style={{ color: '#525252' }}>
              Running 4 AI agents in parallel... This may take 10-30 seconds
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="p-6 border flex items-start space-x-3 mb-12" style={{ backgroundColor: '#fff1f1', borderColor: '#da1e28' }}>
            <AlertCircle className="w-6 h-6 flex-shrink-0 mt-0.5" style={{ color: '#da1e28' }} />
            <div className="flex-1">
              <p className="font-semibold mb-1" style={{ color: '#da1e28' }}>Analysis failed</p>
              <p className="mb-4" style={{ color: '#da1e28' }}>{error}</p>
              <button
                onClick={handleRunAnalysis}
                className="px-6 py-2 text-sm font-medium text-white transition-colors"
                style={{ backgroundColor: '#da1e28' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#ba1b23'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#da1e28'}
              >
                Try again
              </button>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-8">
            {/* Summary Section */}
            <div className="border p-8" style={{ borderColor: '#e0e0e0' }}>
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center space-x-3">
                  <BarChart2 className="w-6 h-6" style={{ color: '#0f62fe' }} />
                  <h2 className="text-2xl font-semibold" style={{ color: '#161616' }}>Security overview</h2>
                </div>
                <div className="text-right">
                  <p className="text-5xl font-light" style={{ color: '#161616' }}>{results.summary.total_findings}</p>
                  <p className="text-sm" style={{ color: '#525252' }}>Total findings</p>
                </div>
              </div>

              {/* Severity Breakdown */}
              <div className="space-y-6">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium" style={{ color: '#525252' }}>Critical</span>
                    <span className="text-sm font-semibold" style={{ color: '#161616' }}>{results.summary.critical_count}</span>
                  </div>
                  <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#f4f4f4' }}>
                    <div
                      className="h-full transition-all duration-1000"
                      style={{
                        width: `${getSeverityPercentage(results.summary.critical_count, results.summary.total_findings)}%`,
                        backgroundColor: '#da1e28'
                      }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium" style={{ color: '#525252' }}>High</span>
                    <span className="text-sm font-semibold" style={{ color: '#161616' }}>{results.summary.high_count}</span>
                  </div>
                  <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#f4f4f4' }}>
                    <div
                      className="h-full transition-all duration-1000"
                      style={{
                        width: `${getSeverityPercentage(results.summary.high_count, results.summary.total_findings)}%`,
                        backgroundColor: '#ff832b'
                      }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium" style={{ color: '#525252' }}>Medium</span>
                    <span className="text-sm font-semibold" style={{ color: '#161616' }}>{results.summary.medium_count}</span>
                  </div>
                  <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#f4f4f4' }}>
                    <div
                      className="h-full transition-all duration-1000"
                      style={{
                        width: `${getSeverityPercentage(results.summary.medium_count, results.summary.total_findings)}%`,
                        backgroundColor: '#f1c21b'
                      }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium" style={{ color: '#525252' }}>Low</span>
                    <span className="text-sm font-semibold" style={{ color: '#161616' }}>{results.summary.low_count}</span>
                  </div>
                  <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#f4f4f4' }}>
                    <div
                      className="h-full transition-all duration-1000"
                      style={{
                        width: `${getSeverityPercentage(results.summary.low_count, results.summary.total_findings)}%`,
                        backgroundColor: '#24a148'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Agent Analysis Section */}
            <div className="border p-8" style={{ borderColor: '#e0e0e0' }}>
              <h2 className="text-2xl font-semibold mb-6" style={{ color: '#161616' }}>Agent analysis</h2>
              <div className="space-y-4">
                {Object.entries(results.agent_results).map(([agentName, agentResult]) => {
                  const Icon = getAgentIcon(agentName)

                  return (
                    <div
                      key={agentName}
                      className="flex items-center justify-between p-6 border hover:bg-gray-10 transition-colors cursor-pointer"
                      style={{ borderColor: '#e0e0e0' }}
                      onClick={() => setSelectedAgent(agentName)}
                    >
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 flex items-center justify-center" style={{ backgroundColor: '#f4f4f4' }}>
                          <Icon className="w-6 h-6" style={{ color: '#0f62fe' }} />
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold mb-1" style={{ color: '#161616' }}>
                            {agentName.replace('Agent', '')}
                          </h3>
                          <div className="flex items-center space-x-4 text-sm" style={{ color: '#525252' }}>
                            <span>{agentResult.findings_count} findings</span>
                            <span>•</span>
                            <span>{agentResult.duration_seconds?.toFixed(2)}s</span>
                            <span>•</span>
                            <span>{agentResult.status}</span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-4xl font-light" style={{ color: '#161616' }}>{agentResult.findings_count}</p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Filter Section */}
            <div className="border-b pb-6" style={{ borderColor: '#e0e0e0' }}>
              <div className="flex items-center space-x-2 overflow-x-auto">
                <button
                  onClick={() => setSelectedAgent('all')}
                  className={`px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors`}
                  style={{
                    backgroundColor: selectedAgent === 'all' ? '#0f62fe' : '#f4f4f4',
                    color: selectedAgent === 'all' ? 'white' : '#161616'
                  }}
                  onMouseEnter={(e) => {
                    if (selectedAgent !== 'all') e.currentTarget.style.backgroundColor = '#e0e0e0'
                  }}
                  onMouseLeave={(e) => {
                    if (selectedAgent !== 'all') e.currentTarget.style.backgroundColor = '#f4f4f4'
                  }}
                >
                  All findings ({getAllFindings().length})
                </button>
                {Object.keys(results.agent_results).map(agentName => {
                  const typedAgentName = agentName as keyof typeof results.agent_results
                  return (
                    <button
                      key={agentName}
                      onClick={() => setSelectedAgent(agentName)}
                      className={`px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors`}
                      style={{
                        backgroundColor: selectedAgent === agentName ? '#0f62fe' : '#f4f4f4',
                        color: selectedAgent === agentName ? 'white' : '#161616'
                      }}
                      onMouseEnter={(e) => {
                        if (selectedAgent !== agentName) e.currentTarget.style.backgroundColor = '#e0e0e0'
                      }}
                      onMouseLeave={(e) => {
                        if (selectedAgent !== agentName) e.currentTarget.style.backgroundColor = '#f4f4f4'
                      }}
                    >
                      {agentName.replace('Agent', '')} ({results.agent_results[typedAgentName]?.findings_count || 0})
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Findings Table */}
            <div className="border" style={{ borderColor: '#e0e0e0' }}>
              <FindingsTable
                findings={getFilteredFindings()}
                onSelectFinding={setSelectedFinding}
              />
            </div>

            {/* Code Viewer Modal */}
            {selectedFinding && (
              <CodeViewer
                finding={selectedFinding}
                onClose={() => setSelectedFinding(null)}
              />
            )}
          </div>
        )}
      </div>
    </div>
  )
}
