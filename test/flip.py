from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.filters import apply_flip
from photoff.operations.fill import fill_color

def measure_flip_fps(width=1920, height=1080,
                    color=RGBA(255, 0, 0, 255),
                    flip_horizontal=True,
                    flip_vertical=False,
                    iterations=100):
    """Mide el rendimiento (FPS) de la operación apply_flip."""
    cuda_image = CudaImage(width, height)
    fill_color(cuda_image, color)
    
    start_time = perf_counter()
    for _ in range(iterations):
        apply_flip(cuda_image, flip_horizontal, flip_vertical)
    end_time = perf_counter()
    
    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')
    
    print(f"Flip mode: {'horizontal' if flip_horizontal else ''}"
          f"{' and ' if flip_horizontal and flip_vertical else ''}"
          f"{'vertical' if flip_vertical else ''}")
    print(f"Completed {iterations} flip operations in {elapsed_time:.2f} seconds.")
    print(f"Flip FPS: {fps:.2f}")

    cuda_image.free()
    return fps, elapsed_time

def compare_flip_modes(iterations=100):
    """Compara el rendimiento entre los diferentes modos de flip."""
    
    print("\nTesting Horizontal Flip:")
    h_fps, h_time = measure_flip_fps(flip_horizontal=True, flip_vertical=False, 
                                   iterations=iterations)
    
    print("\nTesting Vertical Flip:")
    v_fps, v_time = measure_flip_fps(flip_horizontal=False, flip_vertical=True, 
                                   iterations=iterations)
    
    print("\nTesting Both Flips:")
    b_fps, b_time = measure_flip_fps(flip_horizontal=True, flip_vertical=True, 
                                   iterations=iterations)
    
    print("\nMode Comparison:")
    print(f"Horizontal Flip: {h_fps:.2f} FPS")
    print(f"Vertical Flip: {v_fps:.2f} FPS")
    print(f"Both Flips: {b_fps:.2f} FPS")
    
    # Encontrar el más rápido
    modes = {
        'Horizontal': h_fps,
        'Vertical': v_fps,
        'Both': b_fps
    }
    fastest = max(modes.items(), key=lambda x: x[1])
    print(f"\nFastest mode: {fastest[0]} ({fastest[1]:.2f} FPS)")

if __name__ == '__main__':
    compare_flip_modes()