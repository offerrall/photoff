from ..core.types import CudaImage, RGBA
from .blend import blend
from .fill import fill_color
from .resize import resize, ResizeMethod


def get_padding_size(image: CudaImage, padding: int) -> tuple[int, int]:
    """
    Calculates the size of an image after adding equal padding on all sides.

    Args:
        image (CudaImage): The original image.
        padding (int): Padding in pixels to add on each side.

    Returns:
        tuple[int, int]: The new width and height including padding.

    Example:
        >>> get_padding_size(img, 10)
        (image.width + 20, image.height + 20)
    """
    return image.width + (padding * 2), image.height + (padding * 2)

def get_no_padding_size(image: CudaImage, padding: int) -> tuple[int, int]:
    """
    Calculates the size of an image after removing equal padding from all sides.

    Args:
        image (CudaImage): The padded image.
        padding (int): Padding in pixels to remove from each side.

    Returns:
        tuple[int, int]: The resulting width and height without padding.

    Example:
        >>> get_no_padding_size(img, 10)
        (image.width - 20, image.height - 20)
    """
    return image.width - (padding * 2), image.height - (padding * 2)


def blend_aligned(background: CudaImage,
                  image: CudaImage,
                  align: str = "center",
                  offset_x: int = 0,
                  offset_y: int = 0,
                  ) -> None:
    """
    Blends an image onto a background at a specified alignment and optional offset.

    The image is positioned relative to the background based on the `align` parameter,
    which supports standard alignment strings (e.g., "center", "top-left", etc.).
    Offsets can be applied to adjust the final position.

    Args:
        background (CudaImage): The background image where the input image will be blended.
        image (CudaImage): The image to blend.
        align (str, optional): Alignment method. Supported values:
            - "center" / "middle"
            - "top", "bottom", "left", "right"
            - "top-left", "top-right", "bottom-left", "bottom-right"
            Defaults to "center".
        offset_x (int, optional): Horizontal pixel offset to apply after alignment. Defaults to 0.
        offset_y (int, optional): Vertical pixel offset to apply after alignment. Defaults to 0.

    Returns:
        None

    Example:
        >>> blend_aligned(bg, img, align="bottom-right", offset_x=-10, offset_y=-10)
    """

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


def get_cover_resize_dimensions(image: CudaImage,
                                container_width: int,
                                container_height: int) -> tuple[int, int]:
    """
    Calculates the new dimensions to resize an image so that it fully covers
    a container while preserving its aspect ratio.

    The resulting dimensions ensure that the image completely fills the target
    container (`container_width` x `container_height`), potentially exceeding
    one of the container's dimensions. This mimics the behavior of `background-size: cover` in CSS.

    Args:
        image (CudaImage): The original image to be resized.
        container_width (int): Target container width.
        container_height (int): Target container height.

    Returns:
        tuple[int, int]: The new width and height that the image should be resized to.

    Example:
        >>> get_cover_resize_dimensions(img, 1920, 1080)
        (1920, 1280)
    """

    scale = max(container_width / image.width, container_height / image.height)
    new_width = int(image.width * scale)
    new_height = int(image.height * scale)

    return new_width, new_height


def cover_image_in_container(image: CudaImage,
                             container_width: int,
                             container_height: int,
                             offset_x: int = 0,
                             offset_y: int = 0,
                             background_color: RGBA = RGBA(0, 0, 0, 0),
                             container_image_cache: CudaImage = None,
                             resize_image_cache: CudaImage = None,
                             resize_mode: ResizeMethod = ResizeMethod.BICUBIC,
                             ) -> CudaImage:
    """
    Resizes an image to fully cover a container while maintaining aspect ratio,
    and blends it centered (or offset) within the container.

    The image is scaled up proportionally so that it completely fills the container
    dimensions (`container_width` x `container_height`). The resized image may overflow
    on one axis, similar to CSS's `background-size: cover`. Optional caching and
    resizing method are supported for performance and quality tuning.

    Args:
        image (CudaImage): The input image to be resized and placed.
        container_width (int): Width of the container image.
        container_height (int): Height of the container image.
        offset_x (int, optional): Horizontal offset to apply after centering. Defaults to 0.
        offset_y (int, optional): Vertical offset to apply after centering. Defaults to 0.
        background_color (RGBA, optional): Background color to fill the container. Defaults to transparent black.
        container_image_cache (CudaImage, optional): Pre-allocated container image buffer. Must match the container dimensions.
        resize_image_cache (CudaImage, optional): Pre-allocated image for resized content. Must match computed resize dimensions.
        resize_mode (ResizeMethod, optional): Resize algorithm to use (e.g., BICUBIC, NEAREST). Defaults to BICUBIC.

    Returns:
        CudaImage: A new image with the resized input blended over the background.

    Raises:
        ValueError: If the number of images exceeds the grid capacity.
        ValueError: If provided `resize_image_cache` or `container_image_cache` have incorrect dimensions.
    """
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

