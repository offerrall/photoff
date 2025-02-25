from photoff.operations.utils import cover_image_in_container
from photoff.operations.filters import apply_corner_radius
from photoff.io import load_image, save_image
from photoff import RGBA
from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi

def cover_container_ui(
    image: Annotated[str, fileUi] = "./assets/stock.jpg",
    container_width: Annotated[int, intUi(min_value=1, max_value=3000)] = 800,
    container_height: Annotated[int, intUi(min_value=1, max_value=3000)] = 600,
    offset_x: Annotated[int, intUi(min_value=-1000, max_value=1000)] = 0,
    offset_y: Annotated[int, intUi(min_value=-1000, max_value=1000)] = 0
) -> Annotated[str, imageFileReturn]:
    path = "./assets/cover_container_test.png"
    
    src_image = load_image(image)
    result = cover_image_in_container(src_image, container_width, container_height, offset_x, offset_y, RGBA(255, 255, 255, 255))
    apply_corner_radius(result, 50)
    save_image(result, path)
    src_image.free()
    result.free()
    
    return path

App(cover_container_ui)