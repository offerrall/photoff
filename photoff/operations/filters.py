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
        raise ValueError(
            "Cannot flip both horizontal and vertical at the same time")

    _lib.apply_flip(image.buffer, image.width, image.height, flip_horizontal,
                    flip_vertical)


def apply_grayscale(image: CudaImage) -> None:
    _lib.apply_grayscale(image.buffer, image.width, image.height)


def apply_chroma_key(
    image: CudaImage,
    key_image: CudaImage,
    channel: str = "A",
    threshold: int = 128,
    invert: bool = False,
    zero_all_channels: bool = False,
) -> None:
    channel_upper = (channel.upper()
                     if isinstance(channel, str) else str(channel).upper())

    if channel_upper == "R":
        channel_idx = 0
    elif channel_upper == "G":
        channel_idx = 1
    elif channel_upper == "B":
        channel_idx = 2
    elif channel_upper == "A":
        channel_idx = 3
    else:
        raise ValueError(
            f"Invalid channel: {channel}, must be one of 'R', 'G', 'B', 'A'")

    _lib.apply_chroma_key(
        image.buffer,
        key_image.buffer,
        image.width,
        image.height,
        key_image.width,
        key_image.height,
        channel_idx,
        threshold,
        invert,
        zero_all_channels,
    )


def apply_stroke(
    image: CudaImage,
    stroke_width: int,
    stroke_color: RGBA,
    image_copy_cache: CudaImage = None,
    inner: bool = True,
) -> None:
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer,
                               image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width
                or image_copy_cache.height != image.height):
            raise ValueError(
                f"Destination image dimensions must match original image dimensions: {image.width}x{image.height}, got {image_copy_cache.width}x{image_copy_cache.height}"
            )

    _lib.apply_stroke(
        image.buffer,
        image_copy_cache.buffer,
        image.width,
        image.height,
        stroke_width,
        stroke_color.r,
        stroke_color.g,
        stroke_color.b,
        stroke_color.a,
        int(inner),
    )

    if need_free:
        image_copy_cache.free()


def apply_shadow(
    image: CudaImage,
    radius: float,
    intensity: float,
    shadow_color: RGBA,
    image_copy_cache: CudaImage = None,
    inner: bool = False,
) -> None:
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer,
                               image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width
                or image_copy_cache.height != image.height):
            raise ValueError(
                f"Destination image dimensions must match original image dimensions: {image.width}x{image.height}, got {image_copy_cache.width}x{image_copy_cache.height}"
            )

    _lib.apply_shadow(
        image.buffer,
        image_copy_cache.buffer,
        image.width,
        image.height,
        radius,
        intensity,
        shadow_color.r,
        shadow_color.g,
        shadow_color.b,
        shadow_color.a,
        int(inner),
    )

    if need_free:
        image_copy_cache.free()


def apply_gaussian_blur(image: CudaImage,
                        radius: float,
                        image_copy_cache: CudaImage = None) -> None:
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer,
                               image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width
                or image_copy_cache.height != image.height):
            raise ValueError(
                f"El buffer auxiliar debe coincidir con las dimensiones de la imagen original: {image.width}x{image.height}, recibido {image_copy_cache.width}x{image_copy_cache.height}"
            )

    _lib.apply_gaussian_blur(image.buffer, image_copy_cache.buffer,
                             image.width, image.height, radius)

    if need_free:
        image_copy_cache.free()
