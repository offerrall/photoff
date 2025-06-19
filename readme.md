# PhotoFF

**PhotoFF** is a high-performance GPU image processing library written in Python and accelerated with CUDA.
Originally developed as part of a custom OBS-style rendering engine, it has evolved into a personal tool that I intend to use and maintain for the foreseeable future.

I'm sharing this project because it might be beneficial to others, and I highly value real-world feedback. Please note that this is not a commercial product but a project I am passionate about.

---

## ⚡ Key Features

- **CUDA Acceleration:** Experience real-time filters, blending, resizing, and more, all powered by your GPU.
- **Smart Memory Management:** Allocate memory once and reuse it efficiently with dynamic size adjustments.
- **Simple and Direct Python API:** Enjoy a user-friendly API similar to PIL, but supercharged for GPU processing.
- **Exceptional Performance:** [Benchmarks](https://offerrall.github.io/photoff/benchmarks/)
- **Comprehensive Documentation:** Benefit from clear explanations and practical examples.
- **Minimal Dependencies:** Requires only `pillow`, `cffi`.

---

## 🧠 Why PhotoFF Exists

My motivation for creating PhotoFF stemmed from a need for a solution beyond the capabilities of existing libraries like PIL for tasks such as:

- Real-time scene composition.
- Generating GPU-accelerated overlays with visual effects.
- Batch image processing (creating thumbnails, banners, and collages).
- Developing fluid visual interfaces with dynamic filters.
- Building automation tools for creators, streamers, VTubers, and dashboards.

---

## 📦 Installation

### Prerequisites

- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0+
- Python packages: `cffi`, `pillow`,

### Installation

For detailed setup and compilation instructions, please refer to the [Installation Guide](https://offerrall.github.io/photoff/installation/).

---

## 🧪 Quick Example

```python
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import CudaImage

# Load image to GPU memory
src_image = load_image("./assets/stock.jpg")

# Apply filters
apply_gaussian_blur(src_image, radius=5.0)
apply_corner_radius(src_image, size=200)

# Save result
save_image(src_image, "./assets/gaussian_blur_test.png")

# Free GPU memory
src_image.free()
```

---

## 🔁 Buffer Reuse in Action

```python
# Allocate a single large buffer
shared_buffer = CudaImage(5000, 5000)

# Reuse it for different sizes
shared_buffer.width, shared_buffer.height = 800, 600
resize(image1, 800, 600, resize_image_cache=shared_buffer)

shared_buffer.width, shared_buffer.height = 1280, 720
resize(image2, 1280, 720, resize_image_cache=shared_buffer)

# No reallocs, no fragmentation, max performance
```

## 📚 Documentation

Explore the full documentation at [https://offerrall.github.io/photoff/](https://offerrall.github.io/photoff/):

- [🔰 Basics](https://offerrall.github.io/photoff/basics/)
- [⚙️ Advanced Techniques](https://offerrall.github.io/photoff/advanced/)
- [🔬 API Reference](https://offerrall.github.io/photoff/api/)

## 🤝 Contributing

Contributions are welcome! While this is a personal project, I intend to continue its development and improvement. If you're interested in contributing, please feel free to jump in.

---

## 📃 License

MIT.
