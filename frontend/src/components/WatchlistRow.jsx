import { Link } from 'react-router-dom'

export default function WatchlistRow({ stock, last }) {
  if (stock.error) {
    return (
      <div className={`flex items-center justify-between px-4 py-3 ${!last ? 'border-b border-radar-border' : ''}`}>
        <span className="font-mono text-sm text-radar-accent">{stock.symbol}</span>
        <span className="text-xs text-radar-muted">unavailable</span>
      </div>
    )
  }

  const isUp = stock.change >= 0

  return (
    <Link
      to={`/stock/${stock.symbol}`}
      className={`flex items-center justify-between px-4 py-3 hover:bg-radar-surface transition-colors ${
        !last ? 'border-b border-radar-border' : ''
      }`}
    >
      <div>
        <div className="font-mono text-sm font-medium text-radar-accent">{stock.symbol}</div>
        <div className="text-xs text-radar-muted">Vol {(stock.volume / 1e5).toFixed(1)}L</div>
      </div>
      <div className="text-right">
        <div className="text-sm font-medium text-white">₹{stock.price?.toLocaleString('en-IN')}</div>
        <div className={`text-xs ${isUp ? 'text-radar-green' : 'text-radar-red'}`}>
          {isUp ? '+' : ''}{stock.change_pct?.toFixed(2)}%
        </div>
      </div>
    </Link>
  )
}
