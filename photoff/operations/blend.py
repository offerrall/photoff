from ..core import _lib
from ..core.types import CudaImage

def blend(background: CudaImage, over: CudaImage, x: int, y: int) -> None:
    
    _lib.blend_buffers(
        background.buffer, over.buffer,
        background.width, background.height,
        over.width, over.height,
        x, y
    )
