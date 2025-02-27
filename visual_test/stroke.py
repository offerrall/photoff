from photoff.operations.filters import apply_stroke
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi

def stroke_ui(image: Annotated[str, fileUi] = "./assets/logo.png",
              stroke_width: Annotated[int, intUi(min_value=1, max_value=50)] = 10,
              stroke_color: tuple[int, int, int, int] = (255, 0, 0, 255),
              inner: bool = True
              ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/stroke_test.png"
    src_image = load_image(image)
    
    apply_stroke(src_image, stroke_width, RGBA(*stroke_color), image_copy_cache=None, inner=inner)
    
    save_image(src_image, path)
    src_image.free()
    return path

App(stroke_ui)
