import { useState, useRef } from 'react'
import { Search, Loader2, Zap, TrendingUp, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'
import api from '../services/api'
import SignalCard from '../components/SignalCard'

const POPULAR = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'BAJFINANCE', 'TATAMOTORS', 'WIPRO', 'SUNPHARMA']

export default function Scanner() {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [expandedAgent, setExpandedAgent] = useState(null)
  const inputRef = useRef(null)

  const searchStocks = async (q) => {
    setQuery(q)
    if (q.length < 2) { setSuggestions([]); return }
    try {
      const res = await api.get(`/api/stocks/search?q=${q}`)
      setSuggestions(res.data.results || [])
    } catch { setSuggestions([]) }
  }

  const runScan = async (symbol) => {
    setQuery(symbol)
    setSuggestions([])
    setScanning(true)
    setResult(null)
    setError(null)

    try {
      const res = await api.post('/api/signals/scan', { symbol })
      setResult(res.data)
    } catch (e) {
      setError('Scan failed. Please try again.')
    } finally {
      setScanning(false)
    }
  }

  const directionColor = (d) =>
    d === 'bullish' ? 'text-radar-green' : d === 'bearish' ? 'text-radar-red' : 'text-radar-dim'

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="font-display text-3xl text-white">Stock Scanner</h1>
        <p className="text-radar-dim text-sm mt-1">
          Enter any NSE symbol — our 5 AI agents will scan filings, insider trades & management commentary
        </p>
      </div>

      {/* Search box */}
      <div className="relative mb-6">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-radar-muted" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => searchStocks(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && query && runScan(query.toUpperCase())}
              placeholder="Search symbol e.g. RELIANCE, TCS, INFY..."
              className="w-full bg-radar-surface border border-radar-border rounded-xl pl-10 pr-4 py-3.5 text-sm text-radar-text placeholder-radar-muted focus:outline-none focus:border-radar-accent transition-colors"
            />
            {/* Suggestions */}
            {suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-radar-card border border-radar-border rounded-xl overflow-hidden z-10 shadow-xl">
                {suggestions.map((s) => (
                  <button
                    key={s.symbol}
                    onClick={() => runScan(s.symbol)}
                    className="w-full flex items-center justify-between px-4 py-3 hover:bg-radar-surface text-sm transition-colors"
                  >
                    <span className="font-mono font-medium text-radar-accent">{s.symbol}</span>
                    <span className="text-radar-dim">{s.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
          <button
            onClick={() => query && runScan(query.toUpperCase())}
            disabled={scanning || !query}
            className="btn-primary flex items-center gap-2 px-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {scanning ? <Loader2 size={15} className="animate-spin" /> : <Zap size={15} />}
            {scanning ? 'Scanning...' : 'Scan'}
          </button>
        </div>
      </div>

      {/* Popular chips */}
      {!result && !scanning && (
        <div>
          <p className="text-xs text-radar-muted mb-3">Popular stocks</p>
          <div className="flex flex-wrap gap-2">
            {POPULAR.map((s) => (
              <button
                key={s}
                onClick={() => runScan(s)}
                className="font-mono text-xs px-3 py-1.5 bg-radar-surface border border-radar-border rounded-lg text-radar-dim hover:text-radar-accent hover:border-radar-accent transition-colors"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Scanning animation */}
      {scanning && (
        <div className="radar-card radar-sweep mt-6">
          <div className="space-y-4">
            {['FilingWatcher', 'InsiderTracker', 'SentimentAnalyser', 'SignalRanker', 'AlertDispatcher'].map((agent, i) => (
              <div key={agent} className="flex items-center gap-3" style={{ animationDelay: `${i * 0.3}s` }}>
                <Loader2 size={14} className="animate-spin text-radar-accent flex-shrink-0" />
                <span className="text-sm font-mono text-radar-dim">{agent}</span>
                <span className="text-xs text-radar-muted">— scanning {query}...</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="radar-card mt-6 border-radar-red border-opacity-40 flex items-center gap-3">
          <AlertTriangle size={16} className="text-radar-red" />
          <span className="text-sm text-radar-red">{error}</span>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-6 space-y-6 animate-fade-up">
          {/* Summary */}
          <div className="radar-card">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="font-mono font-medium text-radar-accent text-lg">{result.symbol}</div>
                <div className="text-xs text-radar-muted mt-0.5">{result.total_signals} signals detected</div>
              </div>
              <div className="text-right">
                <div className="text-xs text-radar-muted">Management tone</div>
                <div className={`text-sm font-medium mt-0.5 ${directionColor(result.sentiment?.overall_tone)}`}>
                  {result.sentiment?.overall_tone?.toUpperCase() || 'MIXED'}
                </div>
                <div className="text-xs text-radar-muted">{result.sentiment?.tone_shift} trend</div>
              </div>
            </div>
            <div className="flex gap-2">
              {result.alerts?.map((a) => (
                <span key={a.id} className={`signal-tag ${
                  a.direction === 'bullish' ? 'bg-green-950 text-radar-green' :
                  a.direction === 'bearish' ? 'bg-red-950 text-radar-red' :
                  'bg-radar-surface text-radar-dim'
                }`}>{a.tag}</span>
              ))}
            </div>
          </div>

          {/* Alert cards */}
          <div>
            <h3 className="text-sm font-medium text-white mb-3">AI-Generated Alerts</h3>
            <div className="space-y-3">
              {result.alerts?.map((alert) => (
                <SignalCard key={alert.id} alert={alert} showScore />
              ))}
            </div>
          </div>

          {/* Ranked signals detail */}
          {result.ranked_signals?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-white mb-3">All Ranked Signals</h3>
              <div className="space-y-2">
                {result.ranked_signals.map((sig, i) => (
                  <div key={i} className="radar-card">
                    <button
                      className="w-full flex items-center justify-between"
                      onClick={() => setExpandedAgent(expandedAgent === i ? null : i)}
                    >
                      <div className="flex items-center gap-3">
                        <span className="font-mono text-xs text-radar-muted w-5">#{sig.rank}</span>
                        <span className={`text-sm font-medium ${directionColor(sig.direction)}`}>
                          {sig.title}
                        </span>
                        {sig.confluence && (
                          <span className="text-xs bg-amber-950 text-radar-amber px-2 py-0.5 rounded font-mono">
                            CONFLUENCE
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-mono text-xs text-radar-accent">{sig.score}</span>
                        {expandedAgent === i ? <ChevronUp size={14} className="text-radar-muted" /> : <ChevronDown size={14} className="text-radar-muted" />}
                      </div>
                    </button>
                    {expandedAgent === i && (
                      <div className="mt-3 pt-3 border-t border-radar-border space-y-2">
                        <p className="text-sm text-radar-dim">{sig.description}</p>
                        <div className="flex items-center gap-4 text-xs text-radar-muted">
                          <span>Urgency: <span className="text-radar-text">{sig.urgency}</span></span>
                          <span>Type: <span className="text-radar-text">{sig.type}</span></span>
                        </div>
                        {sig.action && (
                          <div className="mt-2 p-3 bg-radar-surface rounded-lg border border-radar-border">
                            <span className="text-xs text-radar-muted block mb-1">Suggested action</span>
                            <span className="text-sm text-white">{sig.action}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
