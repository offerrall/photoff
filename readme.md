# PhotoFF

A high-performance CUDA-accelerated image composition and manipulation library.

## Memory Management & Performance

PhotoFF has been designed with a focus on maximum performance through efficient GPU memory management. The library achieves exceptional processing speeds (up to 30,000 FPS for fill operations at 1920p on an RTX 3070) by implementing several key optimization strategies:

### Buffer Reuse & Memory Control

Unlike many image processing libraries that allocate and free memory for each operation, PhotoFF gives you complete control over buffer allocation and reuse. Key benefits include:

- **Explicit Buffer Management**: Create buffers once and reuse them across multiple operations to eliminate allocation overhead.
- **Processing Pipelines**: Chain multiple effects with zero intermediate allocations.
- **Size Flexibility**: Buffers can be larger than strictly needed for a given operation, allowing pre-allocation of maximum-size buffers that can be reused for smaller operations.

### Example Usage

```python
# Create image and reusable buffer cache once
image = CudaImage(1920, 1080)
cache = CudaImage(1920, 1080)

# Apply multiple effects with zero intermediate allocations
fill_color(image, RGBA(255, 0, 0, 255))
apply_corner_radius(image, 20)
apply_shadow(image, radius=10, intensity=0.5, 
             shadow_color=RGBA(0, 0, 0, 128),
             image_copy_cache=cache)
apply_stroke(image, stroke_width=2, 
             stroke_color=RGBA(255, 255, 255, 255),
             image_copy_cache=cache)
```

### Advanced Buffer Reuse with Virtual Dimensions

One of PhotoFF's most powerful features is the ability to use oversized buffers with virtual dimensions. A single large buffer can be reused for operations on smaller images by adjusting the virtual dimensions:

```python
# Allocate a single large buffer for maximum anticipated size
max_buffer = CudaImage(4096, 4096, auto_init=True)
cache_buffer = CudaImage(4096, 4096, auto_init=True)

# Create different sized images with various effects - all using the same memory
# Example 1: Process a 1080p image with multiple effects in sequence
max_buffer.width, max_buffer.height = 1920, 1080
fill_color(max_buffer, RGBA(0, 100, 255, 255))                           # Fill with blue
apply_corner_radius(max_buffer, 40)                                      # Add rounded corners
apply_opacity(max_buffer, 0.9)                                           # Make slightly transparent
apply_stroke(max_buffer, 5, RGBA(255, 255, 255, 255), cache_buffer)      # Add white border
apply_shadow(max_buffer, 15, 0.7, RGBA(0, 0, 0, 200), cache_buffer)      # Add drop shadow

# Chain more effects with minimal overhead - all on the same buffer
apply_flip(max_buffer, flip_horizontal=True)                             # Flip horizontally

# Example 2: Now use the same buffer for a completely different image
# Just change the dimensions and apply new effects
max_buffer.width, max_buffer.height = 400, 400
fill_gradient(max_buffer, 
              RGBA(255, 50, 50, 255), 
              RGBA(50, 50, 255, 255),
              direction=3,                                               # Radial gradient
              seamless=True)
apply_corner_radius(max_buffer, 200)                                     # Make circular

# Example 3: Create a banner image with the same memory
max_buffer.width, max_buffer.height = 1200, 300
fill_gradient(max_buffer, 
              RGBA(20, 20, 20, 255), 
              RGBA(100, 100, 100, 255),
              direction=1,                                               # Vertical gradient
              seamless=False)
apply_corner_radius(max_buffer, 20)                                      # Slight rounding
apply_stroke(max_buffer, 2, RGBA(200, 200, 200, 255), cache_buffer)      # Subtle border

# Example 4: Use the same buffer as cache for resize operations
source = CudaImage(800, 600)
fill_color(source, RGBA(0, 200, 0, 255))                                # Fill source with green

# Resize the source image using our max_buffer as destination
result = resize(source, 1600, 900, 
                method=ResizeMethod.BICUBIC,
                resize_image_cache=max_buffer)                           # Reuse max_buffer

# Just remember to free when completely done
max_buffer.free()
cache_buffer.free()
source.free()
```

This technique eliminates virtually all memory allocation overhead during processing pipelines, dramatically improving performance for batch operations and real-time applications.
```

### Performance Considerations

- **Processing Speed**: Operations like fill_color achieve ~30,000 FPS at 1920p on an RTX 3070.
- **Zero-Copy Operations**: Many effects modify buffers in-place with no temporary allocations.
- **Cache Parameters**: Operations that would normally require temporary buffers (like shadow, stroke) accept optional pre-allocated cache parameters.
- **Parallelism**: All operations are fully parallelized with optimal CUDA thread blocks (16x16).

### Resource Cleanup

When you're done with your processing pipeline, explicitly free GPU resources:

```python
image.free()
cache.free()
```

### When to Use This Approach

This explicit memory management approach is particularly beneficial for:

- Real-time video processing
- Batch image processing
- Animation rendering
- Any scenario where processing latency is critical

By avoiding the typical overhead of GPU memory allocation/deallocation, PhotoFF achieves performance levels suitable for the most demanding real-time applications.