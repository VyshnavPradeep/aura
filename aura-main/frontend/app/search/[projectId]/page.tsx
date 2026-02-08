'use client'

import { useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { ArrowLeft, Search, Loader, AlertCircle, FileCode, Sparkles } from 'lucide-react'
import { searchCode } from '@/services/api'
import type { RAGSearchResponse, RAGSearchResult } from '@/types'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

export default function SearchPage() {
  const router = useRouter()
  const params = useParams()
  const projectId = params.projectId as string

  const [query, setQuery] = useState('')
  const [strategy, setStrategy] = useState<'standard' | 'multi_query' | 'hyde'>('multi_query')
  const [topK, setTopK] = useState(5)
  const [useReranking, setUseReranking] = useState(true)
  const [includeContext, setIncludeContext] = useState(true)
  const [searching, setSearching] = useState(false)
  const [results, setResults] = useState<RAGSearchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!query.trim()) {
      setError('Please enter a search query')
      return
    }

    setSearching(true)
    setError(null)
    setResults(null)

    try {
      const data = await searchCode({
        query: query.trim(),
        project_id: projectId,
        strategy,
        top_k: topK,
        use_reranking: useReranking,
        include_context: includeContext,
      })
      setResults(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Search failed')
    } finally {
      setSearching(false)
    }
  }

  const getLanguage = (filePath: string) => {
    if (filePath.endsWith('.py')) return 'python'
    if (filePath.endsWith('.js') || filePath.endsWith('.jsx')) return 'javascript'
    if (filePath.endsWith('.ts') || filePath.endsWith('.tsx')) return 'typescript'
    if (filePath.endsWith('.java')) return 'java'
    if (filePath.endsWith('.go')) return 'go'
    if (filePath.endsWith('.sql')) return 'sql'
    return 'javascript'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push(`/dashboard/${projectId}`)}
              className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Dashboard</span>
            </button>
            <div className="flex items-center space-x-2 text-purple-600">
              <Sparkles className="w-5 h-5" />
              <span className="font-semibold">RAG-Powered Search</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8 max-w-6xl">
        {/* Title */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Semantic Code Search</h1>
          <p className="text-xl text-gray-600">
            Use AI-powered semantic search to find relevant code snippets
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Project ID: <span className="font-mono">{projectId}</span>
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
          <form onSubmit={handleSearch} className="space-y-4">
            {/* Search Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Search Query
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="E.g., authentication logic, database queries, error handling..."
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={searching}
                />
              </div>
            </div>

            {/* Advanced Options */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Strategy */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Search Strategy
                </label>
                <select
                  value={strategy}
                  onChange={(e) => setStrategy(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={searching}
                >
                  <option value="standard">Standard (Basic)</option>
                  <option value="multi_query">Multi-Query (Best)</option>
                  <option value="hyde">HyDE (Experimental)</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  {strategy === 'standard' && 'Simple semantic search'}
                  {strategy === 'multi_query' && 'AI generates multiple query variations'}
                  {strategy === 'hyde' && 'Hypothetical document embeddings'}
                </p>
              </div>

              {/* Top K */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Results Count
                </label>
                <input
                  type="number"
                  value={topK}
                  onChange={(e) => setTopK(Number(e.target.value))}
                  min={1}
                  max={20}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={searching}
                />
              </div>

              {/* Options */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Options
                </label>
                <div className="space-y-2">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={useReranking}
                      onChange={(e) => setUseReranking(e.target.checked)}
                      disabled={searching}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">Use Reranking</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={includeContext}
                      onChange={(e) => setIncludeContext(e.target.checked)}
                      disabled={searching}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">Include Context</span>
                  </label>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={searching || !query.trim()}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 font-semibold"
            >
              {searching ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Searching...</span>
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  <span>Search Code</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3 mb-6">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-red-800 font-semibold">Search Failed</p>
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-6">
            {/* Results Header */}
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Found {results.results_count} result{results.results_count !== 1 ? 's' : ''}
                  </h2>
                  <p className="text-sm text-gray-600">
                    Strategy: <span className="font-semibold">{results.strategy}</span>
                    {results.metadata?.reranked && (
                      <span className="ml-2 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded">
                        Reranked
                      </span>
                    )}
                  </p>
                </div>
              </div>

              {/* Enhanced Queries */}
              {results.metadata?.enhanced_queries && results.metadata.enhanced_queries.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-sm font-semibold text-gray-700 mb-2">AI-Generated Query Variations:</p>
                  <div className="flex flex-wrap gap-2">
                    {results.metadata.enhanced_queries.map((eq, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-blue-50 text-blue-700 text-xs rounded-full border border-blue-200"
                      >
                        {eq}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Results List */}
            {results.results.map((result, index) => (
              <div
                key={result.chunk_id || index}
                className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
              >
                {/* Result Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 text-white">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <FileCode className="w-5 h-5" />
                      <span className="font-semibold">{result.file}</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      {result.chunk_type && (
                        <span className="px-2 py-1 bg-white/20 text-xs rounded">
                          {result.chunk_type}
                        </span>
                      )}
                      <span className="px-2 py-1 bg-white/20 text-xs rounded">
                        Score: {(result.score * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Code Content */}
                <div className="p-0">
                  {result.context?.before && (
                    <div className="border-b border-gray-200">
                      <div className="bg-gray-100 px-4 py-2">
                        <p className="text-xs text-gray-600 font-semibold">Context Before:</p>
                      </div>
                      <div className="text-xs text-gray-600 overflow-x-auto">
                        <SyntaxHighlighter
                          language={getLanguage(result.file)}
                          style={vscDarkPlus}
                          customStyle={{
                            margin: 0,
                            padding: '1rem',
                            fontSize: '0.75rem',
                            opacity: 0.7,
                          }}
                        >
                          {result.context.before}
                        </SyntaxHighlighter>
                      </div>
                    </div>
                  )}

                  <div className="border-l-4 border-blue-500">
                    <SyntaxHighlighter
                      language={getLanguage(result.file)}
                      style={vscDarkPlus}
                      showLineNumbers={false}
                      customStyle={{
                        margin: 0,
                        padding: '1rem',
                        fontSize: '0.875rem',
                      }}
                    >
                      {result.content}
                    </SyntaxHighlighter>
                  </div>

                  {result.context?.after && (
                    <div className="border-t border-gray-200">
                      <div className="bg-gray-100 px-4 py-2">
                        <p className="text-xs text-gray-600 font-semibold">Context After:</p>
                      </div>
                      <div className="text-xs text-gray-600 overflow-x-auto">
                        <SyntaxHighlighter
                          language={getLanguage(result.file)}
                          style={vscDarkPlus}
                          customStyle={{
                            margin: 0,
                            padding: '1rem',
                            fontSize: '0.75rem',
                            opacity: 0.7,
                          }}
                        >
                          {result.context.after}
                        </SyntaxHighlighter>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {results && results.results_count === 0 && (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No Results Found</h3>
            <p className="text-gray-600">
              Try adjusting your search query or changing the search strategy
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
