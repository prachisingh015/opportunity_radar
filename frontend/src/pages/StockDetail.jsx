import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, TrendingUp, TrendingDown } from 'lucide-react'
import { useEffect, useState, useRef } from 'react'
import { createChart } from 'lightweight-charts'
import api from '../services/api'

export default function StockDetail() {
  const { symbol } = useParams()
  const [quote, setQuote] = useState(null)
  const [loading, setLoading] = useState(true)
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [quoteRes, histRes] = await Promise.all([
          api.get(`/api/stocks/${symbol}/quote`),
          api.get(`/api/stocks/${symbol}/history?period=3mo`),
        ])
        setQuote(quoteRes.data)

        // Build lightweight-charts candlestick
        if (chartRef.current && histRes.data.candles?.length > 0) {
          if (chartInstance.current) chartInstance.current.remove()
          const chart = createChart(chartRef.current, {
            width: chartRef.current.offsetWidth,
            height: 300,
            layout: { background: { color: '#111827' }, textColor: '#8899BB' },
            grid: { vertLines: { color: '#1E2D45' }, horzLines: { color: '#1E2D45' } },
            crosshair: { mode: 1 },
            rightPriceScale: { borderColor: '#1E2D45' },
            timeScale: { borderColor: '#1E2D45' },
          })
          chartInstance.current = chart

          const candleSeries = chart.addCandlestickSeries({
            upColor: '#00E676',
            downColor: '#FF4757',
            borderUpColor: '#00E676',
            borderDownColor: '#FF4757',
            wickUpColor: '#00E676',
            wickDownColor: '#FF4757',
          })

          const data = histRes.data.candles.map((c) => ({
            time: c.date,
            open: c.open,
            high: c.high,
            low: c.low,
            close: c.close,
          }))
          candleSeries.setData(data)
          chart.timeScale().fitContent()
        }
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
    return () => { if (chartInstance.current) chartInstance.current.remove() }
  }, [symbol])

  const isUp = quote?.change >= 0

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <Link to="/" className="flex items-center gap-2 text-radar-dim hover:text-radar-text text-sm mb-6 transition-colors">
        <ArrowLeft size={14} /> Back to dashboard
      </Link>

      {loading ? (
        <div className="radar-card animate-pulse h-64" />
      ) : (
        <>
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="font-display text-4xl text-white">{symbol}</h1>
              <div className="flex items-center gap-3 mt-2">
                <span className="text-2xl font-medium text-white">₹{quote?.price?.toLocaleString('en-IN')}</span>
                <span className={`flex items-center gap-1 text-sm ${isUp ? 'text-radar-green' : 'text-radar-red'}`}>
                  {isUp ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                  {isUp ? '+' : ''}{quote?.change} ({isUp ? '+' : ''}{quote?.change_pct}%)
                </span>
              </div>
            </div>
            <div className="text-right text-sm text-radar-muted space-y-1">
              <div>52W High: <span className="text-radar-text">₹{quote?.high_52w?.toLocaleString('en-IN')}</span></div>
              <div>52W Low: <span className="text-radar-text">₹{quote?.low_52w?.toLocaleString('en-IN')}</span></div>
              <div>Volume: <span className="text-radar-text">{quote?.volume?.toLocaleString('en-IN')}</span></div>
            </div>
          </div>

          {/* Chart */}
          <div className="radar-card p-0 overflow-hidden mb-6">
            <div ref={chartRef} className="w-full" />
          </div>

          {/* Scan CTA */}
          <Link
            to={`/scanner?symbol=${symbol}`}
            className="btn-primary inline-flex items-center gap-2"
          >
            Run AI Signal Scan for {symbol} →
          </Link>
        </>
      )}
    </div>
  )
}
