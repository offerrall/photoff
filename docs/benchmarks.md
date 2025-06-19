# PhotoFF Performance Benchmarks

## Overview

PhotoFF is built to fully exploit the parallelism of modern NVIDIA GPUs through CUDA. This page presents an apples‑to‑apples comparison between **PhotoFF** and the ubiquitous **Pillow** CPU implementation for common image‑processing tasks. Each benchmark shows the number of frames processed per second (*FPS*) and the resulting speed‑up factor obtained with PhotoFF.

## Test Environment

| Component | Specification                    |
| --------- | -------------------------------- |
| CPU       | AMD Ryzen™ 3 3700X               |
| GPU       | NVIDIA® GeForce RTX™ 3070 (8 GB) |
| OS        | Windows 10 Pro 22H2              |
| Python    | 3.13                             |
| CUDA      | 12.6                             |
| Driver    | 560.94                           |

## Methodology

Each test runs the corresponding script inside `` and executes **100 consecutive iterations** of the target operation. For PhotoFF we measure:

- **GPU (no cache)** – the naive call that internally allocates a *new* destination buffer every iteration.
- **GPU (cache)** – the same call but re‑using a pre‑allocated destination buffer to avoid costly `cudaMalloc` operations (when the API supports it).

Pillow is executed on the host CPU using the nearest equivalent function.

The final metric is calculated as:

```text
FPS = 100 iterations / total time (seconds)
```

where the total time includes all Python overhead, memory transfers and device synchronisations.

## Results

### Blending (`blend`)

| Operation | PhotoFF GPU FPS | Pillow CPU FPS | Speed‑up × |
| --------- | --------------- | -------------- | ---------- |
| blend     | **39 144.23**   | 464.04         | **84.36×** |

### Cropping (`crop_margins`)

*Resolution: 1920 × 1080 → 1720 × 980*

| Method        | GPU (no cache) FPS | GPU (cache) FPS | Pillow FPS | Speed‑up no‑cache × | Speed‑up cache × |
| ------------- | ------------------ | --------------- | ---------- | ------------------- | ---------------- |
| crop\_margins | 1 690.29           | **12 359.09**   | 626.57     | 2.70×               | **19.73×**       |

### Filling

| Operation      | GPU FPS       | Pillow FPS | Speed‑up ×  |
| -------------- | ------------- | ---------- | ----------- |
| fill\_color    | 11 960.15     | 6 477.89   | 1.85×       |
| fill\_gradient | **13 553.62** | 79.47      | **170.54×** |

### Resizing (`resize` → 1920 × 1080 → 1280 × 720)

| Method   | GPU (no cache) FPS | GPU (cache) FPS | Pillow FPS | Speed‑up no‑cache × | Speed‑up cache × |
| -------- | ------------------ | --------------- | ---------- | ------------------- | ---------------- |
| NEAREST  | 2 456.03           | **25 562.55**   | 830.38     | 2.96×               | **30.78×**       |
| BILINEAR | 2 327.16           | **21 242.36**   | 42.45      | 54.82×              | **500.36×**      |
| BICUBIC  | 2 162.25           | **8 842.59**    | 30.55      | 70.77×              | **289.42×**      |

## Discussion

- **GPU cache wins** – Re‑using pre‑allocated output buffers removes all CUDA allocation overhead and multiplies throughput by up to **10×** compared with the naïve GPU path.
- **Bilinear resize** shows the largest absolute gain (over **500×** faster than Pillow) because the CPU version is extremely compute‑bound, whereas the GPU variant distributes the interpolation across thousands of threads.
- `` exhibits only a modest 1.85× speed‑up because the operation is fully memory‑bandwidth‑bound and already trivial on the CPU.
- Even *without caching*, PhotoFF is between **3× and 71×** faster than Pillow across this test‑set.

## Reproducing the Benchmarks

```bash
cd photoff/tests
python blend_speed.py
python crop_speed.py
python fill_speed.py
python resize_speed.py
```

All scripts print a detailed comparison table to stdout. For consistent results close other GPU‑intensive applications and ensure the GPU is running at its maximum performance profile.

## Conclusion

PhotoFF’s CUDA backend delivers **order‑of‑magnitude performance gains** over traditional CPU‑based imaging libraries, making real‑time or batch‑processing workloads practical even at high resolutions. Further gains are possible by batching multiple operations together and minimising host‑device transfers, as explained in the [Advanced Topics](advanced.md) guide.

