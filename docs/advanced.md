# PhotoFF Advanced Topics

This guide covers advanced techniques for optimizing performance when working with the PhotoFF library, with special focus on efficient GPU memory management through buffer reuse.

## Understanding GPU Memory Management

### The Cost of GPU Memory Operations

When working with CUDA-accelerated image processing, memory operations are among the most expensive:

1. **Allocations**: Each call to `CudaImage()` triggers a `cudaMalloc()` operation which is relatively slow
2. **Transfers**: Moving data between CPU and GPU memory is extremely expensive
3. **Deallocations**: Freeing memory with `.free()` triggers `cudaFree()` which also has overhead
4. **Fragmentation**: Frequent allocations and deallocations can fragment GPU memory

PhotoFF provides several strategies to minimize these costs:

## Strategic Buffer Reuse Patterns

### 1. Operation Output Caching

Many operations naturally produce new output (resize, crop, filters). PhotoFF allows passing pre-allocated destination buffers instead of creating new memory:

```python
from photoff.core.types import CudaImage
from photoff.operations.resize import resize, ResizeMethod

# Pre-allocate source and destination buffers once
original = CudaImage(1920, 1080)
resized_cache = CudaImage(800, 600)

# Use pre-allocated buffer as destination
resize(original, 800, 600, method=ResizeMethod.BICUBIC, resize_image_cache=resized_cache)
```

Common cache parameters throughout the library:
- `resize_image_cache` for resize operations
- `container_image_cache` for container operations
- `image_copy_cache` for filters requiring a copy of the original
- `crop_image_cache` for cropping operations

### 2. Temporary Buffer Reuse

Some operations like blur, shadow, and stroke require a copy of the original image for internal calculations. You can reuse the same temporary buffer across multiple operations:

```python
from photoff.operations.filters import apply_gaussian_blur, apply_shadow
from photoff.core.types import CudaImage, RGBA

# Create main image and shared temporary buffer
image = CudaImage(800, 600)
temp_buffer = CudaImage(800, 600)  # Same dimensions required

# Reuse temp buffer for different operations
apply_gaussian_blur(image, radius=5.0, image_copy_cache=temp_buffer)
apply_shadow(
    image, 
    radius=10.0, 
    intensity=0.5, 
    shadow_color=RGBA(0, 0, 0, 128),
    image_copy_cache=temp_buffer  # Same buffer reused
)
```

### 3. Logical Dimension Adjustment - The Core Optimization Technique

The most powerful feature in PhotoFF is the ability to allocate a large maximum memory buffer once, and then dynamically change its logical dimensions as needed:

```python
from photoff.core.types import CudaImage
from photoff.operations.resize import resize, ResizeMethod

# Allocate ONE large buffer with maximum dimensions you'll ever need
# This is the key pattern - allocate once, reuse everywhere
multi_purpose_buffer = CudaImage(5000, 5000)  # 5000x5000 memory allocated

# Now you can change the logical dimensions at any time
# IMPORTANT: This only changes metadata, not the actual memory allocation!
# It simply tells PhotoFF functions how much of the buffer to read/write
multi_purpose_buffer.width = 800   # Just updates a property, no memory operation
multi_purpose_buffer.height = 600  # Just updates a property, no memory operation

# Now use it as a destination buffer for operations
# The function will only use the first 800x600 pixels of the allocated memory
resize(source_image, 800, 600, resize_image_cache=multi_purpose_buffer)

# Later, you can change to different dimensions (still using same memory)
multi_purpose_buffer.width = 1200   # Again, just changing metadata
multi_purpose_buffer.height = 900   # No memory allocation happens
resize(another_image, 1200, 900, resize_image_cache=multi_purpose_buffer)
```

This technique is the heart of PhotoFF's memory optimization. The width and height properties are just metadata that tell operations how much of the pre-allocated memory to use - they don't trigger any GPU memory operations. This allows you to allocate once at startup and never worry about memory fragmentation again.

## Real-World Example: Collage Generator

The following example from a production collage generator demonstrates all three reuse patterns:

