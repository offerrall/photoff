from photoff.operations.filters import apply_chroma_key, apply_corner_radius
from photoff.operations.fill import fill_color
from photoff.operations.utils import blend_aligned
from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi, listUi

def chroma_key_ui(
                key_color: tuple[int, int, int, int] = (0, 255, 0, 255),  # Verde por defecto
                corner_radius: Annotated[int, intUi(min_value=0, max_value=200)] = 50,
                channel: Annotated[str, listUi(values=["R", "G", "B", "A"])] = "G",
                threshold: Annotated[int, intUi(min_value=0, max_value=255)] = 128,
                invert: bool = False,
                zero_all_channels: bool = False
    ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/chroma_key_test.png"
    
    background = CudaImage(800, 600)
    fill_color(background, RGBA(50, 50, 150, 255))
    
    key_image = CudaImage(400, 300)
    fill_color(key_image, RGBA(*key_color))
    apply_corner_radius(key_image, corner_radius)
    
    target_image = CudaImage(400, 300)
    fill_color(target_image, RGBA(255, 128, 0, 255))
    
    apply_chroma_key(
        target_image, 
        key_image, 
        channel=channel, 
        threshold=threshold, 
        invert=invert,
        zero_all_channels=zero_all_channels
    )
    
    blend_aligned(background, key_image, align="top-left", offset_x=50, offset_y=50)
    blend_aligned(background, target_image, align="bottom-right", offset_x=-50, offset_y=-50)
    
    save_image(background, path)
    
    background.free()
    key_image.free()
    target_image.free()
    
    return path

App(chroma_key_ui)