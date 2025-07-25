# PhotoFF Documentation

PhotoFF is a high-performance image processing library that uses CUDA to achieve exceptional processing speeds. Designed to maximize performance through efficient GPU memory management.

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

## Key Features

- **Pythonic Interface**: Clean, intuitive API designed for both beginners and advanced users
- **Robust Image Manipulation**: Comprehensive suite of operations including filters, transforms, and compositing
- **Seamless Integration**: Works with common image formats through PIL interoperability
- **CUDA-Accelerated Processing**: Harness the power of your GPU for blazing-fast image operations
- **Memory-Efficient Design**: Optional advanced memory management for optimized buffer management

## Next Steps

Now that you understand the basics, you can:

- Explore the [Basic Operations](basics.md) to learn about loading, saving, and manipulating images
- Dive into the [Advanced Operations](advanced.md) to discover more complex image processing techniques
- Check out the [API Reference](api.md) for detailed documentation on all available functions and classes
- Read the [Benchmarks](benchmarks.md) to see how PhotoFF compares to other libraries in terms of performance