from photoff.operations.resize import crop_margins
from photoff.io import save_image, load_image
from photoff import CudaImage
from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi

def crop_margins_ui(image: Annotated[str, fileUi] = "./assets/stock.jpg",
                    left: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                    top: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                    right: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                    bottom: Annotated[int, intUi(min_value=0, max_value=500)] = 0
                    ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/crop_margins_test.png"
    
    src_image = load_image(image)
    
    max_width = src_image.width - 1
    max_height = src_image.height - 1
    
    left = min(left, max_width - right)
    right = min(right, max_width - left)
    top = min(top, max_height - bottom)
    bottom = min(bottom, max_height - top)
    
    result = crop_margins(src_image, left, top, right, bottom)
    
    save_image(result, path)
    
    src_image.free()
    result.free()
    
    return path

App(crop_margins_ui)