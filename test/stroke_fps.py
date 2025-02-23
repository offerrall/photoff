from time import perf_counter
from photoff import RGBA, CudaImage
from photoff.operations.filters import apply_stroke
from photoff.io import load_image, save_image

def measure_stroke_fps(input_path="./test/logo.png",
                       output_path="./test/stroke_logo.png",
                       stroke_width=4,
                       stroke_color=RGBA(0, 255, 0, 255),
                       iterations=100):
    """
    Carga la imagen de 'input_path', aplica el filtro stroke 'iterations' veces,
    mide el FPS y guarda el resultado en 'output_path'.
    """
    # Cargar imagen desde archivo (se asume que load_image retorna un objeto CudaImage)
    cuda_image = load_image(input_path)
    
    start_time = perf_counter()
    for _ in range(iterations):
        apply_stroke(cuda_image, stroke_width, stroke_color)
    end_time = perf_counter()
    
    elapsed_time = end_time - start_time
    fps = iterations / elapsed_time if elapsed_time > 0 else float('inf')
    
    # Guardar la imagen resultante
    save_image(cuda_image, output_path)
    
    print(f"Completed {iterations} stroke operations in {elapsed_time:.2f} seconds.")
    print(f"Stroke FPS: {fps:.2f}")
    
    cuda_image.free()
    return fps, elapsed_time

if __name__ == "__main__":
    measure_stroke_fps()
