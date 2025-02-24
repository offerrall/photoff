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
           method: ResizeMethod = ResizeMethod.BICUBIC,
           dst_image: CudaImage = None
           ) -> CudaImage:
    
    if dst_image is None:
        result = CudaImage(width, height)
    else:
        result = dst_image
    
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