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
    width: int
    height: int
    buffer: CudaBuffer

    def __init__(self, width: int, height: int, auto_init: bool = True):
        self.width = width
        self.height = height
        self.buffer: CudaBuffer = None

        self._original_width = width
        self._original_height = height

        if auto_init:
            self.init_image()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        if value > self._alloc_width:
            raise ValueError(f"width {value} is greater than allocated width {self._alloc_width}")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        if value > self._alloc_height:
            raise ValueError(f"height {value} is greater than allocated height {self._alloc_height}")
        self._height = value

    def init_image(self):
        self.buffer = create_buffer(self.width, self.height)

    def free(self):
        if self.buffer is None:
            return
        free_buffer(self.buffer)
        self.buffer = None
    