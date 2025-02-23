from photoff.io import save_image
from photoff import CudaImage, RGBA
from photoff.operations.fill import fill_color

from time import perf_counter

cuda_img = CudaImage(1920, 1080)

fill_color(cuda_img, RGBA(0, 128, 128, 12))


start_time = perf_counter()
save_image(cuda_img, "output.png")
end_time = perf_counter()
print("Elapsed time:", end_time - start_time)