from PIL import Image, ImageDraw, ImageFont
from ..core.types import CudaImage
from ..core.cuda_interface import ffi
from ..core.buffer import copy_to_device
import numpy as np


def render_text(text: str,
                font_path: str,
                font_size: int = 24,
                color: tuple = (0, 0, 0, 255)) -> CudaImage:
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        raise ValueError(f"Error al cargar la fuente '{font_path}': {e}")

    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    try:
        bbox = font.getbbox(text)
    except AttributeError:
        bbox = temp_draw.textbbox((0, 0), text, font=font)

    left, top, right, bottom = bbox
    text_width = right - left
    text_height = bottom - top

    pil_image = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pil_image)

    draw.text((-left, -top), text, fill=color, font=font)
    
    cuda_image = CudaImage(text_width, text_height)
    
    img_array = np.asarray(pil_image, dtype=np.uint8)
    c_buffer = ffi.cast("uchar4*", img_array.ctypes.data)
    copy_to_device(cuda_image.buffer, c_buffer, text_width, text_height)
    
    return cuda_image