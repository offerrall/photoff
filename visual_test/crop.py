from photoff.operations.resize import crop_margins
from photoff.io import save_image, load_image
from photoff import CudaImage
from typing import Annotated
from functogui import App, imageFileReturn, intUi, fileUi

def crop_margins_ui(image: Annotated[str, fileUi] = "./assets/stock.jpg",
                   left: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                   top: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                   right: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                   bottom: Annotated[int, intUi(min_value=0, max_value=500)] = 0,
                   reuse_buffer: bool = True
                   ) -> Annotated[str, imageFileReturn]:
    
    path = "./assets/crop_margins_test.png"
    
    # Cargar la imagen de origen
    src_image = load_image(image)
    
    # Ajustar márgenes para que no excedan las dimensiones de la imagen
    max_width = src_image.width - 1
    max_height = src_image.height - 1
    
    left = min(left, max_width - right)
    right = min(right, max_width - left)
    top = min(top, max_height - bottom)
    bottom = min(bottom, max_height - top)
    
    # Calcular dimensiones resultantes
    new_width = src_image.width - left - right
    new_height = src_image.height - top - bottom
    
    # Variable para mantener el buffer entre llamadas
    if not hasattr(crop_margins_ui, "buffer") or not reuse_buffer:
        crop_margins_ui.buffer = None
    else:
        # Verificar si el buffer existente necesita ser redimensionado
        if (crop_margins_ui.buffer is not None and 
            (crop_margins_ui.buffer.width != new_width or crop_margins_ui.buffer.height != new_height)):
            crop_margins_ui.buffer.free()
            crop_margins_ui.buffer = None
    
    # Crear un nuevo buffer si es necesario
    if crop_margins_ui.buffer is None:
        crop_margins_ui.buffer = CudaImage(new_width, new_height)
    
    # Realizar el recorte
    result = crop_margins(src_image, left, top, right, bottom, crop_margins_ui.buffer)
    
    # Guardar la imagen recortada
    save_image(result, path)
    
    # Liberar memoria de la imagen fuente
    src_image.free()
    
    return path

App(crop_margins_ui)