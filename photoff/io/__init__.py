from ..core import ffi
from ..core.buffer import copy_to_host, copy_to_device
from ..core.types import CudaImage
from PIL import Image
import numpy as np


def image_to_pil(image: CudaImage) -> Image:
    img_data = bytearray(image.width * image.height * 4)
    data_ptr = ffi.from_buffer(img_data)
    copy_to_host(ffi.cast("uchar4*", data_ptr), image.buffer, image.width,
                 image.height)
    return Image.frombytes("RGBA", (image.width, image.height),
                           bytes(img_data))


def save_image(image: CudaImage, filename: str) -> None:
    img = image_to_pil(image)
    img.save(filename)
    img.close()


def load_image(filename: str, container: CudaImage = None) -> CudaImage:
    img = Image.open(filename).convert("RGBA")
    width, height = img.size

    if container is None:
        container = CudaImage(width, height)

    if width > container.width or height > container.height:
        raise ValueError("Image dimensions exceed container dimensions")

    img_array = np.asarray(img, dtype=np.uint8)

    c_buffer = ffi.cast("uchar4*", img_array.ctypes.data)
    copy_to_device(container.buffer, c_buffer, width, height)

    container.width = width
    container.height = height

    return container
