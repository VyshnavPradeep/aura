'use client'

import { X } from 'lucide-react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import type { Finding } from '@/types'

interface CodeViewerProps {
  finding: Finding
  onClose: () => void
}

export default function CodeViewer({ finding, onClose }: CodeViewerProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'border-red-500 bg-red-50'
      case 'HIGH': return 'border-orange-500 bg-orange-50'
      case 'MEDIUM': return 'border-yellow-500 bg-yellow-50'
      case 'LOW': return 'border-blue-500 bg-blue-50'
      default: return 'border-gray-500 bg-gray-50'
    }
  }

  const getLanguage = (filePath?: string) => {
    if (!filePath) return 'javascript'
    if (filePath.endsWith('.py')) return 'python'
    if (filePath.endsWith('.js') || filePath.endsWith('.jsx')) return 'javascript'
    if (filePath.endsWith('.ts') || filePath.endsWith('.tsx')) return 'typescript'
    if (filePath.endsWith('.java')) return 'java'
    if (filePath.endsWith('.go')) return 'go'
    if (filePath.endsWith('.sql')) return 'sql'
    return 'javascript'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className={`border-b-4 ${getSeverityColor(finding.severity)} p-6`}>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <span className={`px-3 py-1 text-sm font-semibold rounded ${
                  finding.severity === 'CRITICAL' ? 'bg-red-600 text-white' :
                  finding.severity === 'HIGH' ? 'bg-orange-600 text-white' :
                  finding.severity === 'MEDIUM' ? 'bg-yellow-600 text-white' :
                  'bg-blue-600 text-white'
                }`}>
                  {finding.severity}
                </span>
                <span className="text-sm text-gray-600">{finding.agent.replace('Agent', '')}</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{finding.title}</h2>
              {finding.file_path && (
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="font-mono">{finding.file_path}</span>
                  {finding.line_number && (
                    <span className="text-gray-500">Line {finding.line_number}</span>
                  )}
                </div>
              )}
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Description */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
            <p className="text-gray-700">{finding.description}</p>
          </div>

          {/* Code Snippet */}
          {finding.code_snippet && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Code Snippet</h3>
              <div className="rounded-lg overflow-hidden border border-gray-300">
                <SyntaxHighlighter
                  language={getLanguage(finding.file_path)}
                  style={vscDarkPlus}
                  showLineNumbers={true}
                  startingLineNumber={finding.line_number || 1}
                  customStyle={{
                    margin: 0,
                    padding: '1rem',
                    fontSize: '0.875rem',
                  }}
                >
                  {finding.code_snippet}
                </SyntaxHighlighter>
              </div>
            </div>
          )}

          {/* Recommendation */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Recommendation</h3>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-gray-800">{finding.recommendation}</p>
            </div>
          </div>

          {/* Metadata */}
          {finding.metadata && Object.keys(finding.metadata).length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Additional Information</h3>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <dl className="space-y-2">
                  {finding.metadata.confidence && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-gray-600">Confidence:</dt>
                      <dd className="text-sm font-semibold text-gray-900">
                        {(finding.metadata.confidence * 100).toFixed(0)}%
                      </dd>
                    </div>
                  )}
                  {finding.metadata.category && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-gray-600">Category:</dt>
                      <dd className="text-sm font-semibold text-gray-900">
                        {finding.metadata.category}
                      </dd>
                    </div>
                  )}
                </dl>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t bg-gray-50 px-6 py-4">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