```python
from photoff.core.types import CudaImage, RGBA
from photoff.operations.filters import apply_corner_radius
from photoff.operations.utils import cover_image_in_container
from photoff.operations.resize import resize, ResizeMethod

# Pre-allocate buffers once at module level
PRINT_WIDTH, PRINT_HEIGHT = 2480, 3500
PREVIEW_WIDTH, PREVIEW_HEIGHT = 600, 848

# These buffers will be reused for all collages created
print_collage_cache = CudaImage(PRINT_WIDTH, PRINT_HEIGHT)
preview_collage_cache = CudaImage(PREVIEW_WIDTH, PREVIEW_HEIGHT)

# Create oversized buffers that will be logically resized as needed
# This is critical - we allocate maximum needed size once
cover_cache = CudaImage(5000, 5000)
cover_resize_cache = CudaImage(5000, 5000)

def create_collage(grid_data, corner_radius=50, background_color=RGBA(255, 255, 255, 255)):
    # Reuse print_collage_cache instead of creating a new buffer
    fill_color(print_collage_cache, background_color)
    
    for cell in grid_data.cells:
        # Calculate cell dimensions
        width = x1_padded - x0_padded
        height = y1_padded - y0_padded
        
        # IMPORTANT: Adjust logical dimensions of oversized buffers
        # This doesn't trigger any memory allocation as long as
        # width/height are smaller than the allocated buffer size
        cover_cache.width = width
        cover_cache.height = height

        # Calculate resize dimensions for cover fit
        resize_size = get_cover_resize_dimensions(source_image, width, height)
        
        # Adjust dimensions of the resize cache buffer
        cover_resize_cache.width = resize_size[0]
        cover_resize_cache.height = resize_size[1]
        
        # Use both cache buffers in the operation
        cover_image_in_container(
            source_image,
            width, height,
            0, 0,
            background_color,
            container_image_cache=cover_cache,  # Reuse container buffer
            resize_image_cache=cover_resize_cache  # Reuse resize buffer
        )
        
        # Apply effects and blend with cached destination
        apply_corner_radius(cover_cache, corner_radius)
        blend(print_collage_cache, cover_cache, x_position, y_position)
    
    # Create preview-sized version using another pre-allocated buffer
    resize(
        print_collage_cache, 
        PREVIEW_WIDTH, PREVIEW_HEIGHT, 
        method=ResizeMethod.BICUBIC,
        resize_image_cache=preview_collage_cache  # Reuse preview buffer
    )
    
    # Return the preview image (no memory freed as buffers will be reused)
    return preview_collage_cache
```

## Buffer Validation and Error Handling

PhotoFF validates buffer dimensions before reusing them:

```python
# From resize.py
if resize_image_cache.width != width or resize_image_cache.height != height:
    raise ValueError(
        f"Destination image dimensions must match resize dimensions: {width}x{height}, got {resize_image_cache.width}x{resize_image_cache.height}"
    )
```

This ensures that reused buffers have appropriate dimensions for the operation.

## CUDA Operation Implementation Details

Looking at the CUDA implementation, we can see how operations are designed to work with pre-allocated buffers:

```c
// Example from photoff.cu - gaussian blur implementation
void apply_gaussian_blur(uchar4* buffer,          // Destination buffer
                         const uchar4* copy_buffer,  // Source buffer (original image copy)
                         uint32_t width,
                         uint32_t height,
                         float radius) {
    // Use CUDA kernel with provided buffers
    gaussianBlurKernel<<<grid, block>>>(copy_buffer, buffer, width, height, radius);
    cudaDeviceSynchronize();
}
```

## Advanced Buffer Management Strategies

### 1. Buffer Pooling

For complex applications, implement a buffer pool:

```python
class BufferPool:
    def __init__(self):
        self.pools = {}  # Maps (width, height) to list of available buffers
        
    def get_buffer(self, width, height):
        key = (width, height)
        if key in self.pools and self.pools[key]:
            return self.pools[key].pop()
        return CudaImage(width, height)
        
    def release_buffer(self, buffer):
        key = (buffer.width, buffer.height)
        if key not in self.pools:
            self.pools[key] = []
        self.pools[key].append(buffer)
        
    def clear(self):
        for buffers in self.pools.values():
            for buffer in buffers:
                buffer.free()
        self.pools.clear()
```

### 2. Use Oversized Buffers with Dynamic Adjustment

Pre-allocate buffers at maximum expected size, then adjust logical dimensions as needed:

```python
# Allocate maximum possible size
max_buffer = CudaImage(4000, 4000)

# When processing a 800x600 image
max_buffer.width = 800
max_buffer.height = 600
process_image(max_buffer)

# When processing a 1200x900 image
max_buffer.width = 1200
max_buffer.height = 900
process_image(max_buffer)
```

This approach is extremely efficient for processing multiple images of varying sizes.

### 3. Context Managers for Clean Resource Management

```python
from contextlib import contextmanager

@contextmanager
def using_buffer_pool(buffer_pool, width, height):
    buffer = buffer_pool.get_buffer(width, height)
    try:
        yield buffer
    finally:
        buffer_pool.release_buffer(buffer)

# Usage
with using_buffer_pool(pool, 800, 600) as temp:
    # Use temp buffer
    pass  # Automatically released back to pool when done
```

## Performance Monitoring

Track memory usage and operation timing:

```python
from time import time

def timed_operation(name, func, *args, **kwargs):
    start = time()
    result = func(*args, **kwargs)
    duration = time() - start
    print(f"{name} took {duration:.4f} seconds")
    return result

# Usage
resized = timed_operation("Resize operation", 
                         resize, image, 800, 600, 
                         method=ResizeMethod.BICUBIC)
```

## Best Practices Summary

1. **Pre-allocate buffers** at the start of your application
2. **Oversized buffers** with logical dimension adjustment are extremely efficient
3. **Reuse temporary buffers** for operations that need them
4. **Batch similar operations** to minimize context switching
5. **Monitor performance** to identify memory bottlenecks
6. **Minimize host-device transfers** by keeping processing on the GPU
7. **Size buffers appropriately** for your maximum expected dimensions
8. **Have a clear ownership strategy** for GPU resources to avoid leaks

By implementing these advanced buffer management techniques, you can achieve exceptional performance with PhotoFF while maintaining clean, maintainable code.