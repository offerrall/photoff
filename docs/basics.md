# PhotoFF Basics

This guide covers the fundamental concepts and operations of the PhotoFF library. After reading this, you'll understand how to load, manipulate, and save images using GPU acceleration.

## Core Concepts

PhotoFF is built around a few key concepts:

### CudaImage

The `CudaImage` class is the central object in PhotoFF. It represents an image stored in GPU memory as a RGBA buffer.

```python
from photoff.core.types import CudaImage

# Create a blank 800x600 image
image = CudaImage(800, 600)

# Always free GPU memory when done
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

# Load an image from disk
image = load_image("input.jpg")

# Save an image to disk
save_image(image, "output.png")

# Always free memory when done
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

# Don't forget to free
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

# Free memory
background.free()
foreground.free()
```

## Memory Management

PhotoFF operates on GPU memory, which makes it fast but requires careful management:

1. Always call `.free()` on any `CudaImage` when you're done with it
2. For complex operations, consider reusing existing buffers:

```python
# Inefficient - creates a new buffer for each operation
image = load_image("input.jpg")
apply_gaussian_blur(image, radius=5.0)
apply_corner_radius(image, size=20)
save_image(image, "output.png")
image.free()

# More efficient - reuses the buffer for the blur operation
image = load_image("input.jpg")
buffer = CudaImage(image.width, image.height)  # Create once, reuse multiple times
apply_gaussian_blur(image, radius=5.0, image_copy_cache=buffer)
apply_corner_radius(image, size=20)
save_image(image, "output.png")
image.free()
buffer.free()
```

## Basic Image Processing Workflow

A typical workflow using PhotoFF might look like this:

```python
from photoff.io import load_image, save_image
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.operations.resize import resize, ResizeMethod

# Load the image
original = load_image("input.jpg")

# Resize if needed
if original.width > 1000 or original.height > 1000:
    resized = resize(original, 1000, 1000, method=ResizeMethod.BICUBIC)
    original.free()  # Free the original once we have the resized copy
    image = resized
else:
    image = original

# Create a buffer for operations that need it
buffer = CudaImage(image.width, image.height)

# Apply processing operations
apply_gaussian_blur(image, radius=3.0, image_copy_cache=buffer)
apply_corner_radius(image, size=30)

# Save the result
save_image(image, "processed.png")

# Clean up
image.free()
buffer.free()
```

## Next Steps

Now that you understand the basics, you can:

- Explore the [Advanced Topics](advanced.md) for more complex operations
- Check the [API Reference](api.md) for detailed information on all functions
- Try combining multiple effects to create unique image transformations
