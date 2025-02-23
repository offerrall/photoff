from ..core import _lib
from ..core.types import CudaImage

def blend(dst: CudaImage, src: CudaImage, x: int, y: int) -> None:
    
    _lib.blend_buffers(dst.buffer, src.buffer, dst.width, dst.height, src.width, src.height, x, y)