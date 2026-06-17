import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'AuraCart | AI-Powered Premium Retail',
  description: 'Experience personalized shopping with cutting-edge AI recommendations.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="navbar glass">
          <div className="logo gradient-text">AuraCart.</div>
          <div style={{ display: 'flex', gap: '2rem' }}>
            <a href="/" style={{ color: 'white', textDecoration: 'none' }}>Home</a>
            <a href="/cart" style={{ color: 'white', textDecoration: 'none' }}>Cart</a>
          </div>
        </nav>
        <main style={{ paddingTop: '80px' }} className="page-transition">
          {children}
        </main>
      </body>
    </html>
  )
}
