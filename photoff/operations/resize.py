from enum import Enum
from ..core import _lib
from ..core.types import CudaImage

class ResizeMethod(Enum):
    BILINEAR = "bilinear"
    NEAREST = "nearest"
    BICUBIC = "bicubic"

def resize(image: CudaImage, 
           width: int, 
           height: int, 
           method: ResizeMethod = ResizeMethod.BICUBIC
           ) -> CudaImage:
  
    result = CudaImage(width, height)
    
    if method == ResizeMethod.BILINEAR:
        _lib.resize_bilinear(
            result.buffer,
            image.buffer,
            width,
            height,
            image.width,
            image.height
        )
    elif method == ResizeMethod.NEAREST:
        _lib.resize_nearest(
            result.buffer,
            image.buffer,
            width,
            height,
            image.width,
            image.height
        )
    elif method == ResizeMethod.BICUBIC:
        _lib.resize_bicubic(
            result.buffer,
            image.buffer,
            width,
            height,
            image.width,
            image.height
        )
    else:
        raise ValueError(f"Unsupported resize method: {method}")
        
    return result