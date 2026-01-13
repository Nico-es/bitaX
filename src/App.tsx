import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Header from './components/Layout/Header'
import BottomNav from './components/Layout/BottomNav'
import Login from './components/Auth/Login'
import Register from './components/Auth/Register'
import Home from './pages/Home'
import Services from './pages/Services'
import Properties from './pages/Properties'
import Professionals from './pages/Professionals'
import Profile from './pages/Profile'

function AuthGate() {
  const [showLogin, setShowLogin] = useState(true)
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-lg mx-auto mb-4">
            <span className="text-5xl">🇬🇶</span>
          </div>
          <div className="inline-block w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
          <p className="text-white text-xl mt-4 font-semibold">Cargando abitaX...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return showLogin ? (
      <Login onSwitchToRegister={() => setShowLogin(false)} />
    ) : (
      <Register onSwitchToLogin={() => setShowLogin(true)} />
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/services" element={<Services />} />
        <Route path="/properties" element={<Properties />} />
        <Route path="/professionals" element={<Professionals />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Profile />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <BottomNav />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AuthGate />
      </AuthProvider>
    </BrowserRouter>
  )
}
