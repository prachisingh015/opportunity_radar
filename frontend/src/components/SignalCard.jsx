import { Link } from 'react-router-dom'
import { TrendingUp, TrendingDown, Minus, Clock } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const TAG_COLORS = {
  'INSIDER BUY':        'bg-green-950 text-green-400',
  'EARNINGS BEAT':      'bg-blue-950 text-blue-400',
  'MANAGEMENT UPGRADE': 'bg-purple-950 text-purple-400',
  'DIVIDEND':           'bg-amber-950 text-amber-400',
  'FILING ALERT':       'bg-red-950 text-red-400',
}

const URGENCY_LABEL = {
  today:      { label: 'Today', color: 'text-radar-red' },
  this_week:  { label: 'This week', color: 'text-radar-amber' },
  this_month: { label: 'This month', color: 'text-radar-dim' },
}

export default function SignalCard({ alert, showScore = false }) {
  const isUp = alert.direction === 'bullish'
  const isDown = alert.direction === 'bearish'
  const urgency = URGENCY_LABEL[alert.urgency] || URGENCY_LABEL.this_week

  const timeAgo = (() => {
    try {
      return formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })
    } catch {
      return ''
    }
  })()

  return (
    <div className="radar-card hover:border-radar-accent hover:border-opacity-40 transition-colors animate-slide-in group">
      <div className="flex items-start gap-4">
        {/* Direction icon */}
        <div className={`flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center mt-0.5 ${
          isUp ? 'bg-green-950' : isDown ? 'bg-red-950' : 'bg-radar-surface'
        }`}>
          {isUp ? (
            <TrendingUp size={16} className="text-radar-green" />
          ) : isDown ? (
            <TrendingDown size={16} className="text-radar-red" />
          ) : (
            <Minus size={16} className="text-radar-dim" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <Link
              to={`/stock/${alert.symbol}`}
              className="font-mono text-sm font-medium text-radar-accent hover:underline"
            >
              {alert.symbol}
            </Link>
            <span className={`signal-tag ${TAG_COLORS[alert.tag] || 'bg-radar-surface text-radar-dim'}`}>
              {alert.tag}
            </span>
            <span className={`text-xs ${urgency.color}`}>{urgency.label}</span>
          </div>

          <h3 className="text-sm font-medium text-white mb-1 leading-snug">{alert.headline}</h3>
          <p className="text-sm text-radar-dim leading-relaxed line-clamp-2">{alert.body}</p>

          <div className="flex items-center justify-between mt-3">
            <div className="flex items-center gap-1 text-xs text-radar-muted">
              <Clock size={11} />
              <span>{timeAgo}</span>
            </div>

            {showScore && (
              <div className="flex items-center gap-2">
                <div className="score-bar w-20">
                  <div
                    className={`score-fill ${isUp ? 'bg-radar-green' : isDown ? 'bg-radar-red' : 'bg-radar-accent'}`}
                    style={{ width: `${alert.score}%` }}
                  />
                </div>
                <span className="font-mono text-xs text-radar-dim">{alert.score}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
