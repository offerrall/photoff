from photoff.operations.composite import blend_padding
from photoff.operations.fill import fill_color
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi, colorUi

def blend_padding_ui(
    color1: Annotated[tuple[int, int, int, int], colorUi] = (255, 0, 0, 255),
    image_width: Annotated[int, intUi(min_value=50, max_value=800)] = 400,
    image_height: Annotated[int, intUi(min_value=50, max_value=600)] = 300,
    padding: Annotated[int, intUi(min_value=0, max_value=100)] = 20,
    bg_color: Annotated[tuple[int, int, int, int], colorUi] = (0, 0, 0, 255)
) -> Annotated[str, imageFileReturn]:

    path = "./assets/blend_padding_test.png"
    
    # Create source image with specified color
    source = CudaImage(image_width, image_height)
    fill_color(source, RGBA(*color1))
    
    # Create background for padding with transparent or specified color
    background = CudaImage(image_width + padding*2, image_height + padding*2)
    fill_color(background, RGBA(*bg_color))
    
    # Apply padding
    result = blend_padding(source, padding, background)
    
    save_image(result, path)
    source.free()
    
    # Don't free the result since it's the same as background
    return path

App(blend_padding_ui)