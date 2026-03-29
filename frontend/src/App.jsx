import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import StockDetail from './pages/StockDetail'
import SignalFeed from './pages/SignalFeed'
import Scanner from './pages/Scanner'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="signals" element={<SignalFeed />} />
        <Route path="scanner" element={<Scanner />} />
        <Route path="stock/:symbol" element={<StockDetail />} />
      </Route>
    </Routes>
  )
}
