from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_gaussian_blur, apply_corner_radius
from photoff.io import save_image, load_image
from photoff import CudaImage
from typing import Annotated
from functogui import App, imageFileReturn, intUi, floatUi, fileUi

def gaussian_blur_ui(image: Annotated[str, fileUi] = "./assets/stock.jpg",
                     radius: Annotated[float, floatUi(min_value=0.1, max_value=50.0)] = 5.0
                     ) -> Annotated[str, imageFileReturn]:

    path = "./assets/gaussian_blur_test.png"
    src_image = load_image(image)

    aux_buffer = CudaImage(src_image.width, src_image.height)
    apply_gaussian_blur(src_image, radius)
    save_image(src_image, path)
    
    src_image.free()
    aux_buffer.free()
    
    return path

App(gaussian_blur_ui)