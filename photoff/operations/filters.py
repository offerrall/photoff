from ..core import _lib
from ..core.types import CudaImage, RGBA

def apply_corner_radius(image: CudaImage, size: int) -> None:
    
    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)

def apply_stroke(image: CudaImage, stroke_width: int, stroke_color: RGBA) -> None:
    
    _lib.apply_stroke(image.buffer, image.width, image.height,
                      stroke_width, stroke_color.r, stroke_color.g,
                      stroke_color.b, stroke_color.a)