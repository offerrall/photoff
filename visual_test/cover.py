# Start file 'C:/Users/offer/Desktop/photoff/visual_test/cover_container.py'
from photoff.core.types import CudaImage
from photoff.operations.utils import cover_image_in_container
from photoff.io import load_image, save_image
from photoff import RGBA
from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi

def cover_container_ui(
    image: Annotated[str, fileUi] = "./assets/stock.jpg",
    container_width: Annotated[int, intUi(min_value=1, max_value=3000)] = 800,
    container_height: Annotated[int, intUi(min_value=1, max_value=3000)] = 600,
) -> Annotated[str, imageFileReturn]:
    path = "./assets/cover_container_test.png"
    
    src_image = load_image(image)
    result = cover_image_in_container(src_image, container_width, container_height, 0, 0, RGBA(255, 255, 255, 255))
    
    save_image(result, path)
    src_image.free()
    result.free()
    
    return path

App(cover_container_ui)