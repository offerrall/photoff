from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.filters import apply_stroke
from photoff.io import load_image, save_image

def measure_stroke_performance(input_path="./test/logo.png",
                             stroke_width=4,
                             stroke_color=RGBA(0, 255, 0, 255),
                             iterations=100):
    """Compara el rendimiento entre la versión original y la optimizada."""
    
    # Cargamos la imagen una sola vez
    src_image = load_image(input_path)
    image_size = (src_image.width, src_image.height)
    
    # Creamos el buffer de destino que reutilizaremos
    dst_image = CudaImage(*image_size)
    
    # Test de la versión optimizada (con buffer reutilizado)
    print("\nTesting optimized version (reused buffer):")
    start_time = perf_counter()
    for _ in range(iterations):
        apply_stroke(src_image, dst_image, stroke_width, stroke_color)
    end_time = perf_counter()
    
    optimized_time = end_time - start_time
    optimized_fps = iterations / optimized_time if optimized_time > 0 else float('inf')
    
    print(f"Completed {iterations} stroke operations in {optimized_time:.2f} seconds")
    print(f"Optimized FPS: {optimized_fps:.2f}")
    
    # Test de la versión original (creando buffer cada vez)
    print("\nTesting original version (new buffer each time):")
    start_time = perf_counter()
    for _ in range(iterations):
        temp_dst = src_image.copy()
        apply_stroke(src_image, temp_dst, stroke_width, stroke_color)
        temp_dst.free()
    end_time = perf_counter()
    
    original_time = end_time - start_time
    original_fps = iterations / original_time if original_time > 0 else float('inf')
    
    print(f"Completed {iterations} stroke operations in {original_time:.2f} seconds")
    print(f"Original FPS: {original_fps:.2f}")
    
    # Comparación de resultados
    print("\nPerformance Comparison:")
    speedup = (original_time / optimized_time - 1) * 100
    print(f"Speedup: {speedup:.1f}% faster with buffer reuse")
    print(f"Time saved: {original_time - optimized_time:.2f} seconds")
    print(f"Memory operations saved: {iterations} allocations and deallocations")
    
    # Limpieza
    src_image.free()
    dst_image.free()
    
    return {
        'optimized': {'fps': optimized_fps, 'time': optimized_time},
        'original': {'fps': original_fps, 'time': original_time},
        'speedup_percentage': speedup
    }

if __name__ == "__main__":
    measure_stroke_performance()