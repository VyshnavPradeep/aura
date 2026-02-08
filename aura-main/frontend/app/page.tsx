'use client'

import { useRouter } from 'next/navigation'
import { Shield, TestTube, Zap, Database, Upload, FolderOpen, ArrowRight, Check } from 'lucide-react'

export default function HomePage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-white">
      {/* Header - IBM Cloud Style */}
      <header className="bg-gray-100 border-b border-gray-20 sticky top-0 z-50">
        <div className="container mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Shield className="w-7 h-7 text-gray-100" style={{ color: '#0f62fe' }} />
              <h1 className="text-xl font-semibold text-gray-100" style={{ color: '#161616' }}>AURA</h1>
              <span className="text-sm text-gray-60 ml-2">Code Analysis Platform</span>
            </div>
            <nav className="flex items-center space-x-1">
              <button
                onClick={() => router.push('/projects')}
                className="px-4 py-2 text-sm font-medium text-gray-100 hover:bg-gray-10 transition-colors"
                style={{ color: '#161616' }}
              >
                Projects
              </button>
              <button
                onClick={() => router.push('/upload')}
                className="ml-4 px-6 py-2 text-sm font-medium text-white transition-colors"
                style={{ backgroundColor: '#0f62fe' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
              >
                Upload code
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="border-b" style={{ borderColor: '#e0e0e0' }}>
        <div className="container mx-auto px-6 py-20">
          <div className="max-w-4xl">
            <h2 className="text-5xl font-light mb-6" style={{ color: '#161616' }}>
              Autonomous code analysis
              <span className="block font-semibold mt-2" style={{ color: '#0f62fe' }}>powered by AI</span>
            </h2>
            <p className="text-xl mb-8" style={{ color: '#525252' }} className="leading-relaxed">
              Upload your backend code and let AI-powered agents analyze security vulnerabilities,
              generate tests, identify scalability issues, and optimize database queries.
            </p>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/upload')}
                className="px-6 py-3 text-sm font-medium text-white flex items-center space-x-2 transition-colors"
                style={{ backgroundColor: '#0f62fe' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
              >
                <Upload className="w-4 h-4" />
                <span>Upload code</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => router.push('/projects')}
                className="px-6 py-3 text-sm font-medium border transition-colors flex items-center space-x-2"
                style={{ color: '#0f62fe', borderColor: '#0f62fe' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f4f4f4'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                <FolderOpen className="w-4 h-4" />
                <span>View projects</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-20">
        <h3 className="text-3xl font-light mb-2" style={{ color: '#161616' }}>
          Four specialized AI agents
        </h3>
        <p className="text-lg mb-12" style={{ color: '#525252' }}>
          Comprehensive code analysis across security, testing, scalability, and database optimization
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Security Agent */}
          <div className="border p-6 hover:shadow-card-hover transition-shadow" style={{ borderColor: '#e0e0e0' }}>
            <div className="w-12 h-12 flex items-center justify-center mb-4" style={{ backgroundColor: '#fff1f1' }}>
              <Shield className="w-6 h-6" style={{ color: '#da1e28' }} />
            </div>
            <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>Security Agent</h4>
            <p className="text-sm mb-4" style={{ color: '#525252' }}>
              Detects SQL injection, XSS, hardcoded secrets, and other vulnerabilities using AI-powered analysis.
            </p>
            <ul className="space-y-2 text-sm" style={{ color: '#6f6f6f' }}>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Pattern-based scanning</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Gemini AI analysis</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />RAG-powered search</li>
            </ul>
          </div>

          {/* Test Generator */}
          <div className="border p-6 hover:shadow-card-hover transition-shadow" style={{ borderColor: '#e0e0e0' }}>
            <div className="w-12 h-12 flex items-center justify-center mb-4" style={{ backgroundColor: '#defbe6' }}>
              <TestTube className="w-6 h-6" style={{ color: '#24a148' }} />
            </div>
            <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>Test Generator</h4>
            <p className="text-sm mb-4" style={{ color: '#525252' }}>
              Automatically generates unit and integration tests with comprehensive edge case coverage.
            </p>
            <ul className="space-y-2 text-sm" style={{ color: '#6f6f6f' }}>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Pytest/Jest templates</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Coverage analysis</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Edge case detection</li>
            </ul>
          </div>

          {/* Scalability Agent */}
          <div className="border p-6 hover:shadow-card-hover transition-shadow" style={{ borderColor: '#e0e0e0' }}>
            <div className="w-12 h-12 flex items-center justify-center mb-4" style={{ backgroundColor: '#fcf4d6' }}>
              <Zap className="w-6 h-6" style={{ color: '#8e6a00' }} />
            </div>
            <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>Scalability Agent</h4>
            <p className="text-sm mb-4" style={{ color: '#525252' }}>
              Identifies N+1 queries, inefficient algorithms, and performance bottlenecks.
            </p>
            <ul className="space-y-2 text-sm" style={{ color: '#6f6f6f' }}>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Performance analysis</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Scalability scoring</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Optimization tips</li>
            </ul>
          </div>

          {/* Database Agent */}
          <div className="border p-6 hover:shadow-card-hover transition-shadow" style={{ borderColor: '#e0e0e0' }}>
            <div className="w-12 h-12 flex items-center justify-center mb-4" style={{ backgroundColor: '#e8daff' }}>
              <Database className="w-6 h-6" style={{ color: '#8a3ffc' }} />
            </div>
            <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>Database Agent</h4>
            <p className="text-sm mb-4" style={{ color: '#525252' }}>
              Optimizes queries, detects missing indexes, and analyzes database schema issues.
            </p>
            <ul className="space-y-2 text-sm" style={{ color: '#6f6f6f' }}>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Query optimization</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Schema analysis</li>
              <li className="flex items-center"><Check className="w-4 h-4 mr-2" style={{ color: '#24a148' }} />Health scoring</li>
            </ul>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="border-t" style={{ borderColor: '#e0e0e0', backgroundColor: '#f4f4f4' }}>
        <div className="container mx-auto px-6 py-20">
          <h3 className="text-3xl font-light mb-12" style={{ color: '#161616' }}>
            How it works
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-5xl">
            <div>
              <div className="w-12 h-12 flex items-center justify-center text-xl font-semibold mb-4" style={{ backgroundColor: '#0f62fe', color: 'white' }}>
                1
              </div>
              <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>Upload code</h4>
              <p style={{ color: '#525252' }}>
                Upload your backend code as a ZIP file. Supports Python, JavaScript, Java, and Go.
              </p>
            </div>
            <div>
              <div className="w-12 h-12 flex items-center justify-center text-xl font-semibold mb-4" style={{ backgroundColor: '#0f62fe', color: 'white' }}>
                2
              </div>
              <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>AI analysis</h4>
              <p style={{ color: '#525252' }}>
                Four specialized agents analyze your code in parallel using Google Gemini AI.
              </p>
            </div>
            <div>
              <div className="w-12 h-12 flex items-center justify-center text-xl font-semibold mb-4" style={{ backgroundColor: '#0f62fe', color: 'white' }}>
                3
              </div>
              <h4 className="text-lg font-semibold mb-2" style={{ color: '#161616' }}>View results</h4>
              <p style={{ color: '#525252' }}>
                Get comprehensive findings with severity levels, code snippets, and fix recommendations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <h3 className="text-3xl font-light mb-4" style={{ color: '#161616' }}>
          Ready to analyze your code?
        </h3>
        <p className="text-lg mb-8" style={{ color: '#525252' }}>
          Start your free code analysis in seconds
        </p>
        <button
          onClick={() => router.push('/upload')}
          className="px-8 py-3 text-sm font-medium text-white inline-flex items-center space-x-2 transition-colors"
          style={{ backgroundColor: '#0f62fe' }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0353e9'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f62fe'}
        >
          <Upload className="w-4 h-4" />
          <span>Upload your code now</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </section>

      {/* Footer */}
      <footer className="border-t" style={{ borderColor: '#e0e0e0', backgroundColor: '#f4f4f4' }}>
        <div className="container mx-auto px-6 py-8">
          <div className="text-center text-sm" style={{ color: '#6f6f6f' }}>
            <p className="mb-1">AURA v2.0.0 - Autonomous Understanding and Review Agent</p>
            <p>Powered by Google Gemini AI</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
