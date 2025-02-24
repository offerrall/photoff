from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_corner_radius
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi

def corner_border_ui(color: tuple[int, int, int, int] = (255, 0, 0, 255),
                     border_size: Annotated[int, intUi(min_value=1, max_value=500)] = 500
                     ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/corner_border.png"
    image = CudaImage(1000, 1000)

    fill_color(image, RGBA(*color))
    apply_corner_radius(image, border_size)
    save_image(image, path)
    image.free()

    return path

App(corner_border_ui)