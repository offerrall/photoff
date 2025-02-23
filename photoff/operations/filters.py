from ..core import _lib
from ..core.types import CudaImage

def apply_corner_radius(image: CudaImage, size: int) -> None:
    
    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)