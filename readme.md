# PhotoFF

![PhotoFF Logo](https://raw.githubusercontent.com/offerrall/photoff/refs/heads/main/assets/logo_lib.png)

A high-performance image processing library that uses CUDA to achieve exceptional processing speeds. PhotoFF is designed with a unique approach to GPU memory management that virtually eliminates allocation overhead during processing pipelines.

## Features

- **Lightning-fast processing**: Leverages GPU parallelism for image operations
- **Advanced memory management**: Pre-allocate buffers once and adjust their logical dimensions on-the-fly
- **Comprehensive operations**: Includes filters, transformations, blending, and more
- **Clean Python API**: Intuitive interface designed for both beginners and advanced users
- **Minimal dependencies**: Only uses CFFI and Pillow. NumPy is used for low-level data conversion, not for core processing.

## Installation

### Prerequisites

- Python 3.9 or newer
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0 or newer
- Visual Studio with C++ support (Windows)
- CFFI, Pillow, and NumPy

### Install

For detailed installation instructions, see our [Installation Guide](https://offerrall.github.io/photoff/installation/).

## Basic Example

```python
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import CudaImage

# Load the image in GPU memory
src_image: CudaImage = load_image("./assets/stock.jpg")

# Apply filters
apply_gaussian_blur(src_image, radius=5.0)
apply_corner_radius(src_image, size=200)

# Save the result
save_image(src_image, "./assets/gaussian_blur_test.png")

# Free the image from GPU memory
src_image.free()
```

## Advanced Memory Management

PhotoFF's unique approach to memory management allows for exceptional performance:

```python
# Allocate a large buffer once
buffer = CudaImage(5000, 5000)

# Process multiple images by adjusting logical dimensions
buffer.width, buffer.height = 800, 600
process_image_1(buffer)

buffer.width, buffer.height = 1200, 900
process_image_2(buffer)

# No memory allocations or deallocations needed!
```

## Documentation

Full documentation is available at [https://offerrall.github.io/photoff/](https://offerrall.github.io/photoff/)

- [Basic Operations](https://offerrall.github.io/photoff/basics/)
- [Advanced Techniques](https://offerrall.github.io/photoff/advanced/)
- [API Reference](https://offerrall.github.io/photoff/api/)


## License

PhotoFF is released under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
