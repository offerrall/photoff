from time import time
from photoff import CudaImage, RGBA
from photoff.operations.resize import ResizeMethod, resize
from photoff.operations.fill import fill_color
from PIL import Image

def resize_speed_test():
    image = CudaImage(1920, 1080, RGBA)
    fill_color(image, RGBA(255, 0, 0, 255))

    photoff_methods = [
        ("NEAREST",  ResizeMethod.NEAREST),
        ("BILINEAR", ResizeMethod.BILINEAR),
        ("BICUBIC",  ResizeMethod.BICUBIC),
    ]

    results = []

    # --- PhotoFF without cache ---
    for name, method in photoff_methods:
        start = time()
        for _ in range(100):
            resize(image, 1280, 720, method=method)
        fps = 100 / (time() - start)
        results.append((name, fps, None, None))  # Placeholder for now

    # --- PhotoFF with cache ---
    cache_img = CudaImage(1280, 720, RGBA)
    fill_color(cache_img, RGBA(0, 255, 0, 255))
    for i, (name, method) in enumerate(photoff_methods):
        start = time()
        for _ in range(100):
            resize(image, 1280, 720, method=method, resize_image_cache=cache_img)
        fps = 100 / (time() - start)
        old = results[i]
        results[i] = (old[0], old[1], fps, None)

    # --- PILLOW (CPU) ---
    pil_img = Image.new("RGBA", (1920, 1080), (255, 0, 0, 255))
    pillow_methods = [
        ("NEAREST",  Image.Resampling.NEAREST),
        ("BILINEAR", Image.Resampling.BILINEAR),
        ("BICUBIC",  Image.Resampling.BICUBIC),
    ]
    for i, (name, resample) in enumerate(pillow_methods):
        start = time()
        for _ in range(100):
            pil_img.resize((1280, 720), resample=resample)
        fps = 100 / (time() - start)
        old = results[i]
        results[i] = (old[0], old[1], old[2], fps)

    # --- Print final table ---
    print("Resize Performance Comparison (FPS & Speedup vs Pillow)")
    print(f"To 1920x1080 → 1280x720")
    print("-" * 100)
    print(f"{'Method':<10} | {'PhotoFF (no cache)':>18} | {'PhotoFF (cache)':>16} | {'Pillow':>10} | {'No cache ×':>12} | {'Cache ×':>9}")
    print("-" * 100)
    for name, no_cache, with_cache, pillow in results:
        speedup_no_cache = no_cache / pillow if pillow else 0
        speedup_cache = with_cache / pillow if pillow else 0
        print(f"{name:<10} | {no_cache:18.2f} | {with_cache:16.2f} | {pillow:10.2f} | {speedup_no_cache:12.2f} | {speedup_cache:9.2f}")
    print("-" * 100)

if __name__ == "__main__":
    resize_speed_test()