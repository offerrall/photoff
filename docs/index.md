# PhotoFF - High-Performance Image Processing Library with CUDA

!!! warning "Development Status"
    **This library is currently under active development.** The API may change significantly between versions. Use at your own risk in production environments.

PhotoFF is a high-performance image processing library that uses CUDA to achieve exceptional processing speeds. Designed to maximize performance through efficient GPU memory management.

## Key Features

- **Image blending**: Combine multiple images with different blending modes.
- **Fill operations**: Fill an image with a solid color or a gradient.
- **Filter effects**: Apply various effects like rounded corners, opacity adjustment, flipping, grayscale conversion, stroke, shadow, and Gaussian blur.
- **Resizing**: Resize images using bilinear, nearest, or bicubic interpolation.
- **Cropping**: Remove margins from images.
- **Text rendering**: Render text onto images.
- **Utility functions**: Calculate padding and compose images to cover containers.
- **I/O operations**: Load images from files, save images, and convert CUDA images to PIL images.

## Basic Example

```python
from photoff.operations.filters import apply_shadow
from photoff.io import load_image, save_image
from photoff import RGBA

# Load image
image = load_image("./assets/image.png")

# Apply shadow effect
apply_shadow(image, radius=5, intensity=0.5, shadow_color=RGBA(0, 0, 0, 255), inner=True)

# Save image
save_image(image, "./assets/image_with_shadow.png")

# Free GPU memory
image.free()
```

## Memory Management & Performance

PhotoFF has been designed with a focus on maximum performance through efficient GPU memory management. The library achieves exceptional processing speeds (up to 30,000 FPS for fill operations at 1920p on an RTX 3070) by implementing several key optimization strategies:

### Buffer Reuse & Memory Control

Unlike many image processing libraries that allocate and free memory for each operation, PhotoFF gives you complete control over buffer allocation and reuse. Key benefits include:

- **Explicit Buffer Management**: Create buffers once and reuse them across multiple operations to eliminate allocation overhead.
- **Processing Pipelines**: Chain multiple effects with zero intermediate allocations.
- **Size Flexibility**: Buffers can be larger than strictly needed for a given operation, allowing pre-allocation of maximum-size buffers that can be reused for smaller operations.

## Requirements

- NVIDIA GPU with CUDA support
- CUDA Toolkit (ensure `nvcc` is in PATH)
- Python 3.9+
- Visual Studio (Windows) for compiling the DLL
- Python dependencies: NumPy, Pillow, CFFI
    - Numpy is only for loading/saving images and is not required for core operations
    - Pillow is required for loading/saving images and text rendering
    - CFFI is required for interfacing with the CUDA DLL

## Quick Navigation

- [Installation Guide](user-guide/installation.md)
- [Getting Started](user-guide/getting-started.md)
- [API Reference](api/core/cuda-image.md)
- [Performance](advanced/performance.md)
