# PhotoFF

![PhotoFF Logo](https://raw.githubusercontent.com/offerrall/photoff/refs/heads/main/assets/logo_lib.png)

**PhotoFF** is a high-performance GPU image processing library written in Python and accelerated with CUDA.  
It was originally created as part of a custom OBS-style rendering engine and has grown into a personal tool I plan to use and maintain for years to come.

I’m sharing it because it might help others, and because I value real feedback. This isn’t a product—it’s a project I care about.

---

## ⚡ Key Features

- **CUDA acceleration** – Filters, blending, resizing and more, all in real time
- **Smart memory management** – Allocate once, reuse infinitely with logical size adjustments
- **Simple and direct Python API** – Like PIL, but on steroids
- **Proven performance** – Up to **30,000 FPS in fill operations** on an RTX 3070
- **Thorough documentation** – Clear explanations, real examples
- **Minimal dependencies** – Only `pillow`, `cffi` and `numpy` (for transfer only)

---

## 🧠 Why PhotoFF Exists

I didn’t want to reimplement PIL. I needed something I could use for:

- A real-time scene compositor (my own OBS engine)
- GPU-based overlay generation with visual effects
- Batch processing of images (thumbnails, banners, collages)
- Fluid visual interfaces with dynamic filters
- Automation tools for creators, streamers, VTubers, or dashboards

---

## 📦 Installation

### Prerequisites

- Python 3.9+
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0+
- Visual Studio with C++ support (Windows)
- Python packages: `cffi`, `pillow`, `numpy`

### Installation

Follow the [Installation Guide](https://offerrall.github.io/photoff/installation/) for setup and compilation instructions.

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

---

## 🚀 Performance

Tested on an RTX 3070:
- **30,000+ FPS** in `fill_color()` operations
- Constant frame times, no spikes
- Designed for real-time and batch processing workloads

---

## 📚 Documentation

Full documentation: [https://offerrall.github.io/photoff/](https://offerrall.github.io/photoff/)

- [🔰 Basics](https://offerrall.github.io/photoff/basics/)
- [⚙️ Advanced Techniques](https://offerrall.github.io/photoff/advanced/)
- [🔬 API Reference](https://offerrall.github.io/photoff/api/)

---

## ⚠️ About Alpha Blending and Color Spaces

PhotoFF uses a simple weighted alpha blend model.  
It does **not** apply gamma correction or use linear color space.  
It’s not for cinematic or HDR production. But for UI, overlays, thumbnails, or dynamic visuals, it’s more than enough.

---

## 🤝 Contributing

Yes, I accept contributions. This is a personal project, but I plan to keep using and improving it. If you want to help—jump in.

---

## 📃 License

MIT.

---
