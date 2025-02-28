from photoff.operations.filters import apply_shadow
from photoff.io import save_image, load_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, fileUi, floatUi


def shadow_ui(
    image: Annotated[str, fileUi] = "./assets/logo.png",
    radius: Annotated[float, floatUi(min_value=1.0, max_value=50.0)] = 10.0,
    intensity: Annotated[float, floatUi(min_value=0.1, max_value=1.0)] = 0.5,
    shadow_color: tuple[int, int, int, int] = (0, 0, 0, 128),
    inner: bool = False,
) -> Annotated[str, imageFileReturn]:
    path = "./assets/shadow_test.png"
    src_image = load_image(image)

    apply_shadow(
        src_image,
        radius,
        intensity,
        RGBA(*shadow_color),
        image_copy_cache=None,
        inner=inner,
    )

    save_image(src_image, path)
    src_image.free()
    return path


App(shadow_ui)
