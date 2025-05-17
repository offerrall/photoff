from dataclasses import dataclass as _dataclass
from typing import Any as CudaBuffer
from .buffer import create_buffer, free_buffer


@_dataclass
class RGBA:
    r: int
    g: int
    b: int
    a: int = 255


class CudaImage:

    def __init__(self, width: int, height: int, auto_init: bool = True):

        self._alloc_width  = width
        self._alloc_height = height

        self._width  = width
        self._height = height

        self.buffer = None
        if auto_init:
            self.init_image()

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        if value > self._alloc_width:
            raise ValueError(
                f"width {value} > alloc_width {self._alloc_width}"
            )
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        if value > self._alloc_height:
            raise ValueError(
                f"height {value} > alloc_height {self._alloc_height}"
            )
        self._height = value

    def init_image(self):
        if self.buffer is None:
            self.buffer = create_buffer(self._alloc_width, self._alloc_height)

    def free(self):
        if self.buffer is not None:
            free_buffer(self.buffer)
            self.buffer = None
