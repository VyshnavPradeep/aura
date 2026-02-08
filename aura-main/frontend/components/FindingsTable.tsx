'use client'

import { useState } from 'react'
import { AlertCircle, ChevronDown, ChevronUp, Code, Filter } from 'lucide-react'
import type { Finding } from '@/types'

interface FindingsTableProps {
  findings: Finding[]
  onSelectFinding: (finding: Finding) => void
}

export default function FindingsTable({ findings, onSelectFinding }: FindingsTableProps) {
  const [sortBy, setSortBy] = useState<'severity' | 'file'>('severity')
  const [filterSeverity, setFilterSeverity] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set())

  const getSeverityOrder = (severity: string) => {
    const order: Record<string, number> = {
      CRITICAL: 0,
      HIGH: 1,
      MEDIUM: 2,
      LOW: 3,
    }
    return order[severity] ?? 4
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border border-red-300'
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border border-orange-300'
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border border-yellow-300'
      case 'LOW':
        return 'bg-blue-100 text-blue-800 border border-blue-300'
      default:
        return 'bg-gray-100 text-gray-800 border border-gray-300'
    }
  }

  const toggleRow = (index: number) => {
    const newExpanded = new Set(expandedRows)
    if (newExpanded.has(index)) {
      newExpanded.delete(index)
    } else {
      newExpanded.add(index)
    }
    setExpandedRows(newExpanded)
  }

  // Filter and sort
  let filteredFindings = findings.filter(f => {
    if (filterSeverity !== 'all' && f.severity !== filterSeverity) return false
    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      return (
        f.title.toLowerCase().includes(term) ||
        f.description.toLowerCase().includes(term) ||
        f.file_path?.toLowerCase().includes(term)
      )
    }
    return true
  })

  if (sortBy === 'severity') {
    filteredFindings = [...filteredFindings].sort(
      (a, b) => getSeverityOrder(a.severity) - getSeverityOrder(b.severity)
    )
  } else {
    filteredFindings = [...filteredFindings].sort((a, b) =>
      (a.file_path || '').localeCompare(b.file_path || '')
    )
  }

  if (filteredFindings.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <p className="text-gray-600">
          {searchTerm || filterSeverity !== 'all'
            ? 'No findings match your filters'
            : 'No findings to display'}
        </p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Filters */}
      <div className="p-4 border-b border-gray-200 space-y-3">
        <div className="flex items-center space-x-3">
          <Filter className="w-5 h-5 text-gray-500" />
          <span className="font-semibold text-gray-700">Filters</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {/* Search */}
          <input
            type="text"
            placeholder="Search findings..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {/* Severity Filter */}
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'severity' | 'file')}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="severity">Sort by Severity</option>
            <option value="file">Sort by File</option>
          </select>
        </div>
        <div className="text-sm text-gray-600">
          Showing {filteredFindings.length} of {findings.length} finding{findings.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Severity
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Title
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Agent
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Location
              </th>
              <th className="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredFindings.map((finding, index) => (
              <>
                <tr key={index} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs font-semibold rounded ${getSeverityBadge(finding.severity)}`}>
                      {finding.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-sm font-medium text-gray-900">{finding.title}</p>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm text-gray-600">{finding.agent.replace('Agent', '')}</span>
                  </td>
                  <td className="px-4 py-3">
                    {finding.file_path && (
                      <div className="text-sm">
                        <p className="text-gray-900 font-mono truncate max-w-xs">{finding.file_path}</p>
                        {finding.line_number && (
                          <p className="text-gray-500 text-xs">Line {finding.line_number}</p>
                        )}
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center space-x-2">
                      {finding.code_snippet && (
                        <button
                          onClick={() => onSelectFinding(finding)}
                          className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center space-x-1"
                        >
                          <Code className="w-3 h-3" />
                          <span>View Code</span>
                        </button>
                      )}
                      <button
                        onClick={() => toggleRow(index)}
                        className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
                      >
                        {expandedRows.has(index) ? (
                          <ChevronUp className="w-4 h-4" />
                        ) : (
                          <ChevronDown className="w-4 h-4" />
                        )}
                      </button>
                    </div>
                  </td>
                </tr>
                {expandedRows.has(index) && (
                  <tr key={`${index}-expanded`} className="bg-gray-50">
                    <td colSpan={5} className="px-4 py-4">
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs font-semibold text-gray-600 mb-1">Description</p>
                          <p className="text-sm text-gray-800">{finding.description}</p>
                        </div>
                        <div>
                          <p className="text-xs font-semibold text-gray-600 mb-1">Recommendation</p>
                          <p className="text-sm text-gray-800">{finding.recommendation}</p>
                        </div>
                        {finding.metadata && (
                          <div>
                            <p className="text-xs font-semibold text-gray-600 mb-1">Additional Info</p>
                            <div className="text-sm text-gray-700">
                              {finding.metadata.confidence && (
                                <p>Confidence: {(finding.metadata.confidence * 100).toFixed(0)}%</p>
                              )}
                              {finding.metadata.category && (
                                <p>Category: {finding.metadata.category}</p>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
