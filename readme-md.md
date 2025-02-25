# Photoff

Photoff es una biblioteca de procesamiento de imágenes acelerada por GPU utilizando CUDA. Este proyecto nace de mi interés por aprender CUDA y aplicarlo a operaciones eficientes sobre imágenes.

## Filosofía del Proyecto

- **Control Explícito de Memoria**: Todas las operaciones de memoria (creación/destrucción de buffers) son explícitas y controladas por el usuario, nunca ocurren implícitamente dentro de otras funciones.
- **Rendimiento Predecible**: Al exponer las operaciones a bajo nivel, los usuarios pueden construir pipelines de procesamiento optimizados con un comportamiento determinista.
- **Reutilización de Recursos**: El diseño permite la reutilización eficiente de buffers para evitar asignaciones/liberaciones constantes de memoria.
- **API Minimalista**: Cada función hace una sola cosa bien, las operaciones complejas se construyen componiendo operaciones más simples.

## Características

- Operaciones básicas de procesamiento de imágenes (recorte, redimensionamiento, mezcla)
- Filtros visuales (desenfoque gaussiano, sombras, trazos, opacidad)
- Efectos de relleno (color sólido, gradientes)
- Transformaciones geométricas (volteo, esquinas redondeadas)
- Interfaz Python fácil de usar sobre el núcleo CUDA

## Estado del Proyecto

Este proyecto está actualmente en desarrollo activo. Lo estoy utilizando como una forma de aprender CUDA y procesamiento de imágenes, a la vez que construyo una herramienta que planeo usar profesionalmente.

La API y la estructura del proyecto pueden cambiar considerablemente mientras aprendo y mejoro el diseño.

## Requisitos

- CUDA Toolkit
- Python 3.9+
- CFFI
- PIL (Pillow)
- NumPy

PIL y NumPy son necesarios para la carga y guardado de imágenes. CFFI se utiliza para la integración con CUDA.

## Ejemplos Básicos

```python
from photoff.core.types import CudaImage, RGBA
from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_corner_radius, apply_gaussian_blur
from photoff.io import save_image

# Crear una imagen
image = CudaImage(800, 600)

# Rellenar con color
fill_color(image, RGBA(255, 100, 100, 255))  # Rojo claro

# Aplicar esquinas redondeadas
apply_corner_radius(image, 30)

# Aplicar desenfoque gaussiano
apply_gaussian_blur(image, radius=5.0)

# Guardar resultado
save_image(image, "output.png")
```

## Estructura del Proyecto

- **photoff/core/**: Definiciones básicas y enlace CUDA
- **photoff/operations/**: Operaciones de alto nivel (filtros, transformaciones)
- **photoff/io/**: Carga y guardado de imágenes
- **photoff_cuda_src/**: Código fuente CUDA con implementaciones de kernel

## Solicitud de Feedback

Este proyecto está siendo compartido para recibir feedback sobre:

- Diseño de la API y patrones de uso
- Implementaciones en CUDA y optimizaciones
- Posibles características adicionales
- Mejores prácticas para el manejo de memoria en CUDA

Si tienes experiencia en CUDA o procesamiento de imágenes, cualquier comentario o sugerencia es bienvenido.

## Licencia

Este proyecto es de uso personal y profesional. Todos los derechos reservados.
