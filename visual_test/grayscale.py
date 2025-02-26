from photoff.operations.filters import apply_grayscale
from photoff.io import save_image, load_image
from photoff import CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, fileUi


def grayscale_ui(image: Annotated[str, fileUi] = "./assets/stock.jpg") -> Annotated[str, imageFileReturn]:

    path = "./assets/grayscale_test.png"
    src_image = load_image(image)
    
    apply_grayscale(src_image)
    save_image(src_image, path)
    src_image.free()
    
    return path


App(grayscale_ui)