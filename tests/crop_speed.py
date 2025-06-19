from time import time
from photoff import CudaImage, RGBA
from photoff.operations.fill import fill_color
from photoff.operations.resize import crop_margins
from PIL import Image

def crop_speed_test():
    width, height = 1920, 1080
    crop_left, crop_top, crop_right, crop_bottom = 100, 50, 100, 50
    new_width = width - crop_left - crop_right
    new_height = height - crop_top - crop_bottom

    image = CudaImage(width, height, RGBA)
    fill_color(image, RGBA(255, 0, 0, 255))

    results = []

    # --- PhotoFF without cache ---
    start = time()
    for _ in range(100):
        crop_margins(image, left=crop_left, top=crop_top, right=crop_right, bottom=crop_bottom)
    fps_no_cache = 100 / (time() - start)
    results.append(("crop_margins", fps_no_cache, None, None))

    # --- PhotoFF with cache ---
    crop_cache = CudaImage(new_width, new_height, RGBA)
    start = time()
    for _ in range(100):
        crop_margins(image, left=crop_left, top=crop_top, right=crop_right, bottom=crop_bottom, crop_image_cache=crop_cache)
    fps_cache = 100 / (time() - start)
    results[0] = (results[0][0], fps_no_cache, fps_cache, None)

    # --- PILLOW (CPU) ---
    pil_img = Image.new("RGBA", (width, height), (255, 0, 0, 255))
    box = (crop_left, crop_top, width - crop_right, height - crop_bottom)
    start = time()
    for _ in range(100):
        pil_img.crop(box)
    fps_pillow = 100 / (time() - start)
    results[0] = (results[0][0], fps_no_cache, fps_cache, fps_pillow)

    # --- Print final table ---
    print("Crop Performance Comparison (FPS & Speedup vs Pillow)")
    print(f"From 1920x1080 → {new_width}x{new_height}")
    print("-" * 90)
    print(f"{'Method':<14} | {'PhotoFF (no cache)':>18} | {'PhotoFF (cache)':>16} | {'Pillow':>10} | {'No cache ×':>12} | {'Cache ×':>9}")
    print("-" * 90)
    for name, no_cache, with_cache, pillow in results:
        speedup_no_cache = no_cache / pillow if pillow else 0
        speedup_cache = with_cache / pillow if pillow else 0
        print(f"{name:<14} | {no_cache:18.2f} | {with_cache:16.2f} | {pillow:10.2f} | {speedup_no_cache:12.2f} | {speedup_cache:9.2f}")
    print("-" * 90)

if __name__ == "__main__":
    crop_speed_test()
