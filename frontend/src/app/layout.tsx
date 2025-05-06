import './globals.css'

export const metadata = {
  title: 'LLM Q&A Application',
  description: 'An interactive Q&A system using LLM integration',
}

import { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-red-500 min-h-screen">
        {children}
      </body>
    </html>
  )
}