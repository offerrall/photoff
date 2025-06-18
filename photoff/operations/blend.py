from ..core import _lib
from ..core.types import CudaImage


def blend(background: CudaImage, over: CudaImage, x: int, y: int) -> None:
    """
    Blends an image (`over`) on top of another (`background`) at a specified position.

    The blending respects the alpha channel of the overlaid image. No clipping is performed
    if the `over` image exceeds the bounds of the `background`; behavior in such cases depends on the underlying CUDA implementation.

    Args:
        background (CudaImage): The base image to draw onto.
        over (CudaImage): The image to blend on top.
        x (int): Horizontal position in the background where the top-left corner of `over` is placed.
        y (int): Vertical position in the background where the top-left corner of `over` is placed.

    Returns:
        None

    Example:
        >>> blend(bg_img, icon_img, x=100, y=50)
    """
    _lib.blend_buffers(background.buffer,
                       over.buffer,
                       background.width,
                       background.height,
                       over.width,
                       over.height,
                       x,
                       y,
                       )
