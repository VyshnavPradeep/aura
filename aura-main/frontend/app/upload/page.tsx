'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useDropzone } from 'react-dropzone'
import { Upload, FileArchive, CheckCircle, AlertCircle, Loader, ArrowLeft, Shield } from 'lucide-react'
import { uploadCode } from '@/services/api'
import type { UploadResponse } from '@/types'

export default function UploadPage() {
  const router = useRouter()
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]

    // Validate file type
    if (!file.name.endsWith('.zip')) {
      setError('Please upload a ZIP file')
      return
    }

    // Validate file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB')
      return
    }

    setError(null)
    setUploading(true)
    setUploadResult(null)

    try {
      const result = await uploadCode(file)
      setUploadResult(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/zip': ['.zip'],
      'application/x-zip-compressed': ['.zip'],
    },
    multiple: false,
    disabled: uploading,
  })

  const handleAnalyze = () => {
    if (uploadResult?.project_id) {
      router.push(`/dashboard/${uploadResult.project_id}`)
    }
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
              onClick={() => router.push('/projects')}
              className="px-4 py-2 text-sm font-medium hover:bg-gray-10 transition-colors"
              style={{ color: '#0f62fe' }}
            >
              View Projects
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-12 max-w-5xl">
        <div className="mb-12">
          <h1 className="text-4xl font-light mb-3" style={{ color: '#161616' }}>Upload your code</h1>
          <p className="text-lg" style={{ color: '#525252' }}>
            Upload a ZIP file containing your backend code for AI-powered analysis
          </p>
        </div>

        {/* Upload Zone */}
        {!uploadResult && (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-12 text-center cursor-pointer transition-all ${isDragActive
                ? 'bg-gray-10'
                : 'hover:bg-gray-10'
              } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
            style={{ borderColor: isDragActive ? '#0f62fe' : '#c6c6c6' }}
          >
            <input {...getInputProps()} />
            {uploading ? (
              <div className="flex flex-col items-center">
                <Loader className="w-16 h-16 animate-spin mb-4" style={{ color: '#0f62fe' }} />
                <p className="text-xl font-medium mb-2" style={{ color: '#161616' }}>Uploading and processing...</p>
                <p className="text-sm" style={{ color: '#6f6f6f' }}>This may take a few seconds</p>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <FileArchive className="w-16 h-16 mb-4" style={{ color: '#0f62fe' }} />
                {isDragActive ? (
                  <p className="text-xl font-medium" style={{ color: '#161616' }}>Drop your ZIP file here</p>
                ) : (
                  <>
                    <p className="text-xl font-medium mb-2" style={{ color: '#161616' }}>
                      Drag and drop your ZIP file here
                    </p>
                    <p className="text-sm mb-6" style={{ color: '#6f6f6f' }}>or</p>
                    <button
                      className="px-6 py-3 text-sm font-medium text-white transition-colors flex items-center space-x-2"
                      style={{ backgroundColor: '#0f62fe' }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
                    >
                      <Upload className="w-4 h-4" />
                      <span>Select file</span>
                    </button>
                  </>
                )}
                <div className="mt-8 text-sm space-y-1" style={{ color: '#6f6f6f' }}>
                  <p>• Supported: Python, JavaScript, TypeScript, Java, Go</p>
                  <p>• Maximum file size: 50MB</p>
                  <p>• File format: .zip only</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-6 p-4 border flex items-start space-x-3" style={{ backgroundColor: '#fff1f1', borderColor: '#da1e28' }}>
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: '#da1e28' }} />
            <div>
              <p className="font-semibold mb-1" style={{ color: '#da1e28' }}>Upload Failed</p>
              <p className="text-sm" style={{ color: '#da1e28' }}>{error}</p>
            </div>
          </div>
        )}

        {/* Success Result */}
        {uploadResult && (
          <div className="space-y-6">
            {/* Success Header */}
            <div className="p-4 border flex items-start space-x-3" style={{ backgroundColor: '#defbe6', borderColor: '#24a148' }}>
              <CheckCircle className="w-6 h-6 flex-shrink-0 mt-0.5" style={{ color: '#24a148' }} />
              <div className="flex-1">
                <p className="font-semibold text-lg mb-1" style={{ color: '#0e6027' }}>Upload Successful!</p>
                <p style={{ color: '#0e6027' }}>Your code has been processed and is ready for analysis</p>
              </div>
            </div>

            {/* Project Info */}
            <div className="border" style={{ borderColor: '#e0e0e0' }}>
              <div className="p-6" style={{ backgroundColor: '#0f62fe' }}>
                <h2 className="text-2xl font-semibold mb-2 text-white">Project Information</h2>
                <p className="text-sm" style={{ color: '#d0e2ff' }}>Project ID: {uploadResult.project_id}</p>
              </div>

              <div className="p-6 space-y-6">
                {/* File Info */}
                <div>
                  <h3 className="text-lg font-semibold mb-3" style={{ color: '#161616' }}>File Details</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4" style={{ backgroundColor: '#f4f4f4' }}>
                      <p className="text-sm mb-1" style={{ color: '#6f6f6f' }}>Filename</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>{uploadResult.filename}</p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#f4f4f4' }}>
                      <p className="text-sm mb-1" style={{ color: '#6f6f6f' }}>Total Files</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.extraction.total_files}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#f4f4f4' }}>
                      <p className="text-sm mb-1" style={{ color: '#6f6f6f' }}>Code Files</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.extraction.code_files}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Detection Info */}
                <div>
                  <h3 className="text-lg font-semibold mb-3" style={{ color: '#161616' }}>Language Detection</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4" style={{ backgroundColor: '#d0e2ff' }}>
                      <p className="text-sm mb-1" style={{ color: '#0043ce' }}>Language</p>
                      <p className="font-semibold capitalize" style={{ color: '#161616' }}>
                        {uploadResult.detection.language}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#d0e2ff' }}>
                      <p className="text-sm mb-1" style={{ color: '#0043ce' }}>Framework</p>
                      <p className="font-semibold capitalize" style={{ color: '#161616' }}>
                        {uploadResult.detection.framework}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#d0e2ff' }}>
                      <p className="text-sm mb-1" style={{ color: '#0043ce' }}>Confidence</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {(uploadResult.detection.confidence * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#d0e2ff' }}>
                      <p className="text-sm mb-1" style={{ color: '#0043ce' }}>Dependencies</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.detection.dependencies}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Code Analysis */}
                <div>
                  <h3 className="text-lg font-semibold mb-3" style={{ color: '#161616' }}>Code Analysis</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-4" style={{ backgroundColor: '#e8daff' }}>
                      <p className="text-sm mb-1" style={{ color: '#6929c4' }}>Functions</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.parsing.total_functions}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#e8daff' }}>
                      <p className="text-sm mb-1" style={{ color: '#6929c4' }}>Classes</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.parsing.total_classes}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#e8daff' }}>
                      <p className="text-sm mb-1" style={{ color: '#6929c4' }}>Lines of Code</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.parsing.total_lines.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-4" style={{ backgroundColor: '#e8daff' }}>
                      <p className="text-sm mb-1" style={{ color: '#6929c4' }}>Complexity</p>
                      <p className="font-semibold capitalize" style={{ color: '#161616' }}>
                        {uploadResult.parsing.summary.complexity_estimate}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Embeddings */}
                <div>
                  <h3 className="text-lg font-semibold mb-3" style={{ color: '#161616' }}>RAG Indexing</h3>
                  <div className="p-4 flex items-center justify-between" style={{ backgroundColor: '#defbe6' }}>
                    <div>
                      <p className="text-sm mb-1" style={{ color: '#0e6027' }}>Code chunks created for semantic search</p>
                      <p className="font-semibold" style={{ color: '#161616' }}>
                        {uploadResult.embeddings.chunks_created} chunks
                      </p>
                    </div>
                    {uploadResult.embeddings.index_created && (
                      <CheckCircle className="w-8 h-8" style={{ color: '#24a148' }} />
                    )}
                  </div>
                </div>

                {/* Next Steps */}
                <div>
                  <h3 className="text-lg font-semibold mb-3" style={{ color: '#161616' }}>Next Steps</h3>
                  <ul className="space-y-2">
                    {uploadResult.next_steps.map((step, index) => (
                      <li key={index} className="flex items-center space-x-2" style={{ color: '#525252' }}>
                        <CheckCircle className="w-4 h-4" style={{ color: '#0f62fe' }} />
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={handleAnalyze}
                className="px-8 py-3 text-sm font-medium text-white transition-colors flex items-center space-x-2"
                style={{ backgroundColor: '#0f62fe' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
              >
                <CheckCircle className="w-4 h-4" />
                <span>Start Analysis</span>
              </button>
              <button
                onClick={() => {
                  setUploadResult(null)
                  setError(null)
                }}
                className="px-8 py-3 text-sm font-medium border transition-colors"
                style={{ color: '#161616', borderColor: '#8d8d8d' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f4f4f4'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                Upload Another
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
