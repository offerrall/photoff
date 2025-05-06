from ..core.types import CudaImage, RGBA
from .blend import blend
from .fill import fill_color
from .resize import resize, ResizeMethod


def get_padding_size(image: CudaImage, padding: int) -> tuple[int, int]:
    return image.width + (padding * 2), image.height + (padding * 2)


def get_no_padding_size(image: CudaImage, padding: int) -> tuple[int, int]:
    return image.width - (padding * 2), image.height - (padding * 2)


def blend_aligned(
    background: CudaImage,
    image: CudaImage,
    align: str = "center",
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
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


def get_cover_resize_dimensions(image: CudaImage, container_width: int,
                                container_height: int) -> tuple[int, int]:
    scale = max(container_width / image.width, container_height / image.height)
    new_width = int(image.width * scale)
    new_height = int(image.height * scale)

    return new_width, new_height


def cover_image_in_container(
    image: CudaImage,
    container_width: int,
    container_height: int,
    offset_x: int = 0,
    offset_y: int = 0,
    background_color: RGBA = RGBA(0, 0, 0, 0),
    container_image_cache: CudaImage = None,
    resize_image_cache: CudaImage = None,
    resize_mode: ResizeMethod = ResizeMethod.BICUBIC,
) -> CudaImage:
    scale = max(container_width / image.width, container_height / image.height)
    new_width = int(image.width * scale)
    new_height = int(image.height * scale)

    need_free_resized = False
    if resize_image_cache is None:
        resized_image = CudaImage(new_width, new_height)
        need_free_resized = True
    else:
        if (resize_image_cache.width != new_width
                or resize_image_cache.height != new_height):
            raise ValueError(
                f"Resize cache dimensions must match: {new_width}x{new_height}, got {resize_image_cache.width}x{resize_image_cache.height}"
            )
        resized_image = resize_image_cache

    resize(
        image,
        new_width,
        new_height,
        method=resize_mode,
        resize_image_cache=resized_image,
    )

    if container_image_cache is None:
        container = CudaImage(container_width, container_height)
    else:
        if (container_image_cache.width != container_width
                or container_image_cache.height != container_height):
            raise ValueError(
                f"Container cache dimensions must match: {container_width}x{container_height}, got {container_image_cache.width}x{container_image_cache.height}"
            )
        container = container_image_cache

    fill_color(container, background_color)

    x = (container_width - new_width) // 2 + offset_x
    y = (container_height - new_height) // 2 + offset_y

    blend(container, resized_image, x, y)

    if need_free_resized:
        resized_image.free()

    return container

def create_image_grid(
    image: CudaImage,
    grid_width: int,
    grid_height: int,
    num_images: int,
    spacing: int = 0,
    background_color: RGBA = RGBA(0, 0, 0, 0),
    grid_image_cache: CudaImage = None,
) -> CudaImage:

    total_cells = grid_width * grid_height
    if num_images > total_cells:
        raise ValueError(
            f"Number of images ({num_images}) exceeds grid capacity ({total_cells})"
        )
    
    width = (image.width * grid_width) + (spacing * (grid_width - 1))
    height = (image.height * grid_height) + (spacing * (grid_height - 1))
    
    if grid_image_cache is None:
        result = CudaImage(width, height)
    else:
        if grid_image_cache.width != width or grid_image_cache.height != height:
            raise ValueError(
                f"Grid cache dimensions must match: {width}x{height}, got {grid_image_cache.width}x{grid_image_cache.height}"
            )
        result = grid_image_cache
    
    fill_color(result, background_color)
    
    count = 0
    for y in range(grid_height):
        for x in range(grid_width):
            if count >= num_images:
                break
                
            pos_x = x * (image.width + spacing)
            pos_y = y * (image.height + spacing)
            
            blend(result, image, pos_x, pos_y)
            
            count += 1
        
        if count >= num_images:
            break
    
    return result


def create_image_collage(
    images: list[CudaImage],
    grid_width: int,
    grid_height: int,
    spacing: int = 0,
    background_color: RGBA = RGBA(0, 0, 0, 0),
    collage_image_cache: CudaImage = None,
) -> CudaImage:

    total_cells = grid_width * grid_height
    num_images = len(images)
    if num_images > total_cells:
        raise ValueError(
            f"Number of images ({num_images}) exceeds grid capacity ({total_cells})"
        )

    first = images[0]
    img_w, img_h = first.width, first.height
    for img in images:
        if img.width != img_w or img.height != img_h:
            raise ValueError(
                "All images must have the same dimensions to form a uniform collage"
            )

    width = (img_w * grid_width) + (spacing * (grid_width - 1))
    height = (img_h * grid_height) + (spacing * (grid_height - 1))

    if collage_image_cache is None:
        result = CudaImage(width, height)
    else:
        if (collage_image_cache.width != width
                or collage_image_cache.height != height):
            raise ValueError(
                f"Collage cache dimensions must match: {width}x{height}, got {collage_image_cache.width}x{collage_image_cache.height}"
            )
        result = collage_image_cache

    fill_color(result, background_color)

    for idx, img in enumerate(images):
        col = idx % grid_width
        row = idx // grid_width
        x_pos = col * (img_w + spacing)
        y_pos = row * (img_h + spacing)
        blend(result, img, x_pos, y_pos)

    return result
