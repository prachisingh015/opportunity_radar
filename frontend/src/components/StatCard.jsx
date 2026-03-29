// StatCard — summary metric
export function StatCard({ label, value, accent, color }) {
  const textColor =
    color === 'green' ? 'text-radar-green' :
    color === 'amber' ? 'text-radar-amber' :
    accent ? 'text-radar-accent' :
    'text-white'

  return (
    <div className="bg-radar-surface rounded-xl p-4 border border-radar-border">
      <div className="text-xs text-radar-muted mb-1">{label}</div>
      <div className={`text-2xl font-medium ${textColor}`}>{value ?? '—'}</div>
    </div>
  )
}

export default StatCard
