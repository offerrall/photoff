from PIL import Image, ImageDraw, ImageFont 
from ..core.types import CudaImage, RGBA
from ..core.cuda_interface import ffi 
from ..core.buffer import copy_to_device
import numpy as np

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
        raise ValueError(f"Error al cargar la fuente '{font_path}': {e}")
    
    temp_img = Image.new("RGBA", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    try:
        bbox = font.getbbox(text)
    except AttributeError:
        bbox = temp_draw.textbbox((0, 0), text, font=font)
    
    left, top, right, bottom = bbox
    text_width = right - left
    text_height = bottom - top
    
    pil_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pil_image)
    
    color_tuple = (color.r, color.g, color.b, color.a)
    draw.text((-left, -top), text, fill=color_tuple, font=font)
    
    cuda_image = CudaImage(text_width, text_height)
    
    img_array = np.asarray(pil_image, dtype=np.uint8)
    c_buffer = ffi.cast("uchar4*", img_array.ctypes.data)
    copy_to_device(cuda_image.buffer, c_buffer, text_width, text_height)
    
    return cuda_image