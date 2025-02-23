from photoff import RGBA, CudaImage
from photoff.operations.fill import fill_color

from time import perf_counter

def measure_fill_fps(width=1920, height=1080, color=RGBA(255, 0, 0, 255), iterations=10000):

    cuda_image = CudaImage(width, height)

    start_time = perf_counter()
    for _ in range(iterations):
        last_time = perf_counter()
        fill_color(cuda_image, RGBA(255, 0, 0, 255))
        last_time = perf_counter() - last_time
    end_time = perf_counter()

    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time

    print(f"Completed {iterations} fill operations in {elapsed_time:.2f} seconds.")
    print(f"Fill FPS: {fps:.2f}")

    return last_time

if __name__ == "__main__":
    print(F"Last time: {measure_fill_fps()}")