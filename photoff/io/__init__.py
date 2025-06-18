from ..core import ffi
from ..core.buffer import copy_to_host, copy_to_device
from ..core.types import CudaImage
from PIL import Image
import numpy as np


def image_to_pil(image: CudaImage) -> Image:
    """
    Converts a CudaImage to a PIL.Image in RGBA format.

    The image is copied from GPU memory to host memory and returned
    as a Pillow image object.

    Args:
        image (CudaImage): The image in GPU memory.

    Returns:
        PIL.Image: A new PIL Image with RGBA channels.

    Example:
        >>> pil_img = image_to_pil(cuda_img)
        >>> pil_img.show()
    """

    img_data = bytearray(image.width * image.height * 4)
    data_ptr = ffi.from_buffer(img_data)
    copy_to_host(ffi.cast("uchar4*", data_ptr), image.buffer, image.width,
                 image.height)
    return Image.frombytes("RGBA", (image.width, image.height),
                           bytes(img_data))


def save_image(image: CudaImage, filename: str) -> None:
    """
    Saves a CudaImage to disk as a standard image file.

    This function converts the image from GPU memory to a Pillow image and saves it
    using the given filename. The format is inferred from the file extension.

    Args:
        image (CudaImage): The image to save.
        filename (str): Destination path, including extension (e.g., 'output.png').

    Returns:
        None

    Example:
        >>> save_image(cuda_img, "output.png")
    """

    img = image_to_pil(image)
    img.save(filename)
    img.close()


def load_image(filename: str, container: CudaImage = None) -> CudaImage:
    """
    Loads an image from disk and transfers it to a CudaImage.

    The image is loaded using Pillow and converted to RGBA format. It is then copied
    to GPU memory. Optionally, a pre-allocated CudaImage container can be used to avoid allocation.

    Args:
        filename (str): Path to the image file to load.
        container (CudaImage, optional): Pre-allocated image buffer. Must be large enough to hold the image.

    Returns:
        CudaImage: A new or reused image object with the loaded data.

    Raises:
        ValueError: If the input image is larger than the provided container.

    Example:
        >>> cuda_img = load_image("texture.png")
    """

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
