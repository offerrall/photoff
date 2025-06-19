from time import time
from photoff import CudaImage, RGBA
from photoff.operations.fill import fill_color
from PIL import Image
from photoff.operations.blend import blend

def blend_speed_test():
    width, height = 1920, 1080
    over_w, over_h = 256, 256
    pos_x, pos_y = 100, 100

    # Crear imágenes PhotoFF
    bg = CudaImage(width, height, RGBA)
    over = CudaImage(over_w, over_h, RGBA)
    fill_color(bg, RGBA(0, 0, 0, 255))      # fondo negro
    fill_color(over, RGBA(255, 0, 0, 128))  # semi-transparente rojo

    # --- PhotoFF (GPU) ---
    start = time()
    for _ in range(100):
        blend(bg, over, pos_x, pos_y)
    fps_photoff = 100 / (time() - start)

    # Crear imágenes PIL
    bg_pil = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    over_pil = Image.new("RGBA", (over_w, over_h), (255, 0, 0, 128))

    # --- PILLOW (CPU) ---
    start = time()
    for _ in range(100):
        composite = bg_pil.copy()
        composite.paste(over_pil, (pos_x, pos_y), over_pil)  # respetando alfa
    fps_pillow = 100 / (time() - start)


    print("\Blend Performance Comparison (FPS & Speedup vs Pillow)")
    print("-" * 70)
    print(f"{'Operation':<10} | {'PhotoFF (GPU)':>16} | {'Pillow (CPU)':>14} | {'Speedup ×':>12}")
    print("-" * 70)
    speedup = fps_photoff / fps_pillow if fps_pillow else 0
    print(f"{'blend':<10} | {fps_photoff:16.2f} | {fps_pillow:14.2f} | {speedup:12.2f}")
    print("-" * 70)

if __name__ == "__main__":
    blend_speed_test()