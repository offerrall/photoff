from photoff.operations.blend import blend
from photoff.operations.fill import fill_color
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi


def blend_ui(color1: tuple[int, int, int, int] = (255, 0, 0, 255),
             color2: tuple[int, int, int, int] = (0, 255, 0, 128),
             color2_height: Annotated[int, intUi(min_value=1, max_value=1080)] = 300,
             color2_width: Annotated[int, intUi(min_value=1, max_value=1920)] = 300,
             x: Annotated[int, intUi(min_value=0, max_value=1920)] = 0,
             y: Annotated[int, intUi(min_value=0, max_value=1080)] = 0
             ) -> Annotated[str, imageFileReturn]:

    path = "./assets/blend.png"
    image1 = CudaImage(1920, 1080)
    image2 = CudaImage(color2_width, color2_height)

    fill_color(image1, RGBA(*color1))
    fill_color(image2, RGBA(*color2))

    blend(image1, image2, x, y)
    save_image(image1, path)
    image1.free()
    image2.free()

    return path




App(blend_ui)