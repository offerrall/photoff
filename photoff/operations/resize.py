from enum import Enum
from ..core import _lib
from ..core.types import CudaImage

class ResizeMethod(Enum):
    BILINEAR = "bilinear"
    NEAREST = "nearest"

def resize(image: CudaImage, 
           width: int, 
           height: int, 
           method: ResizeMethod = ResizeMethod.BILINEAR
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
    else:
        raise ValueError(f"Unknown or unsupported method: {method}")
        
    return result

def resize_bilinear(dst: CudaImage, src: CudaImage) -> None:
        
    _lib.resize_bilinear(
        dst.buffer,
        src.buffer,
        dst.width,
        dst.height,
        src.width,
        src.height
    )

def resize_nearest(dst: CudaImage, src: CudaImage) -> None:
        
    _lib.resize_nearest(
        dst.buffer,
        src.buffer,
        dst.width,
        dst.height,
        src.width,
        src.height
    )