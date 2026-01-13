import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { LogIn, Mail, Lock } from 'lucide-react'

interface LoginProps {
  onSwitchToRegister: () => void
}

export default function Login({ onSwitchToRegister }: LoginProps) {
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
    }

    setLoading(false)
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
            <div className="inline-flex items-center gap-3 mb-3">
              <LogIn className="text-green-ge w-7 h-7" />
              <h2 className="text-3xl font-black text-gray-900">
                Iniciar Sesión
              </h2>
            </div>
            <p className="text-gray-600">Accede a tu cuenta abitaX</p>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-6 py-4 rounded-lg mb-6 flex items-start gap-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="font-semibold">Error de autenticación</p>
                <p className="text-sm">{error}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
                <Mail className="w-5 h-5 text-green-ge" />
                Correo Electrónico
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field text-lg"
                placeholder="tu@email.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
                <Lock className="w-5 h-5 text-green-ge" />
                Contraseña
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field text-lg"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed font-bold shadow-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                  Iniciando sesión...
                </span>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

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
        </div>
      </div>
    </div>
  )
}
