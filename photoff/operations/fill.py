from ..core import _lib
from ..core.types import CudaImage, RGBA

def fill_color(image: CudaImage, color: RGBA) -> None:

    _lib.fill_color(image.buffer, image.width, image.height, color.r, color.g, color.b, color.a)