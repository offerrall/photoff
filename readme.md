# PhotOFF

A GPU-accelerated image processing library I built to learn CUDA and create a tool I wanted for my projects.

## Why?

I wanted to understand how GPU acceleration works and improve my image processing knowledge. Instead of using existing libraries, I decided to build my own as a learning experience. This project helped me:

- Learn CUDA programming and GPU architecture
- Understand image processing algorithms
- Create a tool that fits my specific needs

## Features

- Fast image operations using CUDA
- Basic operations:
  - Fill color
  - Opacity adjustment
  - Corner radius
  - Stroke effects (inner/outer)
- Image transformations:
  - Resize (Nearest neighbor, Bilinear, Bicubic)
  - Alpha blending
- Python interface with simple API
- Easy to extend with new operations

## Example Usage

```python
from photoff import CudaImage, RGBA
from photoff.operations.filters import apply_stroke
from photoff.io import load_image, save_image

# Load image
image = load_image("input.png")

# Add a green stroke
dst_image = CudaImage(image.width, image.height)
apply_stroke(image,
             dst_image, 
             stroke_width=5, 
             stroke_color=RGBA(0, 255, 0, 255))

# Save result
save_image(dst_image, "output.png")
```

## Performance

The library is optimized for GPU execution:
- Operations run directly on GPU memory
- Minimized memory transfers between CPU and GPU
- Efficient CUDA kernels for each operation
- Support for buffer reuse to avoid unnecessary allocations

## Project Structure

```
photoff/
├── cuda_src/        # CUDA implementation
├── photoff/         # Python package
│   ├── core/        # Core functionality
│   ├── operations/  # Image operations
│   └── io/          # Image loading/saving
└── test/            # Performance tests
```

## Learning Outcomes

Building this project taught me about:
- CUDA programming model and memory management
- Image processing algorithms and optimization
- Python-C interop using CFFI
- Project organization and API design

## Future Ideas

Some things I'd like to add:
- More image filters and effects
- Batch processing capabilities
- Additional optimization techniques
- Better error handling and debugging tools

## Dependencies

### Core
- CUDA Toolkit
- Python 3.7+
- CFFI

### Image Loading/Saving (Optional)
- Pillow
- NumPy

## Building (Only windows for now, linux coming soon)

```bash
# Compile CUDA code (nvcc in PATH required)
python cuda_src/compile.py

# Import and use in Python
from photoff import CudaImage
```

## License

This is a personal learning project. Feel free to use it and learn from it!