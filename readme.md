## PhotoFF

A personal project to create a high-performance image processing library using CUDA.

```python
from photoff.operations.filters import apply_shadow
from photoff.io import load_image, save_image
from photoff import RGBA

# Load image
image = load_image("./assets/shadow_test.png")

# Apply shadow effect
apply_shadow(image, radius=5, intensity=0.5, shadow_color=RGBA(0, 0, 0, 255))

# Save image
save_image(image, "./assets/shadow_test.png")

# Free GPU memory
image.free()
```

## Features

- **Image blending**: Combine multiple images with different blending modes.
- **Fill operations**: Fill an image with a solid color or a gradient.
- **Filter effects**: Apply various effects like rounded corners, opacity adjustment, flipping, grayscale conversion, stroke, shadow, and Gaussian blur.
- **Resizing**: Resize images using bilinear, nearest, or bicubic interpolation.
- **Cropping**: Remove margins from images.
- **Text rendering**: Render text onto images.
- **Utility functions**: Calculate padding and compose images to cover containers.
- **I/O operations**: Load images from files, save images, and convert CUDA images to PIL images.


## Memory Management & Performance
PhotoFF has been designed with a focus on maximum performance through efficient GPU memory management. The library achieves exceptional processing speeds (up to 30,000 FPS for fill operations at 1920p on an RTX 3070) by implementing several key optimization strategies:

Buffer Reuse & Memory Control
Unlike many image processing libraries that allocate and free memory for each operation, PhotoFF gives you complete control over buffer allocation and reuse. Key benefits include:

Explicit Buffer Management: Create buffers once and reuse them across multiple operations to eliminate allocation overhead.
Processing Pipelines: Chain multiple effects with zero intermediate allocations.
Size Flexibility: Buffers can be larger than strictly needed for a given operation, allowing pre-allocation of maximum-size buffers that can be reused for smaller operations.

```python
from photoff.core.types import CudaImage, RGBA
from photoff.operations.utils import cover_image_in_container, get_cover_resize_dimensions
from photoff.operations.fill import fill_color
from photoff.io import load_image, image_to_pil

# Pre-allocated caches for container and resizing
cover_cache = CudaImage(5000, 5000)
cover_resize_cache = CudaImage(5000, 5000)

# Load the reference image
placeholder = load_image("./stock.jpg")

# Target dimensions for the "cover" image
target_width = 800
target_height = 600

# Adjust the dimensions of the caches
cover_cache.width = target_width
cover_cache.height = target_height
resize_dims = get_cover_resize_dimensions(placeholder, target_width, target_height)
cover_resize_cache.width, cover_resize_cache.height = resize_dims

# Create the "cover" image by reusing the pre-allocated buffers
cover_image_in_container(
    placeholder,
    target_width,
    target_height,
    0, 0,
    RGBA(255, 255, 255, 255),
    container_image_cache=cover_cache,
    resize_image_cache=cover_resize_cache
)

# Convert the result to a PIL image and save it
pil_image = image_to_pil(cover_cache)
pil_image.save("optimized_cover.jpg")

# Free the GPU buffers
cover_cache.free()
cover_resize_cache.free()

```

# PhotoFF Installation & Usage

## Requirements
- NVIDIA GPU with CUDA support
- CUDA Toolkit (ensure `nvcc` is in PATH)
- Python 3.9+
- Visual Studio (Windows) for compiling the DLL
- NumPy, Pillow, CFFI

## Installation
1. **Clone Repository**
   ```bash
   git clone <repository_url>
   cd photoff
   ```
2. **Install Python Dependencies**
   ```bash
   pip install .
   ```
3. **Compile CUDA Library**
   ```bash
   python photoff_cuda_src/compile.py
   ```


## Visual Tests

Visual tests are provided in the `visual_test/` directory. These scripts demonstrate examples of all PhotoFF functions (blending, filling, filtering, resizing, cropping, text rendering, etc.) in an interactive way.

If you have [FuncToGUI](https://github.com/offerrall/FuncToGUI) installed, you can run these scripts (e.g., `python visual_test/flip.py`) to open a GUI and experiment with different parameters.

## Future Plans

I'm still learning and plan to gradually add more features over time. If you like the idea or if there are collaborators interested, I will take the project more seriously and continue its development.
