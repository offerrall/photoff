from photoff.operations.filters import apply_shadow
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage
from typing import Annotated
from functogui import App, imageFileReturn, intUi, floatUi, fileUi

def shadow_ui(image: Annotated[str, fileUi] = "./visual_test/logo.png",
              radius: Annotated[float, floatUi(min_value=1.0, max_value=100.0)] = 10.0,
              intensity: Annotated[float, floatUi(min_value=0.0, max_value=1.0)] = 0.5,
              shadow_color: tuple[int, int, int, int] = (0, 0, 0, 128),
              inner: bool = False
              ) -> Annotated[str, imageFileReturn]:
    
    path = "./visual_test/shadow_test.png"
    src_image = load_image(image)
    image_size = (src_image.width, src_image.height)
    
    dst_image = CudaImage(*image_size)
    
    apply_shadow(src_image, dst_image, radius, intensity, RGBA(*shadow_color), inner)
    save_image(dst_image, path)
    
    src_image.free()
    dst_image.free()
    
    return path

App(shadow_ui)