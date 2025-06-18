from ..core import _lib
from ..core.types import CudaImage, RGBA


def fill_color(image: CudaImage, color: RGBA) -> None:
    """
    Fills the entire image with a solid color.

    This operation overwrites all pixels in the image with the specified RGBA color.

    Args:
        image (CudaImage): The image to fill.
        color (RGBA): The fill color to apply.

    Returns:
        None

    Example:
        >>> fill_color(img, RGBA(255, 255, 255, 255))  # Fill with solid white
    """

    _lib.fill_color(image.buffer,
                    image.width,
                    image.height,
                    color.r,
                    color.g,
                    color.b,
                    color.a)


def fill_gradient(image: CudaImage,
                  color1: RGBA,
                  color2: RGBA,
                  direction: int = 0,
                  seamless: bool = False) -> None:
    """
    Fills the image with a linear gradient between two colors.

    The gradient direction and style (seamless or linear) can be customized.

    Args:
        image (CudaImage): The target image to fill.
        color1 (RGBA): The starting color of the gradient.
        color2 (RGBA): The ending color of the gradient.
        direction (int, optional): Gradient direction:
            - 0 = vertical (top to bottom)
            - 1 = horizontal (left to right)
            - 2 = diagonal (top-left to bottom-right)
            - 3 = diagonal (bottom-left to top-right)
            Defaults to 0.
        seamless (bool, optional): Whether the gradient should repeat seamlessly. Defaults to False.

    Returns:
        None

    Raises:
        ValueError: If an invalid direction value is provided.

    Example:
        >>> fill_gradient(img, RGBA(0, 0, 0, 255), RGBA(255, 255, 255, 255), direction=1)
    """
    if direction not in (0, 1, 2, 3):
        raise ValueError(f"Invalid gradient direction: {direction}. Must be 0, 1, 2 or 3.")

    _lib.fill_gradient(image.buffer,
                       image.width,
                       image.height,
                       color1.r,
                       color1.g,
                       color1.b,
                       color1.a,
                       color2.r,
                       color2.g,
                       color2.b,
                       color2.a,
                       direction,
                       seamless,
                       )
