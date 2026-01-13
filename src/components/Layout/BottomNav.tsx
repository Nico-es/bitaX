import { Link, useLocation } from 'react-router-dom'
import { Home, Briefcase, Building2, Users, User } from 'lucide-react'

export default function BottomNav() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
      <div className="flex justify-around items-center h-16">
        <Link
          to="/"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
            isActive('/') ? 'text-green-ge' : 'text-gray-500'
          }`}
        >
          <Home className="w-6 h-6 mb-1" />
          <span className="text-xs font-medium">Inicio</span>
        </Link>

        <Link
          to="/services"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
            isActive('/services') ? 'text-green-ge' : 'text-gray-500'
          }`}
        >
          <Briefcase className="w-6 h-6 mb-1" />
          <span className="text-xs font-medium">Servicios</span>
        </Link>

        <Link
          to="/properties"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
            isActive('/properties') ? 'text-green-ge' : 'text-gray-500'
          }`}
        >
          <Building2 className="w-6 h-6 mb-1" />
          <span className="text-xs font-medium">Propiedades</span>
        </Link>

        <Link
          to="/professionals"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
            isActive('/professionals') ? 'text-green-ge' : 'text-gray-500'
          }`}
        >
          <Users className="w-6 h-6 mb-1" />
          <span className="text-xs font-medium">Profesionales</span>
        </Link>

        <Link
          to="/profile"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
            isActive('/profile') ? 'text-green-ge' : 'text-gray-500'
          }`}
        >
          <User className="w-6 h-6 mb-1" />
          <span className="text-xs font-medium">Perfil</span>
        </Link>
      </div>
    </nav>
  )
}
