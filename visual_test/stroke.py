from photoff.operations.filters import apply_stroke

from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi

def corner_border_ui(image: Annotated[str, fileUi] = "./visual_test/logo.png",
                     stroke_width: Annotated[int, intUi(min_value=1, max_value=200)] = 5,
                     stroke_color: tuple[int, int, int, int] = (0, 255, 0, 255),
                     inner: bool = False
                     ) -> Annotated[str, imageFileReturn]:
    
    path = "./visual_test/stroke_test.png"
    image = load_image(image)

    apply_stroke(image, stroke_width, RGBA(*stroke_color), inner)
    
    save_image(image, path)
    image.free()

    return path

App(corner_border_ui)
