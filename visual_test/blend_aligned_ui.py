from photoff.operations.utils import blend_aligned
from photoff.operations.fill import fill_color
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi, listUi, colorUi

def blend_aligned_ui(
    image: Annotated[str, fileUi] = "./assets/stock.jpg",
    canvas_width: Annotated[int, intUi(min_value=100, max_value=1920)] = 800,
    canvas_height: Annotated[int, intUi(min_value=100, max_value=1080)] = 600,
    canvas_color: Annotated[tuple[int, int, int, int], colorUi] = (255, 255, 255, 255),
    alignment: Annotated[str, listUi(values=[
        "center", "top", "bottom", "left", "right", 
        "top-left", "top-right", "bottom-left", "bottom-right"
    ])] = "center",
    offset_x: Annotated[int, intUi(max_value=500)] = 0,
    offset_y: Annotated[int, intUi(max_value=500)] = 0
) -> Annotated[str, imageFileReturn]:

    path = "./assets/blend_aligned_test.png"
    
    # Load source image
    source = load_image(image)
    
    # Create canvas with specified color
    canvas = CudaImage(canvas_width, canvas_height)
    fill_color(canvas, RGBA(*canvas_color))
    
    # Apply aligned blend
    blend_aligned(canvas, source, alignment, offset_x, offset_y)
    
    save_image(canvas, path)
    source.free()
    canvas.free()
    
    return path

App(blend_aligned_ui)