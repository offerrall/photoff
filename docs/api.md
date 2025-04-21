# PhotoFF API Reference

This reference covers all public functions and types available in the PhotoFF library. For usage examples and patterns, refer to [Basics](basics.md) and [Advanced Topics](advanced.md).

---

## Core Types

### `CudaImage(width: int, height: int)`
Represents an image in GPU memory (buffer of type `uchar4`).

**Attributes:**
- `.width`: logical width (adjustable without reallocating)
- `.height`: logical height (adjustable without reallocating)
- `.buffer`: pointer to the GPU memory

**Methods:**
- `.free()` — Frees the GPU memory

---

### `RGBA(r: int, g: int, b: int, a: int = 255)`
Color type with alpha channel. Used in all color-related operations.

---

## Module `photoff.io`

### `load_image(filename: str, container: CudaImage = None) -> CudaImage`
Loads an image from disk into GPU memory.

### `save_image(image: CudaImage, filename: str)`
Saves a `CudaImage` from GPU memory to disk.

### `image_to_pil(image: CudaImage) -> PIL.Image`
Converts a `CudaImage` into a PIL image.

---

## Module `photoff.operations.fill`

### `fill_color(image: CudaImage, color: RGBA)`
Fills the entire image with a solid color.

### `fill_gradient(image: CudaImage, color1: RGBA, color2: RGBA, direction: int = 0, seamless: bool = False)`
Fills the image with a gradient between two colors.

---

## Module `photoff.operations.filters`

### `apply_gaussian_blur(image: CudaImage, radius: float, image_copy_cache: CudaImage = None)`
Applies Gaussian blur using an auxiliary buffer.

### `apply_corner_radius(image: CudaImage, size: int)`
Rounds the corners of the image.

### `apply_opacity(image: CudaImage, opacity: float)`
Modifies the global opacity of the image.

### `apply_flip(image: CudaImage, flip_horizontal: bool = False, flip_vertical: bool = False)`
Flips the image horizontally or vertically.

### `apply_grayscale(image: CudaImage)`
Converts the image to grayscale.

### `apply_chroma_key(image: CudaImage, key_image: CudaImage, channel: str = "A", threshold: int = 128, invert: bool = False, zero_all_channels: bool = False)`
Applies a chroma key effect based on a channel comparison.

### `apply_stroke(image: CudaImage, stroke_width: int, stroke_color: RGBA, image_copy_cache: CudaImage = None, inner: bool = True)`
Draws a border around non-transparent regions.

### `apply_shadow(image: CudaImage, radius: float, intensity: float, shadow_color: RGBA, image_copy_cache: CudaImage = None, inner: bool = False)`
Applies a soft shadow inside or outside the image.

---

## Module `photoff.operations.resize`

### `resize(image: CudaImage, width: int, height: int, method: ResizeMethod = ResizeMethod.BICUBIC, resize_image_cache: CudaImage = None) -> CudaImage`
Resizes an image using interpolation.

### `crop_margins(image: CudaImage, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0, crop_image_cache: CudaImage = None) -> CudaImage`
Crops the specified margins from an image.

### `ResizeMethod`
```python
class ResizeMethod(Enum):
    NEAREST = "nearest"
    BILINEAR = "bilinear"
    BICUBIC = "bicubic"
```

---

## Module `photoff.operations.blend`

### `blend(background: CudaImage, over: CudaImage, x: int, y: int)`
Alpha-blends an image onto another at a given position.

---

## Module `photoff.operations.text`

### `render_text(text: str, font_path: str, font_size: int = 24, color: RGBA = RGBA(0,0,0,255)) -> CudaImage`
Renders text as an RGBA image in GPU memory.

---

## Module `photoff.operations.utils`

### `get_padding_size(image: CudaImage, padding: int) -> tuple[int, int]`
Returns the full dimensions of the image including padding.

### `get_no_padding_size(image: CudaImage, padding: int) -> tuple[int, int]`
Returns the image dimensions excluding padding.

### `blend_aligned(background: CudaImage, image: CudaImage, align: str = "center", offset_x: int = 0, offset_y: int = 0)`
Blends an image onto a background with automatic alignment.

### `get_cover_resize_dimensions(image: CudaImage, container_width: int, container_height: int) -> tuple[int, int]`
Computes resize dimensions to cover a container.

### `cover_image_in_container(...) -> CudaImage`
Resizes and centers an image inside a container using reusable buffers.

### `create_image_grid(...) -> CudaImage`
Creates a grid filled with repeated instances of an image.

---

For advanced memory optimization techniques, see [Advanced Topics](advanced.md).

