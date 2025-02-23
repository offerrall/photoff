from photoff.operations.fill import fill_color
from photoff.operations.filters import apply_corner_radius, apply_stroke

from photoff.io import save_image
from photoff import RGBA, CudaImage

from typing import Annotated
from functogui import App, imageFileReturn, intUi

def corner_border_ui(color: tuple[int, int, int, int] = (255, 0, 0, 255),
                     border_size: Annotated[int, intUi(min_value=1, max_value=500)] = 500,
                     stroke_width: Annotated[int, intUi(min_value=1, max_value=20)] = 5,
                     stroke_color: tuple[int, int, int, int] = (0, 255, 0, 255)
                     ) -> Annotated[str, imageFileReturn]:
    
    path = "./visual_test/corner_border.png"
    image = CudaImage(1000, 1000)

    # Rellenamos la imagen con el color base
    fill_color(image, RGBA(*color))
    # Aplicamos el redondeo de esquinas
    apply_corner_radius(image, border_size)
    # Aplicamos el trazo (stroke) sobre las áreas con canal alfa transparente adyacentes a píxeles opacos
    apply_stroke(image, stroke_width, RGBA(*stroke_color))
    
    save_image(image, path)
    image.free()

    return path

App(corner_border_ui)
