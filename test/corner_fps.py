from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_corner_radius

def measure_corner_radius_fps(width=1920, height=1080,
                              color=RGBA(255, 0, 0, 255),
                              border_size=100,
                              iterations=100):
    """Mide el rendimiento (FPS) de la operación apply_corner_radius."""
    cuda_image = CudaImage(width, height)
    fill_color(cuda_image, color)
    
    start_time = perf_counter()
    for _ in range(iterations):
        apply_corner_radius(cuda_image, border_size)
    end_time = perf_counter()
    
    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')
    
    print(f"Completed {iterations} corner-radius operations in {elapsed_time:.2f} seconds.")
    print(f"Corner-Radius FPS: {fps:.2f}")

    cuda_image.free()
    return fps, elapsed_time

if __name__ == '__main__':
    measure_corner_radius_fps()
