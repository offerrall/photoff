from photoff.api import load_image
from photoff.types import CudaImage

from time import perf_counter

start_time = perf_counter()
test = CudaImage(1, 1)
end_time = perf_counter()
print("Elapsed time with test:", end_time - start_time)

start_time = perf_counter()
cuda_img = load_image("input.png")
end_time = perf_counter()
print("Elapsed time without preallocated memory:", end_time - start_time)

start_time = perf_counter()
cuda_img2 = load_image("input.png")
end_time = perf_counter()
print("Elapsed time without preallocated memory:", end_time - start_time)

cuda_img3 = CudaImage(1920, 1080)

start_time = perf_counter()
cuda_img3 = load_image("input.png", cuda_img3)
end_time = perf_counter()
print("Elapsed time with preallocated memory:", end_time - start_time)


print(cuda_img.buffer, cuda_img2.buffer, cuda_img3.buffer)
