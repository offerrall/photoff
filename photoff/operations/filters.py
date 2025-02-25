from ..core import _lib
from ..core.types import CudaImage, RGBA

def apply_corner_radius(image: CudaImage, size: int) -> None:

    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)

def apply_opacity(image: CudaImage, opacity: float) -> None:
    
    _lib.apply_opacity(image.buffer, image.width, image.height, opacity)

def apply_flip(image: CudaImage,
               flip_horizontal: bool = False,
               flip_vertical: bool = False) -> None:

    if flip_horizontal and flip_vertical:
        raise ValueError("Cannot flip both horizontal and vertical at the same time")

    _lib.apply_flip(image.buffer,
                    image.width,
                    image.height,
                    flip_horizontal,
                    flip_vertical)
