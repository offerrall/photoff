from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import CudaImage
from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi

def gaussian_blur_ui(image: Annotated[str, fileUi] = "./assets/stock.jpg",
                     radius: Annotated[int, intUi(min_value=0, max_value=50)] = 5
                     ) -> Annotated[str, imageFileReturn]:

    path = "./assets/gaussian_blur_test.png"
    src_image = load_image(image)
    if radius == 0:
        radius = 0.1
    
    radius = float(radius)

    aux_buffer = CudaImage(src_image.width, src_image.height)
    apply_gaussian_blur(src_image, radius)
    apply_corner_radius(src_image, 200)
    save_image(src_image, path)
    
    src_image.free()
    aux_buffer.free()
    
    return path

App(gaussian_blur_ui)