from dataclasses import dataclass as _dataclass
from typing import Any as _Any

@_dataclass
class CudaBuffer:
    buffer: _Any = None

@_dataclass
class CudaImage:
    width: int
    height: int
    buffer: CudaBuffer = None

@_dataclass
class RGBA:
    r: int
    g: int
    b: int
    a: int = 255