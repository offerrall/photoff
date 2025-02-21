from PIL import Image
from ._cffi_instance import ffi
from ._core import copy_to_host, copy_to_device
from .types import CudaImage
import numpy as np


def save_image(image: CudaImage,
               filename: str) -> None:

    img_data = bytearray(image.width * image.height * 4)
    data_ptr = ffi.from_buffer(img_data)
    copy_to_host(ffi.cast("uchar4*", data_ptr), image.buffer, image.width, image.height)
    img = Image.frombytes("RGBA", (image.width, image.height), bytes(img_data))
    img.save(filename)

def load_image(filename: str, container: CudaImage = None) -> CudaImage:
    img = Image.open(filename).convert("RGBA")
    width, height = img.size
    img_array = np.asarray(img, dtype=np.uint8)

    if container is None:
        container = CudaImage(width, height)

    c_buffer = ffi.cast("uchar4*", img_array.ctypes.data)
    copy_to_device(container.buffer, c_buffer, width, height)

    return container