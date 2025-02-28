from photoff.operations.text import render_text
from photoff.io import save_image

from typing import Annotated
from functogui import App, imageFileReturn, fileUi, intUi


def text_ui(
    text: str = "Hello, World!",
    font_path: Annotated[str, fileUi] = "./assets/Arial.ttf",
    font_size: Annotated[int, intUi(min_value=8, max_value=72)] = 24,
    text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
) -> Annotated[str, imageFileReturn]:
    path = "./assets/text_test.png"
    text_image = render_text(text, font_path, font_size, text_color)
    save_image(text_image, path)
    text_image.free()

    return path


App(text_ui)
