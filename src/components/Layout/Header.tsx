import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, User, LogOut } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [showAuthModal, setShowAuthModal] = useState<'login' | 'register' | null>(null)
  const { profile, signOut, user } = useAuth()
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  const handleAuthClick = (type: 'login' | 'register') => {
    setShowAuthModal(type)
  }

  const navLinks = [
    { path: '/', label: 'Inicio' },
    { path: '/services', label: 'Servicios' },
    { path: '/properties', label: 'Propiedades' },
    { path: '/professionals', label: 'Profesionales' },
    { path: '/profile', label: 'Perfil' },
  ]

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <Link to="/" className="flex items-center gap-2 flex-shrink-0">
            <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-blue-600 rounded-lg flex items-center justify-center shadow-md">
              <span className="text-xl">🇬🇶</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              abitaX
            </span>
          </Link>

          <nav className="hidden lg:flex items-center gap-8 flex-1 justify-center">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`font-semibold text-sm transition-colors relative pb-1 ${
                  isActive(link.path)
                    ? 'text-gray-900'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {link.label}
                {isActive(link.path) && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900 rounded-full" />
                )}
              </Link>
            ))}
          </nav>

          <div className="hidden lg:flex items-center gap-3 flex-shrink-0">
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-3 px-4 py-2 border border-gray-300 rounded-full hover:shadow-md transition-shadow"
                >
                  <Menu className="w-4 h-4 text-gray-600" />
                  {profile?.avatar_url ? (
                    <img
                      src={profile.avatar_url}
                      alt={profile.full_name}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-600 to-blue-600 flex items-center justify-center text-white font-bold">
                      {profile?.full_name?.[0]?.toUpperCase() || 'U'}
                    </div>
                  )}
                </button>

                {userMenuOpen && (
                  <>
                    <div
                      className="fixed inset-0 z-40"
                      onClick={() => setUserMenuOpen(false)}
                    />
                    <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-gray-100 py-2 z-50">
                      <div className="px-4 py-3 border-b border-gray-100">
                        <p className="font-semibold text-gray-900">{profile?.full_name}</p>
                        <p className="text-sm text-gray-500">{user.email}</p>
                      </div>
                      <Link
                        to="/profile"
                        className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 text-gray-700 font-medium"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        <User className="w-4 h-4" />
                        Mi Perfil
                      </Link>
                      <hr className="my-2" />
                      <button
                        onClick={() => {
                          signOut()
                          setUserMenuOpen(false)
                        }}
                        className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 text-red-600 w-full font-medium"
                      >
                        <LogOut className="w-4 h-4" />
                        Cerrar Sesión
                      </button>
                    </div>
                  </>
                )}
              </div>
            ) : (
              <>
                <button
                  onClick={() => handleAuthClick('login')}
                  className="px-6 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50 rounded-full transition-colors"
                >
                  Iniciar sesión
                </button>
                <button
                  onClick={() => handleAuthClick('register')}
                  className="px-6 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-full transition-all shadow-md hover:shadow-lg"
                >
                  Registrar aquí
                </button>
              </>
            )}
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-50 transition-colors"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <>
          <div
            className="fixed inset-0 bg-black/30 z-40 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
          <div className="lg:hidden absolute top-full left-0 right-0 bg-white border-b border-gray-200 shadow-lg z-50">
            <nav className="px-4 py-6 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`block px-4 py-3 rounded-lg font-semibold transition-colors ${
                    isActive(link.path)
                      ? 'bg-gray-100 text-gray-900'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}

              {user ? (
                <>
                  <hr className="my-4" />
                  <div className="px-4 py-2">
                    <p className="font-semibold text-gray-900">{profile?.full_name}</p>
                    <p className="text-sm text-gray-500">{user.email}</p>
                  </div>
                  <button
                    onClick={() => {
                      signOut()
                      setMobileMenuOpen(false)
                    }}
                    className="block w-full text-left px-4 py-3 rounded-lg font-semibold text-red-600 hover:bg-red-50"
                  >
                    Cerrar Sesión
                  </button>
                </>
              ) : (
                <>
                  <hr className="my-4" />
                  <button
                    onClick={() => {
                      handleAuthClick('login')
                      setMobileMenuOpen(false)
                    }}
                    className="block w-full px-4 py-3 text-center rounded-lg font-semibold text-gray-700 border-2 border-gray-900 hover:bg-gray-50"
                  >
                    Iniciar sesión
                  </button>
                  <button
                    onClick={() => {
                      handleAuthClick('register')
                      setMobileMenuOpen(false)
                    }}
                    className="block w-full px-4 py-3 text-center rounded-lg font-semibold text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800"
                  >
                    Registrar aquí
                  </button>
                </>
              )}
            </nav>
          </div>
        </>
      )}

      {showAuthModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl">
              <h3 className="text-xl font-bold">
                {showAuthModal === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}
              </h3>
              <button
                onClick={() => setShowAuthModal(null)}
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6">
              {showAuthModal === 'login' ? (
                <LoginForm onSuccess={() => setShowAuthModal(null)} />
              ) : (
                <RegisterForm onSuccess={() => setShowAuthModal(null)} />
              )}
              <div className="mt-6 text-center">
                {showAuthModal === 'login' ? (
                  <p className="text-sm text-gray-600">
                    ¿No tienes cuenta?{' '}
                    <button
                      onClick={() => setShowAuthModal('register')}
                      className="text-green-600 font-semibold hover:text-green-700"
                    >
                      Regístrate aquí
                    </button>
                  </p>
                ) : (
                  <p className="text-sm text-gray-600">
                    ¿Ya tienes cuenta?{' '}
                    <button
                      onClick={() => setShowAuthModal('login')}
                      className="text-green-600 font-semibold hover:text-green-700"
                    >
                      Inicia sesión
                    </button>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}

import Login from '../Auth/Login'
import Register from '../Auth/Register'

function LoginForm({ onSuccess }: { onSuccess: () => void }) {
  return <Login onSuccess={onSuccess} inModal={true} />
}

function RegisterForm({ onSuccess }: { onSuccess: () => void }) {
  return <Register onSuccess={onSuccess} inModal={true} />
}
