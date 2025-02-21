from ._cffi_instance import _lib, ffi
from .types import CudaImage, CudaBuffer

def new_image(width: int, height: int) -> CudaImage:

    buffer = _lib.create_buffer(width, height)
    buffer = CudaBuffer(buffer)
    return CudaImage(width, height, buffer)

def free_image(image: CudaImage) -> None:

    _lib.free_buffer(image.buffer.buffer)
    image.buffer = None


def save_image_from_cuda_buffer(cuda_buffer, width: int, height: int, filename: str) -> None:
    """Save an image from a CUDA buffer to a file using Pillow."""
    from PIL import Image
    img_data = bytearray(width * height * 4)
    data_ptr = ffi.from_buffer(img_data)
    _lib.copy_to_host(ffi.cast("uchar4*", data_ptr), cuda_buffer, width, height)
    img = Image.frombytes("RGBA", (width, height), bytes(img_data))
    img.save(filename)