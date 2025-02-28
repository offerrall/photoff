from enum import Enum
from ..core import _lib
from ..core.types import CudaImage


class ResizeMethod(Enum):
    BILINEAR = "bilinear"
    NEAREST = "nearest"
    BICUBIC = "bicubic"


def resize(
    image: CudaImage,
    width: int,
    height: int,
    method: ResizeMethod = ResizeMethod.BICUBIC,
    resize_image_cache: CudaImage = None,
) -> CudaImage:
    if resize_image_cache is None:
        result = CudaImage(width, height)
    else:
        if resize_image_cache.width != width or resize_image_cache.height != height:
            raise ValueError(
                f"Destination image dimensions must match resize dimensions: {width}x{height}, got {resize_image_cache.width}x{resize_image_cache.height}"
            )
        result = resize_image_cache

    if method == ResizeMethod.BILINEAR:
        _lib.resize_bilinear(result.buffer, image.buffer, width, height,
                             image.width, image.height)
    elif method == ResizeMethod.NEAREST:
        _lib.resize_nearest(result.buffer, image.buffer, width, height,
                            image.width, image.height)
    elif method == ResizeMethod.BICUBIC:
        _lib.resize_bicubic(result.buffer, image.buffer, width, height,
                            image.width, image.height)
    else:
        raise ValueError(f"Unsupported resize method: {method}")

    return result


def crop_margins(
    image: CudaImage,
    left: int = 0,
    top: int = 0,
    right: int = 0,
    bottom: int = 0,
    crop_image_cache: CudaImage = None,
) -> CudaImage:
    if left < 0 or top < 0 or right < 0 or bottom < 0:
        raise ValueError("Margins cannot be negative")

    if left + right >= image.width or top + bottom >= image.height:
        raise ValueError("Total margins exceed image dimensions")

    new_width = image.width - left - right
    new_height = image.height - top - bottom

    if crop_image_cache is None:
        result = CudaImage(new_width, new_height)
    else:
        if crop_image_cache.width != new_width or crop_image_cache.height != new_height:
            raise ValueError(
                f"Destination image cache dimensions must match crop result: {new_width}x{new_height}"
            )
        result = crop_image_cache

    _lib.crop_image(
        result.buffer,
        image.buffer,
        image.width,
        image.height,
        new_width,
        new_height,
        left,
        top,
    )

    return result
