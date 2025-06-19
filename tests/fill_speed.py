from time import time
from photoff import CudaImage, RGBA
from PIL import Image, ImageDraw, ImageChops
from photoff.operations.fill import fill_color, fill_gradient

def fill_operations_speed_test():
    width, height = 1920, 1080
    color1 = RGBA(0, 0, 255, 255)
    color2 = RGBA(255, 255, 0, 255)

    results = []

    # -------- fill_color ----------
    img_fill = CudaImage(width, height, RGBA)
    start = time()
    for _ in range(100):
        fill_color(img_fill, color1)
    fps_fill = 100 / (time() - start)
    results.append(("fill_color", fps_fill, None))

    # --- Pillow approx. for fill_color ---
    pil_img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(pil_img)
    start = time()
    for _ in range(100):
        draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 255, 255))
    fps_fill_pillow = 100 / (time() - start)
    results[0] = (results[0][0], fps_fill, fps_fill_pillow)

    # -------- fill_gradient ----------
    img_grad = CudaImage(width, height, RGBA)
    start = time()
    for _ in range(100):
        fill_gradient(img_grad, color1, color2, direction=0)
    fps_grad = 100 / (time() - start)
    results.append(("fill_gradient", fps_grad, None))

    # --- Pillow approx. for fill_gradient (vertical linear gradient) ---
    grad = Image.linear_gradient("L").resize((width, height))
    gradient_img = Image.merge("RGBA", [grad, grad, grad, Image.new("L", grad.size, 255)])
    start = time()
    for _ in range(100):
        ImageChops.add(gradient_img, gradient_img)  # simulate simple gradient load and blend
    fps_grad_pillow = 100 / (time() - start)
    results[1] = (results[1][0], fps_grad, fps_grad_pillow)

    print("\Fill Performance Comparison (FPS & Speedup vs Pillow)")
    print("-" * 90)
    print(f"{'Operation':<14} | {'PhotoFF (GPU)':>16} | {'Pillow (CPU)':>14} | {'Speedup ×':>12}")
    print("-" * 90)
    for name, gpu_fps, cpu_fps in results:
        speedup = gpu_fps / cpu_fps if cpu_fps else 0
        print(f"{name:<14} | {gpu_fps:16.2f} | {cpu_fps:14.2f} | {speedup:12.2f}")
    print("-" * 90)

if __name__ == "__main__":
    fill_operations_speed_test()