def create_image_grid(image: CudaImage,
                      grid_width: int,
                      grid_height: int,
                      num_images: int,
                      spacing: int = 0,
                      background_color: RGBA = RGBA(0, 0, 0, 0),
                      grid_image_cache: CudaImage = None,
                      ) -> CudaImage:
    """
    Creates a grid layout by duplicating a single image multiple times.

    The image is repeated `num_images` times and arranged in a grid with the specified
    width and height. Optional spacing and background color can be configured. A cached
    output image can be reused for efficiency.

    Args:
        image (CudaImage): The image to be repeated across the grid.
        grid_width (int): Number of columns in the grid.
        grid_height (int): Number of rows in the grid.
        num_images (int): Total number of image copies to include in the grid. Must not exceed grid capacity.
        spacing (int, optional): Number of pixels between images in both directions. Defaults to 0.
        background_color (RGBA, optional): Background color to fill empty areas. Defaults to transparent black.
        grid_image_cache (CudaImage, optional): Pre-allocated image buffer to use. Must match final grid size if provided.

    Returns:
        CudaImage: A new image containing the grid of repeated images.

    Raises:
        ValueError: If `num_images` exceeds the grid's capacity.
        ValueError: If `grid_image_cache` is provided but has incorrect dimensions.
    """

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


def create_image_collage(images: list[CudaImage],
                         grid_width: int,
                         grid_height: int,
                         spacing: int = 0,
                         background_color: RGBA = RGBA(0, 0, 0, 0),
                         collage_image_cache: CudaImage = None,
                         ) -> CudaImage:
    """
    Creates a collage from a list of CUDA images arranged in a grid.

    All images must have identical dimensions. The function supports optional
    spacing between images and a custom background color. It also allows
    reuse of a pre-allocated image buffer to avoid reallocations.

    Args:
        images (list[CudaImage]): List of images to include in the collage.
        grid_width (int): Number of columns in the collage grid.
        grid_height (int): Number of rows in the collage grid.
        spacing (int, optional): Space in pixels between images in the grid. Defaults to 0.
        background_color (RGBA, optional): Background color to fill the collage. Defaults to transparent black (0, 0, 0, 0).
        collage_image_cache (CudaImage, optional): Optional pre-allocated image to use as the collage buffer.
            Must match the final dimensions. If not provided, a new image will be created.

    Returns:
        CudaImage: A new image containing the collage.

    Raises:
        ValueError: If the number of images exceeds the grid capacity.
        ValueError: If input images do not have the same dimensions.
        ValueError: If the provided collage_image_cache does not match the required dimensions.
    """

    total_cells = grid_width * grid_height
    num_images = len(images)
    if num_images > total_cells:
        raise ValueError(f"Number of images ({num_images}) exceeds grid capacity ({total_cells})")

    first = images[0]
    img_w, img_h = first.width, first.height
    for img in images:
        if img.width != img_w or img.height != img_h:
            raise ValueError("All images must have the same dimensions to form a uniform collage")

    width = (img_w * grid_width) + (spacing * (grid_width - 1))
    height = (img_h * grid_height) + (spacing * (grid_height - 1))

    if collage_image_cache is None:
        result = CudaImage(width, height)
    else:
        if (collage_image_cache.width != width or collage_image_cache.height != height):
            raise ValueError(f"Collage cache dimensions must match: {width}x{height}, got {collage_image_cache.width}x{collage_image_cache.height}")
        result = collage_image_cache

    fill_color(result, background_color)

    for idx, img in enumerate(images):
        col = idx % grid_width
        row = idx // grid_width
        x_pos = col * (img_w + spacing)
        y_pos = row * (img_h + spacing)
        blend(result, img, x_pos, y_pos)

    return result
