from .cuda_interface import _lib, ffi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import CudaBuffer


def create_buffer(width: int, height: int) -> "CudaBuffer":
    """
    Allocates a new CUDA buffer for an image of given dimensions.

    Args:
        width (int): Width of the buffer in pixels.
        height (int): Height of the buffer in pixels.

    Returns:
        CudaBuffer: A pointer to the allocated device memory buffer.

    Example:
        >>> buffer = create_buffer(512, 512)
    """

    return _lib.create_buffer(width, height)


def free_buffer(buffer: "CudaBuffer") -> None:
    """
    Frees a CUDA buffer previously allocated on the device.

    Args:
        buffer (CudaBuffer): The buffer to free.

    Returns:
        None

    Example:
        >>> free_buffer(buffer)
    """

    _lib.free_buffer(buffer)


def copy_to_host(h_dst: "CudaBuffer", d_src: "CudaBuffer", width: int, height: int) -> None:
    """
    Copies image data from device (GPU) to host (CPU) memory.

    Args:
        h_dst (CudaBuffer): Destination buffer in host memory.
        d_src (CudaBuffer): Source buffer in device memory.
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        None

    Example:
        >>> copy_to_host(cpu_buf, gpu_buf, 256, 256)
    """

    _lib.copy_to_host(h_dst, d_src, width, height)


def copy_to_device(d_dst: "CudaBuffer", h_src: "CudaBuffer", width: int, height: int) -> None:
    """
    Copies image data from host (CPU) to device (GPU) memory.

    Args:
        d_dst (CudaBuffer): Destination buffer in device memory.
        h_src (CudaBuffer): Source buffer in host memory.
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        None

    Example:
        >>> copy_to_device(gpu_buf, cpu_buf, 256, 256)
    """

    _lib.copy_to_device(d_dst, h_src, width, height)


def copy_buffers_same_size(dst: "CudaBuffer", src: "CudaBuffer", width: int, height: int) -> None:
    """
    Copies data between two CUDA buffers of the same size.

    This is useful for in-GPU memory operations like duplicating an image or
    preparing a temporary working buffer.

    Args:
        dst (CudaBuffer): Destination buffer on the device.
        src (CudaBuffer): Source buffer on the device.
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        None

    Example:
        >>> copy_buffers_same_size(tmp_buf, original_buf, 512, 512)
    """

    _lib.copy_buffers_same_size(dst, src, width, height)
