# PhotoFF - High-Performance Image Processing Library with CUDA

![Gaussian Blur Test](https://raw.githubusercontent.com/offerrall/photoff/refs/heads/main/assets/logo_lib.png)

PhotoFF is a high-performance image processing library that uses CUDA to achieve exceptional processing speeds. Designed to maximize performance through efficient GPU memory management.

## Basic Example

```python
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import Image

# Load the image
src_image = load_image("./assets/stock.jpg")

# Apply filters
apply_gaussian_blur(src_image, radius=5.0)
apply_corner_radius(src_image, size=200)

# Save the result
save_image(src_image, "./assets/gaussian_blur_test.png")

# Free resources
src_image.free()
```

![Gaussian Blur Test](https://raw.githubusercontent.com/offerrall/photoff/refs/heads/main/assets/gaussian_blur_test.png)

## Key Features

- **CUDA-Accelerated Processing**: Harness the power of your GPU for blazing-fast image operations
- **Memory-Efficient Design**: Optimized buffer management minimizes memory overhead
- **Robust Image Manipulation**: Comprehensive suite of operations including filters, transforms, and compositing
- **Pythonic Interface**: Clean, intuitive API designed for both beginners and advanced users
- **Seamless Integration**: Works with common image formats through PIL interoperability