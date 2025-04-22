# PhotoFF

![PhotoFF Logo](https://raw.githubusercontent.com/offerrall/photoff/refs/heads/main/assets/logo_lib.png)

**PhotoFF** is a high-performance GPU image processing library written in Python and accelerated with CUDA.
Originally developed as part of a custom OBS-style rendering engine, it has evolved into a personal tool that I intend to use and maintain for the foreseeable future.

I'm sharing this project because it might be beneficial to others, and I highly value real-world feedback. Please note that this is not a commercial product but a project I am passionate about.

---

## ⚡ Key Features

- **CUDA Acceleration:** Experience real-time filters, blending, resizing, and more, all powered by your GPU.
- **Smart Memory Management:** Allocate memory once and reuse it efficiently with dynamic size adjustments.
- **Simple and Direct Python API:** Enjoy a user-friendly API similar to PIL, but supercharged for GPU processing.
- **Exceptional Performance:** Achieve speeds of up to **30,000 FPS in fill operations** on an RTX 3070.
- **Comprehensive Documentation:** Benefit from clear explanations and practical examples.
- **Minimal Dependencies:** Requires only `pillow`, `cffi`, and `numpy` (solely for data transfer).

---

## 🧠 Why PhotoFF Exists

My motivation for creating PhotoFF stemmed from a need for a solution beyond the capabilities of existing libraries like PIL for tasks such as:

- Real-time scene composition (powering my custom OBS engine).
- Generating GPU-accelerated overlays with visual effects.
- Batch image processing (creating thumbnails, banners, and collages).
- Developing fluid visual interfaces with dynamic filters.
- Building automation tools for creators, streamers, VTubers, and dashboards.

---

## 📦 Installation

### Prerequisites

- Python 3.9+
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0+
- Visual Studio with C++ support (Windows)
- Python packages: `cffi`, `pillow`, `numpy`

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

---

## 🚀 Performance Benchmarks

The following performance tests were conducted on an RTX 3070:

- **Fill Color:** Achieved over **30,000 FPS** in `fill_color()` operations.
- **Consistent Frame Times:** Demonstrated stable performance without frame rate spikes, crucial for real-time applications.
- **Optimized for Various Workloads:** Designed to excel in both real-time rendering and batch processing tasks.

**Performance Comparison with Pillow:**

```
------------------------------------------------------------
Performance comparison between PhotoFF and Pillow:
------------------------------------------------------------
PhotoFF Resize (3840x2160) without cache: 0.002497 seconds (average of 20 iterations)
PhotoFF Resize (3840x2160) with cache: 0.000854 seconds (average of 20 iterations)
Pillow Resize (3840x2160): 0.007858 seconds (average of 20 iterations)
------------------------------------------------------------
PhotoFF Gaussian Blur (radius=5) without cache: 0.054405 seconds (average of 20 iterations)
PhotoFF Gaussian Blur (radius=5) with cache: 0.065551 seconds (average of 20 iterations)
Pillow Gaussian Blur (radius=5): 0.224554 seconds (average of 20 iterations)
------------------------------------------------------------
PhotoFF Grayscale: 0.000193 seconds (average of 20 iterations)
Pillow Grayscale: 0.008707 seconds (average of 20 iterations)
------------------------------------------------------------
Performance Comparison Summary:
------------------------------------------------------------
Resize (without cache): PhotoFF was 3.15 times faster than Pillow.
Resize (with cache): PhotoFF was 9.20 times faster than Pillow.
Gaussian Blur (without cache): PhotoFF was 4.13 times faster than Pillow.
Grayscale: PhotoFF was 45.12 times faster than Pillow.
------------------------------------------------------------
```

These benchmarks highlight the significant performance advantages of PhotoFF.

---

## 📚 Documentation

Explore the full documentation at [https://offerrall.github.io/photoff/](https://offerrall.github.io/photoff/):

- [🔰 Basics](https://offerrall.github.io/photoff/basics/)
- [⚙️ Advanced Techniques](https://offerrall.github.io/photoff/advanced/)
- [🔬 API Reference](https://offerrall.github.io/photoff/api/)

---

## ⚠️ About Alpha Blending and Color Spaces

PhotoFF employs a straightforward weighted alpha blend model. It's important to note that it does **not** perform gamma correction or operate in a linear color space. Therefore, it may not be suitable for cinematic or HDR production. However, for UI elements, overlays, thumbnails, and dynamic visual effects, its capabilities are more than sufficient.

---

## 🤝 Contributing

Contributions are welcome! While this is a personal project, I intend to continue its development and improvement. If you're interested in contributing, please feel free to jump in.

---

## 📃 License

MIT.