import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, User, LogOut, Settings } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const { profile, signOut } = useAuth()
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-green-ge to-blue-ge rounded-lg flex items-center justify-center">
              <span className="text-2xl">🇬🇶</span>
            </div>
            <span className="text-xl font-bold text-gray-900">abitaX</span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className={`font-medium transition-colors ${
                isActive('/') ? 'text-green-ge' : 'text-gray-600 hover:text-green-ge'
              }`}
            >
              Inicio
            </Link>
            <Link
              to="/services"
              className={`font-medium transition-colors ${
                isActive('/services') ? 'text-green-ge' : 'text-gray-600 hover:text-green-ge'
              }`}
            >
              Servicios
            </Link>
            <Link
              to="/properties"
              className={`font-medium transition-colors ${
                isActive('/properties') ? 'text-green-ge' : 'text-gray-600 hover:text-green-ge'
              }`}
            >
              Propiedades
            </Link>
            <Link
              to="/professionals"
              className={`font-medium transition-colors ${
                isActive('/professionals') ? 'text-green-ge' : 'text-gray-600 hover:text-green-ge'
              }`}
            >
              Profesionales
            </Link>
          </nav>

          <div className="hidden md:flex items-center gap-4">
            <div className="relative">
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                {profile?.avatar_url ? (
                  <img
                    src={profile.avatar_url}
                    alt={profile.full_name}
                    className="w-8 h-8 rounded-full object-cover"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-green-ge flex items-center justify-center text-white">
                    {profile?.full_name?.[0]?.toUpperCase() || 'U'}
                  </div>
                )}
                <span className="font-medium text-gray-900">{profile?.full_name}</span>
              </button>

              {userMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 animate-fade-in">
                  <Link
                    to="/profile"
                    className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-gray-700"
                    onClick={() => setUserMenuOpen(false)}
                  >
                    <User className="w-4 h-4" />
                    Mi Perfil
                  </Link>
                  <Link
                    to="/settings"
                    className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-gray-700"
                    onClick={() => setUserMenuOpen(false)}
                  >
                    <Settings className="w-4 h-4" />
                    Configuración
                  </Link>
                  <hr className="my-2" />
                  <button
                    onClick={() => {
                      signOut()
                      setUserMenuOpen(false)
                    }}
                    className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-red-600 w-full"
                  >
                    <LogOut className="w-4 h-4" />
                    Cerrar Sesión
                  </button>
                </div>
              )}
            </div>
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200 animate-slide-in">
          <nav className="px-4 py-4 space-y-2">
            <Link
              to="/"
              className={`block px-4 py-2 rounded-lg font-medium ${
                isActive('/') ? 'bg-green-light text-green-dark' : 'text-gray-600 hover:bg-gray-50'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Inicio
            </Link>
            <Link
              to="/services"
              className={`block px-4 py-2 rounded-lg font-medium ${
                isActive('/services') ? 'bg-green-light text-green-dark' : 'text-gray-600 hover:bg-gray-50'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Servicios
            </Link>
            <Link
              to="/properties"
              className={`block px-4 py-2 rounded-lg font-medium ${
                isActive('/properties') ? 'bg-green-light text-green-dark' : 'text-gray-600 hover:bg-gray-50'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Propiedades
            </Link>
            <Link
              to="/professionals"
              className={`block px-4 py-2 rounded-lg font-medium ${
                isActive('/professionals') ? 'bg-green-light text-green-dark' : 'text-gray-600 hover:bg-gray-50'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Profesionales
            </Link>
            <hr className="my-2" />
            <Link
              to="/profile"
              className="block px-4 py-2 rounded-lg font-medium text-gray-600 hover:bg-gray-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              Mi Perfil
            </Link>
            <button
              onClick={() => {
                signOut()
                setMobileMenuOpen(false)
              }}
              className="block w-full text-left px-4 py-2 rounded-lg font-medium text-red-600 hover:bg-red-50"
            >
              Cerrar Sesión
            </button>
          </nav>
        </div>
      )}
    </header>
  )
}
