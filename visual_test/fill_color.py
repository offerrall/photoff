from photoff.operations.fill import fill_color
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn


def fill_color_ui(
    color: tuple[int, int, int, int] = (255, 0, 0, 255),
) -> Annotated[str, imageFileReturn]:
    path = "./assets/fill_color.png"
    image = CudaImage(1920, 1080)

    fill_color(image, RGBA(*color))
    save_image(image, path)
    image.free()

    return path


App(fill_color_ui)
