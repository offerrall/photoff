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


def blend_aligned(background: CudaImage, 
                  image: CudaImage, 
                  align: str = "center",
                  offset_x: int = 0,
                  offset_y: int = 0) -> None:

    if align == "center" or align == "middle":
        x = (background.width - image.width) // 2
        y = (background.height - image.height) // 2
    
    elif align == "top":
        x = (background.width - image.width) // 2
        y = 0
    
    elif align == "bottom":
        x = (background.width - image.width) // 2
        y = background.height - image.height
    
    elif align == "left":
        x = 0
        y = (background.height - image.height) // 2
    
    elif align == "right":
        x = background.width - image.width
        y = (background.height - image.height) // 2
    
    elif align == "top-left":
        x = 0
        y = 0
    
    elif align == "top-right":
        x = background.width - image.width
        y = 0
    
    elif align == "bottom-left":
        x = 0
        y = background.height - image.height
    
    elif align == "bottom-right":
        x = background.width - image.width
        y = background.height - image.height
    
    else:
        x = (background.width - image.width) // 2
        y = (background.height - image.height) // 2
    
    x += offset_x
    y += offset_y
    
    blend(background, image, x, y)