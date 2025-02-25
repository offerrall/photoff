from .cuda_interface import _lib, ffi
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import CudaBuffer

def create_buffer(width: int, height: int) -> 'CudaBuffer':
    buffer = _lib.create_buffer(width, height)

    if buffer == ffi.NULL:
        raise MemoryError("Failed to allocate buffer")
    return _lib.create_buffer(width, height)

def free_buffer(buffer: 'CudaBuffer') -> None:
    _lib.free_buffer(buffer)

def copy_to_host(h_dst: 'CudaBuffer', d_src: 'CudaBuffer', width: int, height: int) -> None:
    _lib.copy_to_host(h_dst, d_src, width, height)

def copy_to_device(d_dst: 'CudaBuffer', h_src: 'CudaBuffer', width: int, height: int) -> None:
    _lib.copy_to_device(d_dst, h_src, width, height)
