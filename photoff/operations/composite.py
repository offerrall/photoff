from ..core.types import CudaImage
from .blend import blend




def get_blend_padding_size(image: CudaImage, 
                           padding: int) -> tuple[int, int]:
    
    return image.width + (padding * 2), image.height + (padding * 2)


def blend_padding(image: CudaImage,
                  padding: int,
                  background: CudaImage = None) -> CudaImage:

    padded_width, padded_height = get_blend_padding_size(image, padding)
    
    if background is None:
        background = CudaImage(padded_width, padded_height)
    else:
        if background.width != padded_width or background.height != padded_height:
            raise ValueError(f"Destination image dimensions must match padding result: {padded_width}x{padded_height}, got {background.width}x{background.height}")
    
    blend(background, image, padding, padding)
    
    return background