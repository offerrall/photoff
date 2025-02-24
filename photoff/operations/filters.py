from ..core import _lib
from ..core.types import CudaImage, RGBA

def apply_corner_radius(image: CudaImage, size: int) -> None:

    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)

def apply_stroke(src_image: CudaImage,
                 src_copy_image: CudaImage,
                 stroke_width: int,
                 stroke_color: RGBA,
                 inner: bool = False) -> None:

    _lib.apply_stroke(src_image.buffer, src_copy_image.buffer,
                      src_image.width, src_image.height,
                      stroke_width, stroke_color.r, stroke_color.g,
                      stroke_color.b, stroke_color.a, int(inner))

def apply_shadow(src_image: CudaImage,
                 src_copy_image: CudaImage,
                 radius: float,
                 intensity: float,
                 shadow_color: RGBA,
                 inner: bool = False) -> None:
    
    _lib.apply_shadow(src_image.buffer, src_copy_image.buffer,
                    src_image.width, src_image.height,
                    radius, intensity, shadow_color.r,
                    shadow_color.g, shadow_color.b, shadow_color.a, int(inner))


def apply_opacity(image: CudaImage, opacity: float) -> None:
    
    _lib.apply_opacity(image.buffer, image.width, image.height, opacity)

