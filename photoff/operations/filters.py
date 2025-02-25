from ..core import _lib
from ..core.types import CudaImage, RGBA
from ..core.buffer import copy_buffers_same_size

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

def apply_stroke(image: CudaImage,
                 stroke_width: int,
                 stroke_color: RGBA,
                 image_copy_cache: CudaImage = None,
                 inner: bool = False) -> None:
    
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image.buffer, image_copy_cache.buffer, image.width, image.height)
    else:
        if image_copy_cache.width != image.width or image_copy_cache.height != image.height:
            raise ValueError(f"Destination image dimensions must match original image dimensions: {image.width}x{image.height}, got {image_copy_cache.width}x{image_copy_cache.height}")

    _lib.apply_stroke(image.buffer,
                      image_copy_cache.buffer,
                      image.width,
                      image.height,
                      stroke_width,
                      stroke_color.r,
                      stroke_color.g,
                      stroke_color.b,
                      stroke_color.a,
                      int(inner))
    