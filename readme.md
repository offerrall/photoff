## PhotoFF

A CUDA-accelerated image composition and manipulation library.

## Project

PhotoFF was built to simplify image composition tasks using GPU acceleration. By leveraging CUDA, the library provides significantly better performance compared to CPU-based alternatives like Pillow or OpenCV for many common image operations.
The core approach focuses on giving developers direct control over memory management, allowing for efficient reuse of GPU buffers during complex processing pipelines.

```python

from photoff.operations.filters import apply_shadow
from photoff.io import save_image, load_image
from photoff import RGBA

path = "./assets/shadow_test.png"
src_image = load_image(path)

apply_shadow(src_image,
             radius = 5,
             intensity = 0.5,
             shadow_color = RGBA(0, 0, 0, 255))

save_image(src_image, path)

src_image.free()

```

## Features
High-performance image processing accelerated by CUDA.
Fine-grained control over GPU memory management for building complex processing pipelines.
Seamless integration with PIL/Numpy for input/output operations.

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