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
        if auto_init:
            self.init_image()

    def init_image(self):
        self.buffer = create_buffer(self.width, self.height)

    def free(self):
        if self.buffer is None:
            return
        free_buffer(self.buffer)
        self.buffer = None
