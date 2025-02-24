from photoff.operations.filters import apply_flip
from photoff.operations.fill import fill_color
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, fileUi

def flip_ui(image: Annotated[str, fileUi] = "./visual_test/logo.png",
            flip_horizontal: bool = False,
            flip_vertical: bool = False) -> Annotated[str, imageFileReturn]:
    
    path = "./visual_test/flip_test.png"
    src_image = load_image(image)
    
    apply_flip(src_image, flip_horizontal, flip_vertical)
    save_image(src_image, path)
    src_image.free()
    
    return path

App(flip_ui)