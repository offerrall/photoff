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
        if dst_image.width != width or dst_image.height != height:
            raise ValueError(f"Destination image dimensions must match resize dimensions: {width}x{height}, got {dst_image.width}x{dst_image.height}")
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

def crop_margins(src_image: CudaImage, 
                 left: int = 0, 
                 top: int = 0, 
                 right: int = 0, 
                 bottom: int = 0,
                 dst_image: CudaImage = None) -> CudaImage:

    if left < 0 or top < 0 or right < 0 or bottom < 0:
        raise ValueError("Margins cannot be negative")
        
    if left + right >= src_image.width or top + bottom >= src_image.height:
        raise ValueError("Total margins exceed image dimensions")
    
    new_width = src_image.width - left - right
    new_height = src_image.height - top - bottom
    
    if dst_image is None:
        result = CudaImage(new_width, new_height)
    else:
        if dst_image.width != new_width or dst_image.height != new_height:
            raise ValueError(f"Destination image dimensions must match crop result: {new_width}x{new_height}")
        result = dst_image
    
    _lib.crop_image(
        src_image.buffer,
        result.buffer,
        src_image.width,
        src_image.height,
        new_width,
        new_height,
        left,
        top
    )
    
    return result