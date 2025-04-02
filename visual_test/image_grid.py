from photoff.operations.utils import create_image_grid  # Asumiendo que has añadido la función
from photoff.io import save_image, load_image
from photoff import RGBA
from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi, colorUi


def image_grid_ui(
    image: Annotated[str, fileUi] = "./assets/logo.png",
    grid_width: Annotated[int, intUi(min_value=1, max_value=10)] = 3,
    grid_height: Annotated[int, intUi(min_value=1, max_value=10)] = 3,
    num_images: Annotated[int, intUi(min_value=1, max_value=100)] = 5,
    spacing: Annotated[int, intUi(min_value=0, max_value=100)] = 10,
    background_color: Annotated[tuple[int, int, int, int], colorUi] = (0, 0, 0, 0),
) -> Annotated[str, imageFileReturn]:
    path = "./assets/image_grid_test.png"
    
    source_image = load_image(image)
    
    max_images = grid_width * grid_height
    if num_images > max_images:
        num_images = max_images
    
    result = create_image_grid(
        source_image,
        grid_width,
        grid_height,
        num_images,
        spacing,
        RGBA(*background_color)
    )
    
    save_image(result, path)
    source_image.free()
    result.free()
    
    return path


App(image_grid_ui)