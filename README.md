# abitaX - La SuperApp de Guinea Ecuatorial

La primera superapp basada en mapas de Guinea Ecuatorial, conectando personas, lugares y servicios en todo el país.

## Características

- **Autenticación Segura**: Sistema de registro e inicio de sesión con Supabase
- **Servicios**: Encuentra profesionales para cualquier servicio que necesites
- **Propiedades**: Explora casas, apartamentos y terrenos en venta o alquiler
- **Profesionales**: Conecta con expertos verificados en diversas áreas
- **Mapas Integrados**: Google Maps para visualizar ubicaciones
- **Diseño Responsivo**: Funciona perfectamente en móvil y escritorio
- **Colores Nacionales**: Diseño inspirado en la bandera de Guinea Ecuatorial

## Tecnologías

- **Frontend**: React 18 + TypeScript + Vite
- **Estilos**: Tailwind CSS
- **Base de Datos**: Supabase (PostgreSQL con PostGIS)
- **Autenticación**: Supabase Auth
- **Mapas**: Google Maps JavaScript API
- **Iconos**: Lucide React
- **Routing**: React Router v6

## Configuración

1. Instala las dependencias:
```bash
npm install
```

2. Configura las variables de entorno en `.env`:
```env
VITE_SUPABASE_URL=tu_url_de_supabase
VITE_SUPABASE_ANON_KEY=tu_clave_anon_de_supabase
VITE_GOOGLE_MAPS_API_KEY=tu_api_key_de_google_maps
```

3. Inicia el servidor de desarrollo:
```bash
npm run dev
```

4. Construye para producción:
```bash
npm run build
```

## Estructura de la Base de Datos

- **profiles**: Perfiles de usuario extendidos
- **professionals**: Perfiles de profesionales
- **services**: Servicios ofrecidos
- **properties**: Propiedades inmobiliarias
- **reviews**: Reseñas de profesionales
- **chats**: Conversaciones entre usuarios
- **messages**: Mensajes individuales
- **favorites**: Propiedades y servicios guardados

## Características de Diseño

- Colores basados en la bandera de Guinea Ecuatorial:
  - Verde (#007A33)
  - Azul (#0055A4)
  - Rojo (#CE1126)
  - Dorado (#FFD700)
- Animaciones suaves y transiciones
- Interfaz intuitiva y moderna
- Navegación inferior para móviles
- Búsqueda y filtrado avanzado
- Integración de mapas para ubicaciones

## Funcionalidades Principales

### Para Usuarios
- Buscar servicios y propiedades
- Ver profesionales verificados
- Contactar con prestadores de servicios
- Guardar favoritos
- Chat en tiempo real (próximamente)

### Para Profesionales
- Crear perfil profesional
- Publicar servicios
- Recibir reseñas y calificaciones
- Gestionar disponibilidad
- Ver estadísticas

### Para Propietarios
- Publicar propiedades
- Gestionar listados
- Recibir consultas
- Actualizar disponibilidad

## Seguridad

- Row Level Security (RLS) habilitado en todas las tablas
- Autenticación basada en JWT
- Políticas de acceso estrictas
- Validación de datos en cliente y servidor

## Licencia

© 2026 abitaX - Todos los derechos reservados
