import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AURA - AI Code Analysis Platform',
  description: 'Autonomous Understanding and Review Agent for comprehensive code analysis',
  icons: {
    icon: [
      { url: '/favicon.png', type: 'image/png' },
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
