'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Trash2, FolderOpen, Calendar, Code, Loader, AlertCircle, Search as SearchIcon, Shield } from 'lucide-react'
import { listProjects, deleteProject } from '@/services/api'

export default function ProjectsPage() {
  const router = useRouter()
  const [projects, setProjects] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await listProjects()
      setProjects(data.projects || [])
    } catch (err: any) {
      setError(err.message || 'Failed to load projects')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (projectId: string) => {
    if (!confirm(`Are you sure you want to delete project ${projectId}?`)) {
      return
    }

    setDeleting(projectId)
    try {
      await deleteProject(projectId)
      setProjects(projects.filter(p => p !== projectId))
    } catch (err: any) {
      alert(`Failed to delete project: ${err.message}`)
    } finally {
      setDeleting(null)
    }
  }

  const handleViewProject = (projectId: string) => {
    router.push(`/dashboard/${projectId}`)
  }

  const filteredProjects = projects.filter(project =>
    project.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Parse project ID to extract date and info
  const parseProjectId = (projectId: string) => {
    // Format: YYYYMMDD_HHMMSS_randomid
    const parts = projectId.split('_')
    if (parts.length >= 2) {
      const datePart = parts[0]
      const timePart = parts[1]
      const year = datePart.substring(0, 4)
      const month = datePart.substring(4, 6)
      const day = datePart.substring(6, 8)
      const hour = timePart.substring(0, 2)
      const minute = timePart.substring(2, 4)

      return {
        date: `${year}-${month}-${day}`,
        time: `${hour}:${minute}`,
        dateObj: new Date(`${year}-${month}-${day}T${hour}:${minute}:00`),
      }
    }
    return null
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
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
                onClick={() => router.push('/')}
                className="flex items-center space-x-2 text-sm font-medium hover:bg-gray-10 px-3 py-2 transition-colors"
                style={{ color: '#161616' }}
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
            </div>
            <button
              onClick={() => router.push('/upload')}
              className="px-6 py-2 text-sm font-medium text-white transition-colors"
              style={{ backgroundColor: '#0f62fe' }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
            >
              Upload New Project
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-12 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-4xl font-light mb-3" style={{ color: '#161616' }}>Your Projects</h1>
          <p className="text-lg" style={{ color: '#525252' }}>
            Manage and view analysis results for your uploaded code
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{ color: '#8d8d8d' }} />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border focus:outline-none"
              style={{ borderColor: '#e0e0e0' }}
              onFocus={(e) => e.currentTarget.style.borderColor = '#0f62fe'}
              onBlur={(e) => e.currentTarget.style.borderColor = '#e0e0e0'}
            />
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader className="w-12 h-12 animate-spin mb-4" style={{ color: '#0f62fe' }} />
            <p style={{ color: '#525252' }}>Loading projects...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="p-6 border flex items-start space-x-3" style={{ backgroundColor: '#fff1f1', borderColor: '#da1e28' }}>
            <AlertCircle className="w-6 h-6 flex-shrink-0 mt-0.5" style={{ color: '#da1e28' }} />
            <div>
              <p className="font-semibold mb-1" style={{ color: '#da1e28' }}>Error Loading Projects</p>
              <p style={{ color: '#da1e28' }}>{error}</p>
              <button
                onClick={loadProjects}
                className="mt-3 px-4 py-2 text-sm font-medium text-white transition-colors"
                style={{ backgroundColor: '#da1e28' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#ba1b23'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#da1e28'}
              >
                Try Again
              </button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && filteredProjects.length === 0 && (
          <div className="text-center py-20">
            <FolderOpen className="w-16 h-16 mx-auto mb-4" style={{ color: '#8d8d8d' }} />
            <h3 className="text-xl font-semibold mb-2" style={{ color: '#161616' }}>
              {searchTerm ? 'No projects found' : 'No projects yet'}
            </h3>
            <p className="mb-6" style={{ color: '#525252' }}>
              {searchTerm
                ? 'Try adjusting your search term'
                : 'Upload your first project to get started with AI-powered code analysis'}
            </p>
            {!searchTerm && (
              <button
                onClick={() => router.push('/upload')}
                className="px-6 py-3 text-sm font-medium text-white transition-colors"
                style={{ backgroundColor: '#0f62fe' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
              >
                Upload Project
              </button>
            )}
          </div>
        )}

        {/* Projects Grid */}
        {!loading && !error && filteredProjects.length > 0 && (
          <>
            <div className="mb-4 text-sm" style={{ color: '#6f6f6f' }}>
              Showing {filteredProjects.length} of {projects.length} project{projects.length !== 1 ? 's' : ''}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProjects.map((projectId) => {
                const projectInfo = parseProjectId(projectId)
                return (
                  <div
                    key={projectId}
                    className="border hover:shadow-card-hover transition-all overflow-hidden"
                    style={{ borderColor: '#e0e0e0' }}
                  >
                    <div className="p-4" style={{ backgroundColor: '#0f62fe' }}>
                      <div className="flex items-center space-x-2 text-white">
                        <Code className="w-5 h-5" />
                        <h3 className="font-semibold text-sm">Project</h3>
                      </div>
                    </div>

                    <div className="p-4">
                      {/* Project ID */}
                      <div className="mb-3">
                        <p className="text-xs mb-1" style={{ color: '#6f6f6f' }}>Project ID</p>
                        <p className="text-sm font-mono break-all" style={{ color: '#161616' }}>{projectId}</p>
                      </div>

                      {/* Date/Time */}
                      {projectInfo && (
                        <div className="flex items-center space-x-2 text-sm mb-4" style={{ color: '#525252' }}>
                          <Calendar className="w-4 h-4" />
                          <span>
                            {projectInfo.date} at {projectInfo.time}
                          </span>
                        </div>
                      )}

                      {/* Actions */}
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleViewProject(projectId)}
                          className="flex-1 px-4 py-2 text-sm font-medium text-white transition-colors"
                          style={{ backgroundColor: '#0f62fe' }}
                          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
                        >
                          View Analysis
                        </button>
                        <button
                          onClick={() => handleDelete(projectId)}
                          disabled={deleting === projectId}
                          className="px-4 py-2 transition-colors disabled:opacity-50"
                          style={{ backgroundColor: '#fff1f1', color: '#da1e28' }}
                          onMouseEnter={(e) => !e.currentTarget.disabled && (e.currentTarget.style.backgroundColor = '#ffd7d9')}
                          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#fff1f1'}
                          title="Delete project"
                        >
                          {deleting === projectId ? (
                            <Loader className="w-4 h-4 animate-spin" />
                          ) : (
                            <Trash2 className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
