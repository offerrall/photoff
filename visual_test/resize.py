from photoff.operations.resize import resize, ResizeMethod
from photoff.io import save_image, load_image
from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi, listUi


def resize_ui(
    image: Annotated[str, fileUi] = "./assets/logo.png",
    new_width: Annotated[int, intUi(min_value=1, max_value=1920)] = 800,
    new_height: Annotated[int, intUi(min_value=1, max_value=1080)] = 600,
    method: Annotated[
        str, listUi(values=["bilinear", "nearest", "bicubic"])] = "bicubic",
) -> Annotated[str, imageFileReturn]:
    path = "./assets/resized.png"

    source_image = load_image(image)
    resize_method = ResizeMethod[method.upper()]
    resized = resize(source_image, new_width, new_height, method=resize_method)

    save_image(resized, path)
    source_image.free()
    resized.free()

    return path


App(resize_ui)
