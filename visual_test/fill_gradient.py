from photoff.operations.fill import fill_gradient
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, listUi

def fill_gradient_ui(color1: tuple[int, int, int, int] = (255, 0, 0, 255),
                     color2: tuple[int, int, int, int] = (0, 0, 255, 255),
                     direction: Annotated[str, listUi(values=["horizontal", "vertical", "diagonal", "radial"])] = "horizontal",
                     seamless: bool = False
                     ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/fill_gradient.png"
    image = CudaImage(5000, 5000) # Example for extra buffer space
    image.height = 1080
    image.width = 1920

    directions = {"horizontal": 0, "vertical": 1, "diagonal": 2, "radial": 3}
    dir_value = directions[direction]

    fill_gradient(image, RGBA(*color1), RGBA(*color2), dir_value, seamless)
    save_image(image, path)
    image.free()
    
    return path

App(fill_gradient_ui)
