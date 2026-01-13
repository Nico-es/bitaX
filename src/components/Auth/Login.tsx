import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { Mail, Lock } from 'lucide-react'

interface LoginProps {
  onSwitchToRegister?: () => void
  onSuccess?: () => void
  inModal?: boolean
}

export default function Login({ onSwitchToRegister, onSuccess, inModal = false }: LoginProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { signIn } = useAuth()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    const { error } = await signIn(email, password)

    if (error) {
      setError(error.message)
      setLoading(false)
    } else {
      setLoading(false)
      onSuccess?.()
    }
  }

  const formContent = (
    <>
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <Mail className="w-4 h-4" />
            Correo Electrónico
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
            placeholder="tu@email.com"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <Lock className="w-4 h-4" />
            Contraseña
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
            placeholder="••••••••"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-3 text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </button>
      </form>
    </>
  )

  if (inModal) {
    return formContent
  }

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="text-center mb-10 animate-fade-in">
          <div className="flex justify-center mb-6">
            <div className="w-28 h-28 bg-white rounded-3xl flex items-center justify-center shadow-2xl">
              <span className="text-6xl">🇬🇶</span>
            </div>
          </div>
          <h1 className="text-5xl font-black text-white mb-3 drop-shadow-lg">abitaX</h1>
          <div className="flex items-center justify-center gap-3 mb-2">
            <div className="h-1 w-12 bg-white/50 rounded"></div>
            <p className="text-white/90 text-xl font-bold">Guinea Ecuatorial</p>
            <div className="h-1 w-12 bg-white/50 rounded"></div>
          </div>
          <p className="text-white/80 text-lg">La SuperApp basada en mapas</p>
        </div>

        <div className="feature-card p-10 animate-fade-in glass-effect" style={{ animationDelay: '0.1s' }}>
          <div className="text-center mb-8">
            <h2 className="text-3xl font-black text-gray-900 mb-2">
              Iniciar Sesión
            </h2>
            <p className="text-gray-600">Accede a tu cuenta abitaX</p>
          </div>
          {formContent}

          {onSwitchToRegister && (
            <div className="mt-8 text-center">
              <p className="text-gray-600 text-lg">
                ¿No tienes cuenta?{' '}
                <button
                  onClick={onSwitchToRegister}
                  className="text-green-ge hover:text-green-dark font-bold underline"
                >
                  Regístrate aquí
                </button>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
