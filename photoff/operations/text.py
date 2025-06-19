from PIL import Image, ImageDraw, ImageFont 
from ..core.types import CudaImage, RGBA
from ..core.cuda_interface import ffi 
from ..core.buffer import copy_to_device

def render_text(text: str,
                font_path: str,
                font_size: int = 24,
                color: RGBA = RGBA(0, 0, 0, 255)
                ) -> CudaImage:
    """
    Renders a string of text into a CudaImage using a specified TrueType font.

    The function uses Pillow (PIL) to rasterize the text and transfers the resulting
    RGBA image into GPU memory as a `CudaImage`. Font metrics are computed to fit
    the rendered text exactly, avoiding unnecessary padding.

    Args:
        text (str): The string to render.
        font_path (str): Path to a TrueType (.ttf) or OpenType (.otf) font file.
        font_size (int, optional): Font size in points. Defaults to 24.
        color (RGBA, optional): Text color. Defaults to opaque black (0, 0, 0, 255).

    Returns:
        CudaImage: GPU image containing the rendered text.

    Raises:
        ValueError: If the font file cannot be loaded.

    Example:
        >>> img = render_text("Hello GPU!", "/fonts/Roboto-Regular.ttf", 32, RGBA(255, 255, 255, 255))
    """
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        raise ValueError(f"Error loading font '{font_path}': {e}")

    tmp_img = Image.new("RGBA", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp_img)
    try:
        left, top, right, bottom = font.getbbox(text)
    except AttributeError:
        left, top, right, bottom = tmp_draw.textbbox((0, 0), text, font=font)

    width, height = right - left, bottom - top

    pil_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pil_img)
    draw.text((-left, -top), text, fill=(color.r, color.g, color.b, color.a), font=font)

    cuda_img = CudaImage(width, height)

    host_buf = bytearray(pil_img.tobytes())
    src_ptr = ffi.cast("uchar4*", ffi.from_buffer(host_buf))
    copy_to_device(cuda_img.buffer, src_ptr, width, height)

    return cuda_img