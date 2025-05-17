# PhotoFF Basics

This guide covers the fundamental concepts and operations of the PhotoFF library. After reading this, you'll understand how to load, manipulate, and save images using GPU acceleration.

## Core Concepts

### CudaImage

The `CudaImage` class is the central object in PhotoFF. It represents an image stored in GPU memory as a RGBA buffer.

> **Note:** `CudaImage` does **not** guarantee that the newly reserved GPU memory is zero‑initialized. If you plan to use the image as a fully transparent background, clear it right after allocation:
>
> ```python
> from photoff.core.types import CudaImage, RGBA
> from photoff.operations.fill import fill_color
>
> image = CudaImage(800, 600)
> fill_color(image, RGBA(0, 0, 0, 0))  # Ensure full transparency
> ```

```python
from photoff.core.types import CudaImage

# Reserving GPU memory for an 800x600 image
image = CudaImage(800, 600)

# Free the image from GPU memory when done
image.free()
```

### RGBA

PhotoFF uses the RGBA color model (Red, Green, Blue, Alpha) for all operations:

```python
from photoff.core.types import RGBA

# Create colors
red = RGBA(255, 0, 0, 255)         # Solid red
blue = RGBA(0, 0, 255, 255)        # Solid blue
semi_transparent = RGBA(0, 255, 0, 128)  # Semi-transparent green
transparent = RGBA(0, 0, 0, 0)     # Completely transparent
```

## Basic Operations

### Loading and Saving Images

To load images from disk and save them back:

```python
from photoff.io import load_image, save_image
from photoff.core.types import CudaImage

# Load an image from disk into GPU memory
image = load_image("input.jpg")

# Save an image to disk
save_image(image, "output.png")

# Free the image from GPU memory
image.free()
```

### Image Filling

Fill an image with a solid color or gradient:

```python
from photoff.operations.fill import fill_color, fill_gradient
from photoff.core.types import CudaImage, RGBA

# Create and fill with solid color
image = CudaImage(400, 300)
fill_color(image, RGBA(255, 0, 0, 255))  # Fill with red

# Fill with gradient
start_color = RGBA(255, 0, 0, 255)  # Red
end_color = RGBA(0, 0, 255, 255)    # Blue
direction = 0  # 0: horizontal, 1: vertical, 2: diagonal, 3: radial
seamless = False
fill_gradient(image, start_color, end_color, direction, seamless)

# Free the image from GPU memory
image.free()
```

### Applying Filters

PhotoFF offers various filters to modify images:

```python
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius, apply_grayscale
from photoff.io import load_image, save_image

# Load an image
image = load_image("input.jpg")

# Apply a Gaussian blur
apply_gaussian_blur(image, radius=5.0)

# Round the corners
apply_corner_radius(image, size=20)

# Convert to grayscale
apply_grayscale(image)

# Save the result
save_image(image, "filtered.png")

# Free the image from GPU memory
image.free()
```

### Resizing Images

Resize images with different interpolation methods:

```python
from photoff.operations.resize import resize, ResizeMethod
from photoff.io import load_image, save_image

# Load an image
image = load_image("input.jpg")

# Resize to 400x300 using bicubic interpolation
resized = resize(image, 400, 300, method=ResizeMethod.BICUBIC)

# Save the result
save_image(resized, "resized.png")

# Free both images
image.free()
resized.free()
```

### Blending Images

Combine multiple images together:

```python
from photoff.operations.blend import blend
from photoff.io import load_image, save_image
from photoff.core.types import CudaImage, RGBA
from photoff.operations.fill import fill_color

# Create a background
background = CudaImage(800, 600)
fill_color(background, RGBA(200, 200, 200, 255))  # Light gray

# Load a foreground image
foreground = load_image("logo.png")

# Blend the foreground onto the background at position (100, 100)
blend(background, foreground, 100, 100)

# Save the result
save_image(background, "blended.png")

# Free the images from GPU memory
background.free()
foreground.free()
```

## Next Steps

Now that you understand the basics, you can:

* Explore the [Advanced Topics](advanced.md) for more memory management and performance tips
* Check the [API Reference](api.md) for detailed information on all functions
