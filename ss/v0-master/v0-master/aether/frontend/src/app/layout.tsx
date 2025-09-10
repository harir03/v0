import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Aether Agents - The Autonomous Agentic Workforce Platform',
  description: 'Build sophisticated AI agents that can think, code, and operate applications just like a human employee. No-code/low-code platform for creating, deploying, and managing AI agents.',
  keywords: ['AI agents', 'automation', 'no-code', 'low-code', 'artificial intelligence', 'workflow automation'],
  authors: [{ name: 'Aether Agents Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#0a0f1f',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-aether-dark text-white antialiased">
        {children}
      </body>
    </html>
  )
}