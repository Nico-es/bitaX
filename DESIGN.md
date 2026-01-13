# abitaX - Guía de Diseño

## Colores de la Bandera de Guinea Ecuatorial

Tu diseño HTML ha sido completamente integrado en la aplicación React con los colores oficiales de Guinea Ecuatorial:

### Colores Principales
- **Verde (#007A33)**: Recursos naturales y riqueza del país
- **Blanco (#FFFFFF)**: Paz y unidad
- **Rojo (#CE1126)**: Lucha por la independencia
- **Azul (#0055A4)**: El mar que conecta el territorio
- **Dorado (#FFD700)**: Prosperidad y desarrollo

### Paleta Extendida
- `--verde-claro: #E8F5E9` - Fondos suaves
- `--verde-oscuro: #006028` - Textos destacados
- `--azul-claro: #E3F2FD` - Secciones alternativas
- `--rojo-claro: #FFEBEE` - Alertas suaves
- `--dorado-oscuro: #E6C300` - Acentos premium

## Tipografía

El sistema tipográfico usa tres familias principales:

- **Montserrat** (900): Logo y títulos principales
- **Poppins** (700-900): Encabezados y subtítulos
- **Inter** (300-700): Texto de cuerpo y UI

## Componentes del Diseño

### Logo abitaX
- Icono cuadrado con gradiente verde
- Texto con gradiente verde-azul
- Bandera de Guinea Ecuatorial (🇬🇶) integrada

### Botones
- **btn-primary**: Gradiente verde con hover elevado
- **btn-secondary**: Gradiente azul
- **btn-outline**: Borde verde que rellena al hover

### Cards
- Bordes redondeados (24px)
- Sombra suave que aumenta al hover
- Elevación con transform translateY

### Secciones
- **Hero**: Gradiente verde-azul con estadísticas
- **Servicios**: Fondo claro con cards destacadas
- **Propiedades**: Gradiente sutil con imágenes
- **Mapa**: Integración de Google Maps con filtros
- **Testimonios**: Fondo azul con patrón sutil
- **CTA**: Gradiente verde con animación rotatoria

## Sistema de Espaciado

Basado en múltiplos de 8px:
- Pequeño: 12px
- Mediano: 16px
- Grande: 24px
- Extra grande: 32px

## Animaciones

### Transiciones Principales
- **Rápida**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Lenta**: 0.5s cubic-bezier(0.4, 0, 0.2, 1)

### Animaciones Personalizadas
- **fadeInUp**: Entrada desde abajo con fade
- **slideIn**: Deslizamiento horizontal
- **spin**: Rotación continua (loading)

## Sombras

Tres niveles de profundidad:
- **Suave**: `0 4px 20px rgba(0, 0, 0, 0.08)`
- **Media**: `0 8px 30px rgba(0, 0, 0, 0.12)`
- **Fuerte**: `0 15px 40px rgba(0, 0, 0, 0.15)`

## Gradientes

Todos los gradientes siguen la dirección 135deg:
- **Verde**: `#007A33` → `#009B4D`
- **Azul**: `#0055A4` → `#0066CC`
- **Rojo**: `#CE1126` → `#E63946`
- **Dorado**: `#FFD700` → `#FFC107`
- **Hero**: Combinación verde-azul con transparencia

## Responsive Design

### Breakpoints
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px
- **Small Mobile**: < 480px

### Adaptaciones Móviles
- Navegación inferior fija
- Menú hamburguesa
- Cards en columna única
- Tipografía reducida
- Espaciado compacto

## Iconografía

Usando Lucide React con tamaños consistentes:
- Pequeño: 16px
- Mediano: 20px
- Grande: 24px
- Extra grande: 32px

## Integración con Supabase

### Autenticación
- Login/Register con diseño de modales
- Perfil de usuario con avatar circular
- Menú desplegable con opciones

### Datos Dinámicos
- Servicios desde BD con filtros
- Propiedades con geolocalización
- Profesionales con calificaciones
- Chat en tiempo real (próximamente)

## Google Maps Integration

### Características del Mapa
- Centrado en Guinea Ecuatorial (1.6139, 10.4670)
- Marcadores con colores por categoría:
  - Verde: Construcción
  - Azul: Mantenimiento
  - Rojo: Inmobiliaria
  - Dorado: Otros servicios

### Panel de Resultados
- Sidebar con lista scrolleable
- Sincronización con marcadores
- Filtros por categoría y ciudad
- Geolocalización del usuario

## Accesibilidad

- Contraste mínimo WCAG AA
- Navegación por teclado
- Estados focus visibles
- Textos alternativos en imágenes
- ARIA labels en componentes interactivos

## Performance

### Optimizaciones Aplicadas
- Lazy loading de imágenes
- Code splitting por rutas
- CSS minificado
- Compresión gzip
- Cache de assets estáticos

### Métricas Objetivo
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Cumulative Layout Shift: < 0.1

## Próximas Características

1. **Sistema de Chat en Tiempo Real**
   - Supabase Realtime
   - Notificaciones push
   - Estado online/offline

2. **Portafolio Profesional**
   - Galería de trabajos
   - Testimonios de clientes
   - Calendario de disponibilidad

3. **Sistema de Pagos**
   - Integración con pasarelas locales
   - Pagos seguros
   - Historial de transacciones

4. **App Móvil Nativa**
   - React Native
   - Notificaciones push
   - Geolocalización avanzada

## Notas de Desarrollo

### Variables CSS Globales
Todas las variables están en `:root` en `src/index.css`

### Componentes Reutilizables
- Header con navegación responsiva
- Footer con enlaces organizados
- Cards para servicios y propiedades
- Modales para auth y detalles
- Botones con estados hover

### Estructura de Archivos
```
src/
├── components/
│   ├── Auth/          # Login y Register
│   ├── Layout/        # Header, Footer, BottomNav
│   └── Map/           # GoogleMap integration
├── pages/             # Páginas principales
├── contexts/          # AuthContext con Supabase
├── lib/              # supabase client
└── index.css         # Estilos globales y variables
```

## Soporte

Para preguntas sobre el diseño:
- Email: design@abitax.ge
- Documentación: https://abitax.ge/docs
- Figma: [Enlace a diseños]

---

**Inspirado en los colores y valores de Guinea Ecuatorial 🇬🇶**

© 2026 abitaX - La SuperApp de Guinea Ecuatorial
