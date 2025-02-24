from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_opacity
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn


def apply_opacity_ui(opacity: float = 0.5) -> Annotated[str, imageFileReturn]:

    path = "./visual_test/fill_color.png"
    image = CudaImage(1920, 1080)

    fill_color(image, RGBA(*(255, 0, 0, 255)))
    apply_opacity(image, opacity)
    save_image(image, path)
    image.free()

    return path




App(apply_opacity_ui)