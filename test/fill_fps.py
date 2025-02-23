from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.fill import fill_color

def measure_fill_fps(width=1920, height=1080,
                     color=RGBA(255, 0, 0, 255),
                     iterations=100):
    """Mide el rendimiento (FPS) de la operación fill_color."""
    cuda_image = CudaImage(width, height)

    start_time = perf_counter()
    for _ in range(iterations):
        fill_color(cuda_image, color)
    end_time = perf_counter()

    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')

    print(f"Completed {iterations} fill operations in {elapsed_time:.2f} seconds.")
    print(f"Fill FPS: {fps:.2f}")

    cuda_image.free()
    return fps, elapsed_time

if __name__ == "__main__":
    measure_fill_fps()
