import { useState } from 'react'
import { Upload, X, Image as ImageIcon, Check } from 'lucide-react'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../contexts/AuthContext'

export default function ServiceUploadForm() {
  const { user } = useAuth()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('')
  const [price, setPrice] = useState('')
  const [photos, setPhotos] = useState<File[]>([])
  const [photoPreviews, setPhotoPreviews] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  if (!user) {
    return (
      <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl shadow-xl p-12 max-w-4xl mx-auto text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-600 to-blue-600 rounded-full mb-6">
          <Upload className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-3xl font-bold text-gray-900 mb-3">
          Comparte tus Servicios
        </h3>
        <p className="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">
          Inicia sesión para publicar tus servicios y conectar con clientes en toda Guinea Ecuatorial
        </p>
        <div className="flex items-center justify-center gap-4">
          <button className="px-8 py-3 text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-full font-semibold transition-all shadow-lg hover:shadow-xl">
            Iniciar Sesión
          </button>
          <button className="px-8 py-3 text-gray-700 border-2 border-gray-300 hover:border-gray-400 rounded-full font-semibold transition-all">
            Crear Cuenta
          </button>
        </div>
      </div>
    )
  }

  const categories = [
    'Construcción',
    'Electricidad',
    'Plomería',
    'Limpieza',
    'Jardinería',
    'Transporte',
    'Reparaciones',
    'Tecnología',
    'Educación',
    'Salud',
    'Otros'
  ]

  const handlePhotoSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const remainingSlots = 4 - photos.length
    const filesToAdd = files.slice(0, remainingSlots)

    if (files.length > remainingSlots) {
      setError(`Solo puedes subir ${remainingSlots} foto(s) más`)
      setTimeout(() => setError(''), 3000)
    }

    setPhotos([...photos, ...filesToAdd])

    filesToAdd.forEach(file => {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPhotoPreviews(prev => [...prev, reader.result as string])
      }
      reader.readAsDataURL(file)
    })
  }

  const removePhoto = (index: number) => {
    setPhotos(photos.filter((_, i) => i !== index))
    setPhotoPreviews(photoPreviews.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!user) {
      setError('Debes iniciar sesión para publicar un servicio')
      return
    }

    if (photos.length === 0) {
      setError('Debes subir al menos una foto')
      return
    }

    setLoading(true)
    setError('')

    try {
      const imageUrls: string[] = []

      for (const photo of photos) {
        const fileExt = photo.name.split('.').pop()
        const fileName = `${Math.random()}.${fileExt}`
        const filePath = `service-images/${fileName}`

        const { error: uploadError } = await supabase.storage
          .from('public')
          .upload(filePath, photo)

        if (uploadError) throw uploadError

        const { data: { publicUrl } } = supabase.storage
          .from('public')
          .getPublicUrl(filePath)

        imageUrls.push(publicUrl)
      }

      const { error: insertError } = await supabase
        .from('services')
        .insert({
          user_id: user.id,
          title,
          description,
          category,
          price: parseFloat(price),
          images: imageUrls,
          active: true
        })

      if (insertError) throw insertError

      setSuccess(true)
      setTitle('')
      setDescription('')
      setCategory('')
      setPrice('')
      setPhotos([])
      setPhotoPreviews([])

      setTimeout(() => setSuccess(false), 5000)
    } catch (err: any) {
      setError(err.message || 'Error al publicar el servicio')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h3 className="text-3xl font-bold text-gray-900 mb-2">
          Publica tu Servicio
        </h3>
        <p className="text-gray-600">
          Comparte tus servicios con la comunidad de abitaX
        </p>
      </div>

      {success && (
        <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <Check className="w-5 h-5" />
          <span className="font-medium">¡Servicio publicado exitosamente!</span>
        </div>
      )}

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Título del Servicio *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
              placeholder="Ej: Instalación eléctrica profesional"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Categoría *
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
              required
            >
              <option value="">Seleccionar categoría</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Descripción *
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
            rows={4}
            placeholder="Describe tu servicio, experiencia y lo que ofreces..."
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Precio (XAF) *
          </label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
            placeholder="10000"
            min="0"
            step="100"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Fotos del Servicio * (Máximo 4)
          </label>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            {photoPreviews.map((preview, index) => (
              <div key={index} className="relative group">
                <img
                  src={preview}
                  alt={`Preview ${index + 1}`}
                  className="w-full h-32 object-cover rounded-lg"
                />
                <button
                  type="button"
                  onClick={() => removePhoto(index)}
                  className="absolute top-2 right-2 w-8 h-8 bg-red-600 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}

            {photos.length < 4 && (
              <label className="w-full h-32 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-green-600 hover:bg-green-50 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handlePhotoSelect}
                  className="hidden"
                  multiple
                />
                <Upload className="w-8 h-8 text-gray-400 mb-2" />
                <span className="text-sm text-gray-500 font-medium">
                  Subir foto
                </span>
              </label>
            )}
          </div>

          <p className="text-xs text-gray-500 flex items-center gap-1">
            <ImageIcon className="w-4 h-4" />
            {photos.length}/4 fotos subidas
          </p>
        </div>

        <button
          type="submit"
          disabled={loading || photos.length === 0}
          className="w-full px-6 py-4 text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
        >
          {loading ? 'Publicando...' : 'Publicar Servicio'}
        </button>
      </form>
    </div>
  )
}
