import time
from PIL import Image, ImageFilter
from photoff.io import load_image, save_image
from photoff.operations.resize import resize, ResizeMethod
from photoff.operations.filters import apply_gaussian_blur, apply_grayscale
from photoff.core.types import CudaImage

def test_photoff_resize(image_path, width, height, iterations=10, use_cache=False):
    """Tests the performance of photoff's resize function with and without cache."""
    try:
        cuda_image = load_image(image_path)
        cache = CudaImage(width, height) if use_cache else None
        start_time = time.perf_counter()
        for _ in range(iterations):
            resized_cuda = resize(cuda_image, width, height, method=ResizeMethod.BICUBIC, resize_image_cache=cache)
            if not use_cache:
                resized_cuda.free()
        end_time = time.perf_counter()
        cuda_image.free()
        if use_cache:
            cache.free()
        average_time = (end_time - start_time) / iterations
        cache_str = "with cache" if use_cache else "without cache"
        print(f"PhotoFF Resize ({width}x{height}) {cache_str}: {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during PhotoFF resize test ({cache_str}): {e}")
        return float('inf')

def test_pillow_resize(image_path, width, height, iterations=10):
    """Tests the performance of Pillow's resize function."""
    try:
        pil_image = Image.open(image_path).convert("RGBA")
        start_time = time.perf_counter()
        for _ in range(iterations):
            resized_pil = pil_image.resize((width, height), Image.Resampling.BICUBIC)
        end_time = time.perf_counter()
        average_time = (end_time - start_time) / iterations
        print(f"Pillow Resize ({width}x{height}): {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during Pillow resize test: {e}")
        return float('inf')

def test_photoff_gaussian_blur(image_path, radius, iterations=10, use_cache=False):
    """Tests the performance of photoff's gaussian blur with and without cache."""
    try:
        cuda_image = load_image(image_path)
        cache = CudaImage(cuda_image.width, cuda_image.height) if use_cache else None
        start_time = time.perf_counter()
        for _ in range(iterations):
            apply_gaussian_blur(cuda_image, radius=radius, image_copy_cache=cache)
        end_time = time.perf_counter()
        cuda_image.free()
        if use_cache:
            cache.free()
        average_time = (end_time - start_time) / iterations
        cache_str = "with cache" if use_cache else "without cache"
        print(f"PhotoFF Gaussian Blur (radius={radius}) {cache_str}: {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during PhotoFF gaussian blur test ({cache_str}): {e}")
        return float('inf')

def test_pillow_gaussian_blur(image_path, radius, iterations=10):
    """Tests the performance of Pillow's gaussian blur."""
    try:
        pil_image = Image.open(image_path).convert("RGBA")
        start_time = time.perf_counter()
        for _ in range(iterations):
            blurred_pil = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
        end_time = time.perf_counter()
        average_time = (end_time - start_time) / iterations
        print(f"Pillow Gaussian Blur (radius={radius}): {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during Pillow gaussian blur test: {e}")
        return float('inf')

def test_photoff_grayscale(image_path, iterations=10):
    """Tests the performance of photoff's grayscale function."""
    try:
        cuda_image = load_image(image_path)
        start_time = time.perf_counter()
        for _ in range(iterations):
            apply_grayscale(cuda_image)
        end_time = time.perf_counter()
        cuda_image.free()
        average_time = (end_time - start_time) / iterations
        print(f"PhotoFF Grayscale: {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during PhotoFF grayscale test: {e}")
        return float('inf')

def test_pillow_grayscale(image_path, iterations=10):
    """Tests the performance of Pillow's grayscale conversion."""
    try:
        pil_image = Image.open(image_path).convert("RGBA")
        start_time = time.perf_counter()
        for _ in range(iterations):
            grayscale_pil = pil_image.convert("L") # 'L' mode for grayscale
        end_time = time.perf_counter()
        average_time = (end_time - start_time) / iterations
        print(f"Pillow Grayscale: {average_time:.6f} seconds (average of {iterations} iterations)")
        return average_time
    except Exception as e:
        print(f"Error during Pillow grayscale test: {e}")
        return float('inf')

if __name__ == "__main__":
    # Create a dummy image for testing if one doesn't exist
    dummy_image_path = "test_image.png"
    try:
        Image.open(dummy_image_path)
    except FileNotFoundError:
        dummy_image = Image.new('RGBA', (3840, 2160), color = 'red')
        dummy_image.save(dummy_image_path)

    test_width = 3840
    test_height = 2160
    gaussian_radius = 5
    num_iterations = 20

    print("Starting performance comparison between PhotoFF and Pillow:")
    print("-" * 60)

    # Resize tests
    photoff_resize_no_cache = test_photoff_resize(dummy_image_path, test_width, test_height, num_iterations, use_cache=False)
    photoff_resize_cached = test_photoff_resize(dummy_image_path, test_width, test_height, num_iterations, use_cache=True)
    pillow_resize = test_pillow_resize(dummy_image_path, test_width, test_height, num_iterations)

    print("-" * 60)

    # Gaussian Blur tests
    photoff_blur_no_cache = test_photoff_gaussian_blur(dummy_image_path, gaussian_radius, num_iterations, use_cache=False)
    photoff_blur_cached = test_photoff_gaussian_blur(dummy_image_path, gaussian_radius, num_iterations, use_cache=True)
    pillow_blur = test_pillow_gaussian_blur(dummy_image_path, gaussian_radius, num_iterations)

    print("-" * 60)

    # Grayscale tests
    photoff_grayscale = test_photoff_grayscale(dummy_image_path, num_iterations)
    pillow_grayscale = test_pillow_grayscale(dummy_image_path, num_iterations)

    print("-" * 60)
    print("Performance Comparison Summary:")
    print("-" * 60)

    if photoff_resize_no_cache != float('inf') and pillow_resize != float('inf'):
        speedup_resize_no_cache = pillow_resize / photoff_resize_no_cache
        print(f"Resize (without cache): PhotoFF was {speedup_resize_no_cache:.2f} times faster than Pillow.")

    if photoff_resize_cached != float('inf') and pillow_resize != float('inf'):
        speedup_resize_cached = pillow_resize / photoff_resize_cached
        print(f"Resize (with cache): PhotoFF was {speedup_resize_cached:.2f} times faster than Pillow.")
    if photoff_blur_no_cache != float('inf') and pillow_blur != float('inf'):
        speedup_blur_no_cache = pillow_blur / photoff_blur_no_cache
        print(f"Gaussian Blur (without cache): PhotoFF was {speedup_blur_no_cache:.2f} times faster than Pillow.")