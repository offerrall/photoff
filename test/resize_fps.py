from time import perf_counter
from photoff import CudaImage
from photoff.operations.resize import resize, ResizeMethod
from photoff.operations.fill import fill_color
from photoff import RGBA

def measure_resize_fps(
    src_width=1920,
    src_height=1080,
    dst_width=1920,
    dst_height=1080,
    method=ResizeMethod.BILINEAR,
    iterations=100,
    reuse_buffer=True
):
    source_image = CudaImage(src_width, src_height)
    fill_color(source_image, RGBA(255, 0, 0, 255))
    
    result_image = CudaImage(dst_width, dst_height) if reuse_buffer else None
    
    start_time = perf_counter()
    for _ in range(iterations):
        resize(source_image, dst_width, dst_height, method=method, dst_image=result_image)
    end_time = perf_counter()
    
    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')
    
    buffer_mode = "reused buffer" if reuse_buffer else "new buffer each time"
    print(f"Method: {method.value} ({buffer_mode})")
    print(f"Resolution: {src_width}x{src_height} -> {dst_width}x{dst_height}")
    print(f"Completed {iterations} resize operations in {elapsed_time:.2f} seconds.")
    print(f"Resize FPS: {fps:.2f}")
    
    source_image.free()
    if result_image:
        result_image.free()
    return fps, elapsed_time

def compare_resize_methods(
    src_width=1920,
    src_height=1080,
    dst_width=1280,
    dst_height=720,
    iterations=100
):
    print("Testing with buffer reuse:")
    print("\nTesting BILINEAR resize:")
    bilinear_fps, bilinear_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.BILINEAR,
        iterations,
        reuse_buffer=True
    )
    
    print("\nTesting NEAREST resize:")
    nearest_fps, nearest_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.NEAREST,
        iterations,
        reuse_buffer=True
    )
    
    print("\nTesting BICUBIC resize:")
    bicubic_fps, bicubic_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.BICUBIC,
        iterations,
        reuse_buffer=True
    )

    print("\nTesting without buffer reuse:")
    bilinear_no_reuse_fps, bilinear_no_reuse_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.BILINEAR,
        iterations,
        reuse_buffer=False
    )
    
    print("\nComparison:")
    print(f"BILINEAR (reused):  {bilinear_fps:.2f} FPS ({bilinear_time:.2f}s)")
    print(f"BILINEAR (new):     {bilinear_no_reuse_fps:.2f} FPS ({bilinear_no_reuse_time:.2f}s)")
    print(f"NEAREST (reused):   {nearest_fps:.2f} FPS ({nearest_time:.2f}s)")
    print(f"BICUBIC (reused):   {bicubic_fps:.2f} FPS ({bicubic_time:.2f}s)")
    
    print("\nSpeed comparisons:")
    print(f"Buffer reuse speedup: {(bilinear_fps/bilinear_no_reuse_fps - 1)*100:.1f}%")
    print(f"NEAREST vs BILINEAR: {(nearest_fps/bilinear_fps - 1)*100:.1f}%")
    print(f"BICUBIC vs BILINEAR: {(bicubic_fps/bilinear_fps - 1)*100:.1f}%")

if __name__ == "__main__":
    compare_resize_methods()