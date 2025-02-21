from ._cffi_instance import ffi, _lib
from .types import CudaImage
from ._core import save_image_from_cuda_buffer
from PIL import Image
import numpy as np

def save_image(image: CudaImage, filename: str) -> None:
    """Save a CudaImage to a file."""
    save_image_from_cuda_buffer(image.buffer.buffer, image.width, image.height, filename)

def open_image(target: CudaImage, filename: str) -> None:
    """Load an image file into an existing CudaImage."""
    from PIL import Image
    pil_image = Image.open(filename).convert("RGBA")
    width, height = pil_image.size
    img_data = bytearray(pil_image.tobytes())
    data_ptr = ffi.from_buffer(img_data)
    _lib.copy_to_device(target.buffer.buffer, 
                       ffi.cast("uchar4*", data_ptr),
                       width, height)