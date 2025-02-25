from ..core import _lib
from ..core.types import CudaImage, RGBA

def fill_color(image: CudaImage, color: RGBA) -> None:
    _lib.fill_color(image.buffer, image.width, image.height, color.r, color.g, color.b, color.a)

def fill_gradient(image: CudaImage, color1: RGBA, color2: RGBA, direction: int, seamless: bool) -> None:
    _lib.fill_gradient(
        image.buffer,
        image.width,
        image.height,
        color1.r, color1.g, color1.b, color1.a,
        color2.r, color2.g, color2.b, color2.a,
        direction,
        seamless
    )
