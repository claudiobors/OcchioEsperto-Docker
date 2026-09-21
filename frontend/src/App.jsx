import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import { ToastProvider } from './context/ToastContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Analisi from './pages/Analisi'
import Pricing from './pages/Pricing'
import Terms from './pages/Terms'
import Privacy from './pages/Privacy'
import NotFound from './pages/NotFound'
import AuthLayout from './components/AuthLayout'
import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

function RoutePosition() {
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'instant' }) }, [pathname])
  return null
}

function App() {
  return (
    <ToastProvider>
      <RoutePosition />
      <div className="oe-shell min-h-screen flex flex-col">
        <Navbar />
        <main id="main-content" tabIndex={-1} className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<AuthLayout><Login /></AuthLayout>} />
            <Route path="/register" element={<AuthLayout><Register /></AuthLayout>} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analisi" element={<Analisi />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="/privacy" element={<Privacy />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </ToastProvider>
  )
}

export default App
