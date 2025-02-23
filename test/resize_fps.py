from time import perf_counter
from photoff import CudaImage
from photoff.operations.resize import resize, ResizeMethod
from photoff.operations.fill import fill_color
from photoff import RGBA

def measure_resize_fps(
    src_width=1920,
    src_height=1080,
    dst_width=1280,
    dst_height=720,
    method=ResizeMethod.BILINEAR,
    iterations=100
):

    source_image = CudaImage(src_width, src_height)
    fill_color(source_image, RGBA(255, 0, 0, 255))
    
    result_image = CudaImage(dst_width, dst_height)
    
    start_time = perf_counter()
    for _ in range(iterations):
        resize(source_image, dst_width, dst_height, method=method)
    end_time = perf_counter()
    
    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')
    
    print(f"Method: {method.value}")
    print(f"Resolution: {src_width}x{src_height} -> {dst_width}x{dst_height}")
    print(f"Completed {iterations} resize operations in {elapsed_time:.2f} seconds.")
    print(f"Resize FPS: {fps:.2f}")
    
    source_image.free()
    result_image.free()
    return fps, elapsed_time

def compare_resize_methods(
    src_width=1920,
    src_height=1080,
    dst_width=1280,
    dst_height=720,
    iterations=100
):
    print("Testing BILINEAR resize:")
    bilinear_fps, bilinear_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.BILINEAR,
        iterations
    )
    
    print("\nTesting NEAREST resize:")
    nearest_fps, nearest_time = measure_resize_fps(
        src_width, src_height,
        dst_width, dst_height,
        ResizeMethod.NEAREST,
        iterations
    )
    
    print("\nComparison:")
    print(f"BILINEAR: {bilinear_fps:.2f} FPS ({bilinear_time:.2f}s)")
    print(f"NEAREST:  {nearest_fps:.2f} FPS ({nearest_time:.2f}s)")
    print(f"Speed difference: {(nearest_fps/bilinear_fps - 1)*100:.1f}% (+ means NEAREST is faster)")

if __name__ == "__main__":
    compare_resize_methods()