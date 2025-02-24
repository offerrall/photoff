from photoff.operations.filters import apply_stroke
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi

def corner_border_ui(image: Annotated[str, fileUi] = "./assets/logo.png",
                    stroke_width: Annotated[int, intUi(min_value=1, max_value=200)] = 5,
                    stroke_color: tuple[int, int, int, int] = (0, 255, 0, 255),
                    inner: bool = False
                    ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/stroke_test.png"
    src_image = load_image(image)
    image_size = (src_image.width, src_image.height)
    
    dst_image = src_image.copy()
    
    apply_stroke(src_image, dst_image, stroke_width, RGBA(*stroke_color), inner)    
    save_image(dst_image, path)
    
    src_image.free()
    dst_image.free()

    return path

App(corner_border_ui)