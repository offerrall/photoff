from ..core import _lib
from ..core.types import CudaImage, RGBA

def apply_corner_radius(image: CudaImage, size: int) -> None:

    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)

def apply_stroke(src_image: CudaImage,
                 stroke_width: int,
                 stroke_color: RGBA,
                 inner: bool = False,
                 src_copy_image: CudaImage = None,
                 ) -> None:
    
    need_free = False
    if src_copy_image is None:
        src_copy_image = src_image.copy()
        need_free = True
    else:
        if src_copy_image.width != src_image.width or src_copy_image.height != src_image.height:
            raise ValueError(f"Destination image dimensions must match source dimensions:
                             {src_image.width}x{src_image.height}, got {src_copy_image.width}x{src_copy_image.height}")

    _lib.apply_stroke(src_image.buffer, src_copy_image.buffer,
                      src_image.width, src_image.height,
                      stroke_width, stroke_color.r, stroke_color.g,
                      stroke_color.b, stroke_color.a, int(inner))
    
    if need_free:
        tmp_image = src_image.buffer
        src_image.buffer = src_copy_image.buffer
        src_copy_image.buffer = tmp_image
        src_copy_image.free()

def apply_shadow(src_image: CudaImage,
                 radius: float,
                 intensity: float,
                 shadow_color: RGBA,
                 inner: bool = False,
                 src_copy_image: CudaImage = None,
                 ) -> None:
    
    need_free = False
    if src_copy_image is None:
        src_copy_image = src_image.copy()
        need_free = True
    else:
        if src_copy_image.width != src_image.width or src_copy_image.height != src_image.height:
            raise ValueError(f"Destination image dimensions must match source dimensions:
                             {src_image.width}x{src_image.height}, got {src_copy_image.width}x{src_copy_image.height}")
    
    _lib.apply_shadow(src_image.buffer, src_copy_image.buffer,
                    src_image.width, src_image.height,
                    radius, intensity, shadow_color.r,
                    shadow_color.g, shadow_color.b, shadow_color.a, int(inner))

    if need_free:
        tmp_image = src_image.buffer
        src_image.buffer = src_copy_image.buffer
        src_copy_image.buffer = tmp_image
        src_copy_image.free()


def apply_opacity(image: CudaImage, opacity: float) -> None:
    
    _lib.apply_opacity(image.buffer, image.width, image.height, opacity)

def apply_flip(image: CudaImage,
               flip_horizontal: bool = False,
               flip_vertical: bool = False) -> None:

    _lib.apply_flip(image.buffer,
                    image.width,
                    image.height,
                    flip_horizontal,
                    flip_vertical)