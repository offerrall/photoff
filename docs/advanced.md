# PhotoFF Advanced Topics

This guide covers advanced techniques for optimizing performance when working with the PhotoFF library. It focuses on efficient memory management, buffer reuse, and optimization strategies.

## Memory Management Strategies

### Understanding GPU Memory Allocation

PhotoFF's `CudaImage` objects allocate GPU memory. Creating and freeing these objects frequently can lead to memory fragmentation and performance degradation. Advanced applications should:

1. Pre-allocate buffers at the start of your application
2. Reuse these buffers for different operations
3. Only free memory when truly done with processing

### Buffer Reuse Pattern

Most PhotoFF operations support a destination buffer parameter, allowing you to reuse existing GPU memory:

```python
from photoff.core.types import CudaImage
from photoff.operations.resize import resize, ResizeMethod

# Create buffers once
original = CudaImage(1920, 1080)
resized_cache = CudaImage(800, 600)  # Reusable buffer for resized images

# Reuse the resized_cache buffer instead of allocating new memory
resize(original, 800, 600, method=ResizeMethod.BICUBIC, resize_image_cache=resized_cache)
```

## Real-World Example: Collage Generator

The following example demonstrates sophisticated buffer reuse in a production environment:

```python
from photoff.core.types import CudaImage, RGBA
from photoff.operations.filters import apply_corner_radius
from photoff.operations.utils import cover_image_in_container, get_cover_resize_dimensions
from photoff.operations.blend import blend
from photoff.operations.resize import resize, ResizeMethod
from photoff.operations.fill import fill_color

# Pre-allocate all required buffers once
PRINT_WIDTH = 2480
PRINT_HEIGHT = 3500
PREVIEW_WIDTH = 600
PREVIEW_HEIGHT = 848

# These buffers will be reused throughout the entire application lifecycle
print_collage_cache = CudaImage(PRINT_WIDTH, PRINT_HEIGHT)
preview_collage_cache = CudaImage(PREVIEW_WIDTH, PREVIEW_HEIGHT)
cover_cache = CudaImage(5000, 5000)
cover_resize_cache = CudaImage(5000, 5000)

def create_collage(grid_data, corner_radius=50, background_color=RGBA(255, 255, 255, 255), padding=30):
    # Reuse the print_collage_cache instead of creating a new buffer
    fill_color(print_collage_cache, background_color)
    
    for cell in grid_data.cells:
        # Calculate dimensions
        width = cell_width - padding*2
        height = cell_height - padding*2
        
        # Reuse the cover_cache buffer by adjusting its logical dimensions
        # This avoids allocating new memory for each cell
        cover_cache.width = width
        cover_cache.height = height

        # Calculate resize dimensions for the image to cover the cell
        resize_size = get_cover_resize_dimensions(source_image, width, height)
        
        # Reuse the resize cache buffer with new dimensions
        cover_resize_cache.width = resize_size[0]
        cover_resize_cache.height = resize_size[1]
        
        # Place the image in the cell using the reused buffers
        cover_image_in_container(
            source_image,
            width, height,
            0, 0,
            background_color,
            container_image_cache=cover_cache,
            resize_image_cache=cover_resize_cache
        )
        
        # Apply effects to the cell
        apply_corner_radius(cover_cache, corner_radius)
        
        # Blend the cell onto the main collage
        blend(print_collage_cache, cover_cache, x_position, y_position)
    
    # Create preview-sized version using the pre-allocated buffer
    resize(
        print_collage_cache, 
        PREVIEW_WIDTH, PREVIEW_HEIGHT, 
        method=ResizeMethod.BICUBIC,
        resize_image_cache=preview_collage_cache
    )
    
    # Return the preview image (no need to free buffers as they are reused)
    return preview_collage_cache
```

## Working with Temporary Buffers

Many operations require temporary buffers for intermediate results. PhotoFF provides two approaches:

### 1. Explicitly Providing Temporary Buffers

```python
from photoff.operations.filters import apply_gaussian_blur
from photoff.core.types import CudaImage

# Create the main image and a temporary buffer with the same dimensions
image = CudaImage(800, 600)
temp_buffer = CudaImage(800, 600)

# Use the temporary buffer for operations that need it
apply_gaussian_blur(image, radius=5.0, image_copy_cache=temp_buffer)
```

### 2. Automatic Temporary Buffer Management

If you don't provide a temporary buffer, PhotoFF will create and free one automatically:

```python
# This works but is less efficient for repeated operations
apply_gaussian_blur(image, radius=5.0)  # Temporary buffer created and freed internally
```

## Buffer Dimension Management

A unique feature of PhotoFF is the ability to reuse buffers even for different size requirements by adjusting their logical dimensions:

```python
# Create a large buffer once
multi_purpose_buffer = CudaImage(2000, 2000)

# Use it for a 800x600 operation by changing the logical dimensions
multi_purpose_buffer.width = 800
multi_purpose_buffer.height = 600

# Later, use it for a 1200x900 operation
multi_purpose_buffer.width = 1200
multi_purpose_buffer.height = 900
```

This technique allows you to minimize memory allocations by having a few large buffers that can be logically resized.

## Performance Tips

1. **Batch Similar Operations**: Group similar operations to minimize context switching.

2. **Size Buffers Appropriately**: Allocate buffers that are large enough for your maximum expected size, then adjust the logical dimensions as needed.

3. **Minimize Host-Device Transfers**: Loading and saving images involves transferring data between CPU and GPU memory, which is slow. Perform all processing on the GPU before transferring back to the CPU.

4. **Profile Your Application**: Use timing functions to identify bottlenecks:

```python
from time import time

start = time()
# Your operation
end = time()
print(f"Operation took {end - start:.4f} seconds")
```

5. **Cache Images**: If you repeatedly use the same source images, keep them loaded in GPU memory.

## Cleanup Strategies

Even with buffer reuse, proper cleanup is essential. Establish clear ownership patterns for GPU resources:

1. Functions that create `CudaImage` objects should explicitly document whether the caller is responsible for freeing them.

2. Consider using context managers for automatic cleanup:

```python
from contextlib import contextmanager

@contextmanager
def using_cuda_image(width, height):
    image = CudaImage(width, height)
    try:
        yield image
    finally:
        image.free()

# Usage
with using_cuda_image(800, 600) as img:
    # Use img here
    fill_color(img, RGBA(255, 0, 0, 255))
    # img will be automatically freed when the block exits
```

By implementing these advanced strategies, your PhotoFF applications can achieve maximum performance while maintaining clean, maintainable code.