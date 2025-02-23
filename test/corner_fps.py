import time
import sys
from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_corner_radius
from photoff import RGBA, CudaImage

def corner_border_fps(color=(255, 0, 0, 255), border_size=100, iterations=100):

    image = CudaImage(1920, 1080)
    fill_color(image, RGBA(*color))
    
    start_time = time.time()
    for _ in range(iterations):
        apply_corner_radius(image, border_size)
    end_time = time.time()
    
    total_time = end_time - start_time
    fps = iterations / total_time if total_time > 0 else float('inf')
    
    image.free()
    return fps, total_time

if __name__ == '__main__':

    border_size = 100
    iterations = 100

    fps, total_time = corner_border_fps(border_size=border_size, iterations=iterations)
    print(f"FPS: {fps:.2f} (calculado en {iterations} iteraciones en {total_time:.4f} segundos)")
