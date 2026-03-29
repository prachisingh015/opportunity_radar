import { Outlet, NavLink } from 'react-router-dom'
import { Activity, Radio, Search, BarChart2, Zap } from 'lucide-react'
import { useEffect, useState } from 'react'

const navItems = [
  { to: '/', icon: Activity, label: 'Dashboard', end: true },
  { to: '/signals', icon: Zap, label: 'Signal Feed' },
  { to: '/scanner', icon: Search, label: 'Scanner' },
]

export default function Layout() {
  const [time, setTime] = useState(new Date())
  const [marketOpen, setMarketOpen] = useState(false)

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date()
      setTime(now)
      const ist = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }))
      const h = ist.getHours(), m = ist.getMinutes()
      const day = ist.getDay()
      setMarketOpen(day >= 1 && day <= 5 && (h > 9 || (h === 9 && m >= 15)) && h < 15)
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const istTime = time.toLocaleTimeString('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })

  return (
    <div className="flex min-h-screen bg-radar-bg">
      {/* Sidebar */}
      <aside className="w-64 border-r border-radar-border flex flex-col sticky top-0 h-screen">
        {/* Logo */}
        <div className="p-6 border-b border-radar-border">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-radar-accent bg-opacity-15 flex items-center justify-center">
              <Radio size={16} className="text-radar-accent" />
            </div>
            <div>
              <div className="font-display text-white text-lg leading-none">Opportunity</div>
              <div className="font-display text-radar-accent text-lg leading-none">Radar</div>
            </div>
          </div>
          <div className="mt-3 text-xs text-radar-muted font-mono">ET AI Hackathon 2026 · PS 6</div>
        </div>

        {/* Market Status */}
        <div className="px-5 py-3 border-b border-radar-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className={marketOpen ? 'live-dot' : 'w-2 h-2 rounded-full bg-radar-muted'} />
              <span className="text-xs text-radar-dim">
                {marketOpen ? 'Market Open' : 'Market Closed'}
              </span>
            </div>
            <span className="text-xs font-mono text-radar-dim">{istTime} IST</span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-radar-accent bg-opacity-10 text-radar-accent border border-radar-accent border-opacity-20'
                    : 'text-radar-dim hover:text-radar-text hover:bg-radar-surface'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-5 border-t border-radar-border">
          <div className="text-xs text-radar-muted leading-relaxed">
            Scanning NSE/BSE filings, insider trades & management commentary in real time.
          </div>
          <div className="mt-2 text-xs font-mono text-radar-muted">
            Powered by GPT-4o + LangGraph
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
