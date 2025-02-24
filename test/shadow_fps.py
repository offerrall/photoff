from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.filters import apply_shadow
from photoff.io import load_image, save_image

def measure_shadow_performance(input_path="./assets/logo.png",
                             radius=10.0,
                             intensity=0.5,
                             shadow_color=RGBA(0, 0, 0, 128),
                             inner=False,
                             iterations=100):
    """Compara el rendimiento entre la versión original y la optimizada."""
    
    # Cargamos la imagen una sola vez
    src_image = load_image(input_path)
    image_size = (src_image.width, src_image.height)
    
    # Creamos el buffer de destino que reutilizaremos
    dst_image = CudaImage(*image_size)
    
    # Test de la versión optimizada (con buffer reutilizado)
    print(f"\nTesting {'inner' if inner else 'outer'} shadow (reused buffer):")
    start_time = perf_counter()
    for _ in range(iterations):
        apply_shadow(src_image, dst_image, radius, intensity, shadow_color, inner)
    end_time = perf_counter()
    
    optimized_time = end_time - start_time
    optimized_fps = iterations / optimized_time if optimized_time > 0 else float('inf')
    
    print(f"Completed {iterations} shadow operations in {optimized_time:.2f} seconds")
    print(f"Optimized FPS: {optimized_fps:.2f}")
    
    # Test de la versión original (creando buffer cada vez)
    print("\nTesting with new buffer each time:")
    start_time = perf_counter()
    for _ in range(iterations):
        temp_dst = src_image.copy()
        apply_shadow(src_image, temp_dst, radius, intensity, shadow_color, inner)
        temp_dst.free()
    end_time = perf_counter()
    
    original_time = end_time - start_time
    original_fps = iterations / original_time if original_time > 0 else float('inf')
    
    print(f"Completed {iterations} shadow operations in {original_time:.2f} seconds")
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

def compare_shadow_modes(input_path="./assets/logo.png",
                        radius=10.0,
                        intensity=0.5,
                        shadow_color=RGBA(0, 0, 0, 128),
                        iterations=100):
    """Compara el rendimiento entre sombra interna y externa."""
    
    print("Testing Outer Shadow:")
    outer_results = measure_shadow_performance(
        input_path, radius, intensity, shadow_color, False, iterations
    )
    
    print("\nTesting Inner Shadow:")
    inner_results = measure_shadow_performance(
        input_path, radius, intensity, shadow_color, True, iterations
    )
    
    print("\nMode Comparison:")
    print(f"Outer Shadow: {outer_results['optimized']['fps']:.2f} FPS")
    print(f"Inner Shadow: {inner_results['optimized']['fps']:.2f} FPS")
    
    diff = (inner_results['optimized']['fps'] / outer_results['optimized']['fps'] - 1) * 100
    print(f"Performance difference: {abs(diff):.1f}% "
          f"({'inner' if diff > 0 else 'outer'} shadow is faster)")

if __name__ == "__main__":
    compare_shadow_modes()