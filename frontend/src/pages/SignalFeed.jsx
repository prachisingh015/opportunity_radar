import { useEffect, useState } from 'react'
import { Filter, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import api from '../services/api'
import SignalCard from '../components/SignalCard'

const FILTERS = ['All', 'Bullish', 'Bearish', 'Today', 'High conviction']
const TAGS = ['INSIDER BUY', 'EARNINGS BEAT', 'MANAGEMENT UPGRADE', 'DIVIDEND', 'FILING ALERT']

export default function SignalFeed() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('All')
  const [tagFilter, setTagFilter] = useState(null)

  useEffect(() => {
    api.get('/api/alerts/feed?limit=20')
      .then((r) => setAlerts(r.data.alerts))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = alerts.filter((a) => {
    if (filter === 'Bullish' && a.direction !== 'bullish') return false
    if (filter === 'Bearish' && a.direction !== 'bearish') return false
    if (filter === 'High conviction' && a.score < 85) return false
    if (tagFilter && a.tag !== tagFilter) return false
    return true
  })

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="font-display text-3xl text-white">Signal Feed</h1>
        <p className="text-radar-dim text-sm mt-1">
          Real-time AI-detected signals across the NSE universe
        </p>
      </div>

      {/* Direction filters */}
      <div className="flex gap-2 mb-4 flex-wrap">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${
              filter === f
                ? 'border-radar-accent text-radar-accent bg-radar-accent bg-opacity-10'
                : 'border-radar-border text-radar-dim hover:border-radar-accent hover:text-radar-accent'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Tag filters */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {TAGS.map((t) => (
          <button
            key={t}
            onClick={() => setTagFilter(tagFilter === t ? null : t)}
            className={`font-mono text-xs px-2 py-1 rounded transition-colors ${
              tagFilter === t
                ? 'bg-radar-accent bg-opacity-15 text-radar-accent'
                : 'bg-radar-surface text-radar-muted hover:text-radar-dim'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Feed */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="radar-card animate-pulse h-28 bg-radar-surface" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 text-radar-muted">
          <Filter size={32} className="mx-auto mb-3 opacity-30" />
          <p>No signals match this filter</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((alert) => (
            <SignalCard key={alert.id} alert={alert} showScore />
          ))}
        </div>
      )}
    </div>
  )
}
