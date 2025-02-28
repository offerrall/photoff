# PhotoFF - High-Performance Image Processing Library with CUDA

PhotoFF is a high-performance image processing library that uses CUDA to achieve exceptional processing speeds. Designed to maximize performance through efficient GPU memory management.

## Basic Example

```python
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import CudaImage

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

![Gaussian Blur Test](/assets/gaussian_blur_test.png)

## Key Features

!!! warning "Development Status"
    **This only the beginning!** More features are coming soon.

- **Image blending**: Combine multiple images with different blending modes.
- **Fill operations**: Fill an image with a solid color or a gradient.
- **Filter effects**: Apply various effects like rounded corners, opacity adjustment, flipping, grayscale conversion, stroke, shadow, and Gaussian blur.
- **Resizing**: Resize images using bilinear, nearest, or bicubic interpolation.
- **Cropping**: Remove margins from images.
- **Text rendering**: Render text onto images.
- **Utility functions**: Calculate padding and compose images to cover containers.
- **I/O operations**: Load images from files, save images, and convert CUDA images to PIL images.

