import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { TrendingUp, TrendingDown, Zap, Eye, ChevronRight, RefreshCw } from 'lucide-react'
import { useSignalStore } from '../store/signalStore'
import SignalCard from '../components/SignalCard'
import StatCard from '../components/StatCard'
import WatchlistRow from '../components/WatchlistRow'
import api from '../services/api'

export default function Dashboard() {
  const { alerts, setAlerts } = useSignalStore()
  const [stats, setStats] = useState(null)
  const [watchlist, setWatchlist] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [alertsRes, statsRes] = await Promise.all([
          api.get('/api/alerts/feed?limit=5'),
          api.get('/api/alerts/stats'),
        ])
        setAlerts(alertsRes.data.alerts)
        setStats(statsRes.data)

        // Load watchlist
        const symbols = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'BAJFINANCE']
        const quotes = await Promise.all(
          symbols.map((s) => api.get(`/api/stocks/${s}/quote`).then((r) => r.data).catch(() => ({ symbol: s, error: true })))
        )
        setWatchlist(quotes)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-display text-3xl text-white">Signal Dashboard</h1>
          <p className="text-radar-dim text-sm mt-1">
            AI-detected opportunities across NSE/BSE — updated in real time
          </p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="btn-ghost flex items-center gap-2"
        >
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      {/* Stats row */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard label="Stocks scanned" value={stats.stocks_scanned?.toLocaleString('en-IN')} accent />
          <StatCard label="Signals today" value={stats.total_today} />
          <StatCard label="Bullish signals" value={stats.bullish} color="green" />
          <StatCard label="High conviction" value={stats.high_conviction} color="amber" />
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Signal feed — left 2/3 */}
        <div className="xl:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="live-dot" />
              <span className="text-sm font-medium text-white">Latest Signals</span>
            </div>
            <Link to="/signals" className="text-xs text-radar-accent hover:underline flex items-center gap-1">
              View all <ChevronRight size={12} />
            </Link>
          </div>

          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="radar-card animate-pulse h-28 bg-radar-surface" />
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              {alerts.map((alert) => (
                <SignalCard key={alert.id} alert={alert} />
              ))}
            </div>
          )}

          <Link to="/signals" className="block text-center text-sm text-radar-dim hover:text-radar-accent py-3 border border-radar-border rounded-xl transition-colors">
            Load more signals →
          </Link>
        </div>

        {/* Watchlist — right 1/3 */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-white">Watchlist</span>
            <span className="text-xs text-radar-muted">NSE Live</span>
          </div>
          <div className="radar-card p-0 overflow-hidden">
            {loading ? (
              <div className="p-4 text-radar-muted text-sm animate-pulse">Loading quotes...</div>
            ) : (
              <div>
                {watchlist.map((stock, i) => (
                  <WatchlistRow
                    key={stock.symbol}
                    stock={stock}
                    last={i === watchlist.length - 1}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Scanner CTA */}
          <Link
            to="/scanner"
            className="radar-card block hover:border-radar-accent transition-colors cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-radar-accent bg-opacity-10 flex items-center justify-center group-hover:bg-opacity-20 transition-colors">
                <Zap size={18} className="text-radar-accent" />
              </div>
              <div>
                <div className="text-sm font-medium text-white">Run a scan</div>
                <div className="text-xs text-radar-dim">Analyse any NSE stock</div>
              </div>
              <ChevronRight size={14} className="text-radar-muted ml-auto group-hover:text-radar-accent transition-colors" />
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}
