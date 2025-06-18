from ..core import _lib
from ..core.types import CudaImage, RGBA
from ..core.buffer import copy_buffers_same_size


def apply_corner_radius(image: CudaImage, size: int) -> None:
    """
    Applies a rounded corner mask to an image in-place.

    Args:
        image (CudaImage): Image to be modified.
        size (int): Radius of the corner in pixels.

    Returns:
        None
    """

    _lib.apply_corner_radius(image.buffer, image.width, image.height, size)


def apply_opacity(image: CudaImage, opacity: float) -> None:
    """
    Modifies the alpha channel of an image to apply global opacity.

    Args:
        image (CudaImage): Image to modify.
        opacity (float): Opacity value between 0.0 (transparent) and 1.0 (opaque).

    Returns:
        None
    """

    _lib.apply_opacity(image.buffer, image.width, image.height, opacity)


def apply_flip(image: CudaImage,
               flip_horizontal: bool = False,
               flip_vertical: bool = False) -> None:
    """
    Flips an image horizontally or vertically in-place.

    Args:
        image (CudaImage): Image to flip.
        flip_horizontal (bool, optional): Flip the image horizontally. Defaults to False.
        flip_vertical (bool, optional): Flip the image vertically. Defaults to False.

    Raises:
        ValueError: If both `flip_horizontal` and `flip_vertical` are True.

    Returns:
        None
    """
    
    if flip_horizontal and flip_vertical:
        raise ValueError("Cannot flip both horizontal and vertical at the same time")

    _lib.apply_flip(image.buffer, image.width, image.height, flip_horizontal, flip_vertical)


def apply_grayscale(image: CudaImage) -> None:
    """
    Converts an image to grayscale in-place using luminosity method.

    Args:
        image (CudaImage): Image to convert.

    Returns:
        None
    """

    _lib.apply_grayscale(image.buffer, image.width, image.height)


def apply_chroma_key(image: CudaImage,
                     key_image: CudaImage,
                     channel: str = "A",
                     threshold: int = 128,
                     invert: bool = False,
                     zero_all_channels: bool = False) -> None:
    """
    Applies a chroma key mask based on a channel of another image.

    Args:
        image (CudaImage): The target image to apply transparency.
        key_image (CudaImage): Image whose channel values are used as a mask.
        channel (str, optional): Channel to use from the key image ('R', 'G', 'B', 'A'). Defaults to 'A'.
        threshold (int, optional): Threshold (0–255) to apply masking. Defaults to 128.
        invert (bool, optional): Invert the mask logic. Defaults to False.
        zero_all_channels (bool, optional): If True, sets RGB to zero where mask applies. Defaults to False.

    Raises:
        ValueError: If the provided channel is invalid.

    Returns:
        None
    """
    
    channel_upper = (channel.upper() if isinstance(channel, str) else str(channel).upper())

    if channel_upper == "R":
        channel_idx = 0
    elif channel_upper == "G":
        channel_idx = 1
    elif channel_upper == "B":
        channel_idx = 2
    elif channel_upper == "A":
        channel_idx = 3
    else:
        raise ValueError(f"Invalid channel: {channel}, must be one of 'R', 'G', 'B', 'A'")

    _lib.apply_chroma_key(image.buffer,
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


def apply_stroke(image: CudaImage,
                 stroke_width: int,
                 stroke_color: RGBA,
                 image_copy_cache: CudaImage = None,
                 inner: bool = True) -> None:
    """
    Draws a stroke (outline) around the non-transparent areas of an image.

    Args:
        image (CudaImage): Image to which the stroke will be applied.
        stroke_width (int): Width of the stroke in pixels.
        stroke_color (RGBA): Color of the stroke.
        image_copy_cache (CudaImage, optional): Optional cache of the original image. Must match dimensions.
        inner (bool, optional): If True, stroke is drawn inside the shape; otherwise outside. Defaults to True.

    Raises:
        ValueError: If the provided cache does not match image dimensions.

    Returns:
        None
    """
    
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer, image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width or image_copy_cache.height != image.height):
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
                      int(inner),
                      )

    if need_free:
        image_copy_cache.free()


def apply_shadow(image: CudaImage,
                 radius: float,
                 intensity: float,
                 shadow_color: RGBA,
                 image_copy_cache: CudaImage = None,
                 inner: bool = False) -> None:
    """
    Applies a shadow effect around the opaque regions of an image.

    Args:
        image (CudaImage): Image to apply the shadow to.
        radius (float): Blur radius of the shadow.
        intensity (float): Intensity multiplier of the shadow.
        shadow_color (RGBA): Color of the shadow.
        image_copy_cache (CudaImage, optional): Optional image copy buffer. Must match original image size.
        inner (bool, optional): Whether to draw the shadow inside the shape. Defaults to False.

    Raises:
        ValueError: If the cache does not match the image dimensions.

    Returns:
        None
    """
    
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer, image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width or image_copy_cache.height != image.height):
            raise ValueError(f"Destination image dimensions must match original image dimensions: {image.width}x{image.height}, got {image_copy_cache.width}x{image_copy_cache.height}")

    _lib.apply_shadow(image.buffer,
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
    """
    Applies a Gaussian blur effect to an image in-place.

    Args:
        image (CudaImage): Image to blur.
        radius (float): Radius of the blur in pixels.
        image_copy_cache (CudaImage, optional): Optional buffer. Must match image size.

    Raises:
        ValueError: If the cache does not match the image dimensions.

    Returns:
        None
    """
    
    need_free = False
    if image_copy_cache is None:
        image_copy_cache = CudaImage(image.width, image.height)
        copy_buffers_same_size(image_copy_cache.buffer, image.buffer, image.width, image.height)
        need_free = True
    else:
        if (image_copy_cache.width != image.width or image_copy_cache.height != image.height):
            raise ValueError(f"El buffer auxiliar debe coincidir con las dimensiones de la imagen original: {image.width}x{image.height}, recibido {image_copy_cache.width}x{image_copy_cache.height}")

    _lib.apply_gaussian_blur(image.buffer, image_copy_cache.buffer, image.width, image.height, radius)

    if need_free:
        image_copy_cache.free()