from enum import Enum
from ..core import _lib
from ..core.types import CudaImage


class ResizeMethod(Enum):
    """
    Enum representing supported image resizing algorithms.

    Attributes:
        BILINEAR: Bilinear interpolation (smooth, reasonably fast).
        NEAREST: Nearest neighbor interpolation (fastest, lowest quality).
        BICUBIC: Bicubic interpolation (higher quality, slower).

    Usage:
        method = ResizeMethod.BICUBIC
    """
    BILINEAR = "bilinear"
    NEAREST = "nearest"
    BICUBIC = "bicubic"

def resize(image: CudaImage,
           width: int,
           height: int,
           method: ResizeMethod = ResizeMethod.BICUBIC,
           resize_image_cache: CudaImage = None,
           ) -> CudaImage:
    """
    Resizes a CudaImage to the specified dimensions using the chosen interpolation method.

    Supports bilinear, nearest-neighbor, and bicubic resampling. A cache image can be reused
    for performance to avoid memory allocation.

    Args:
        image (CudaImage): The input image to resize.
        width (int): Target width.
        height (int): Target height.
        method (ResizeMethod, optional): Resampling method. Defaults to BICUBIC.
        resize_image_cache (CudaImage, optional): Pre-allocated image for the resized result.
            Must match target dimensions if provided.

    Returns:
        CudaImage: A new (or reused) image resized to the given dimensions.

    Raises:
        ValueError: If the cache image dimensions do not match the target size.
        ValueError: If the interpolation method is not supported.

    Example:
        >>> resized = resize(img, 256, 256, method=ResizeMethod.BILINEAR)
    """

    if resize_image_cache is None:
        result = CudaImage(width, height)
    else:
        if resize_image_cache.width != width or resize_image_cache.height != height:
            raise ValueError(f"Destination image dimensions must match resize dimensions: {width}x{height}, got {resize_image_cache.width}x{resize_image_cache.height}")
        result = resize_image_cache

    if method == ResizeMethod.BILINEAR:
        _lib.resize_bilinear(result.buffer, image.buffer, width, height, image.width, image.height)
    elif method == ResizeMethod.NEAREST:
        _lib.resize_nearest(result.buffer, image.buffer, width, height, image.width, image.height)
    elif method == ResizeMethod.BICUBIC:
        _lib.resize_bicubic(result.buffer, image.buffer, width, height, image.width, image.height)
    else:
        raise ValueError(f"Unsupported resize method: {method}")

    return result


def crop_margins(image: CudaImage,
                 left: int = 0,
                 top: int = 0,
                 right: int = 0,
                 bottom: int = 0,
                 crop_image_cache: CudaImage = None,
                 ) -> CudaImage:
    """
    Crops margins from the edges of a CudaImage.

    Margins are specified in pixels. The resulting image will be smaller and positioned
    relative to the top-left corner of the cropped area.

    Args:
        image (CudaImage): The input image to crop.
        left (int, optional): Pixels to remove from the left edge. Defaults to 0.
        top (int, optional): Pixels to remove from the top edge. Defaults to 0.
        right (int, optional): Pixels to remove from the right edge. Defaults to 0.
        bottom (int, optional): Pixels to remove from the bottom edge. Defaults to 0.
        crop_image_cache (CudaImage, optional): Pre-allocated buffer for the cropped image.
            Must match the expected result dimensions.

    Returns:
        CudaImage: The cropped image.

    Raises:
        ValueError: If any margin is negative.
        ValueError: If margins exceed the image's size.
        ValueError: If the cache image does not match the result size.

    Example:
        >>> cropped = crop_margins(img, left=10, top=10, right=10, bottom=10)
    """

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
            raise ValueError(f"Destination image cache dimensions must match crop result: {new_width}x{new_height}")
        result = crop_image_cache

    _lib.crop_image(result.buffer,
                    image.buffer,
                    image.width,
                    image.height,
                    new_width,
                    new_height,
                    left,
                    top,
                    )

    return result
