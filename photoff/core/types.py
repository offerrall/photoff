from dataclasses import dataclass as _dataclass
from .buffer import create_buffer, free_buffer


@_dataclass
class RGBA:
    """
    Represents an RGBA color with 8-bit channels.

    Attributes:
        r (int): Red channel (0 – 255).
        g (int): Green channel (0 – 255).
        b (int): Blue channel (0 – 255).
        a (int): Alpha channel (0 – 255), defaults to 255 (opaque).

    Example:
        >>> color = RGBA(255, 0, 0)  # Opaque red
        >>> transparent_black = RGBA(0, 0, 0, 0)
    """
    r: int
    g: int
    b: int
    a: int = 255



class CudaImage:
    """
    Represents an image stored in GPU memory with optional dimension constraints.

    The image has an underlying GPU buffer and stores its logical and allocated dimensions.
    Use `.width` and `.height` to manage the actual used size, while the allocation
    size is fixed on creation. Memory is managed via `create_buffer` and `free_buffer`.

    Attributes:
        width (int): Logical width (can be set lower than allocated width).
        height (int): Logical height (can be set lower than allocated height).
        buffer (CudaBuffer): Pointer to the underlying CUDA buffer.

    Methods:
        init_image(): Allocates the GPU buffer if not already allocated.
        free(): Frees the associated GPU buffer.

    Example:
        >>> img = CudaImage(512, 512)
        >>> img.width = 256  # Use only part of the allocation
        >>> img.free()
    """

    def __init__(self, width: int, height: int, auto_init: bool = True):
        """
        Initializes a new CudaImage with specified dimensions.

        Args:
            width (int): Allocation and initial logical width in pixels.
            height (int): Allocation and initial logical height in pixels.
            auto_init (bool, optional): Whether to automatically allocate the buffer. Defaults to True.
        """

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
            raise ValueError(f"width {value} > alloc_width {self._alloc_width}")
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        if value > self._alloc_height:
            raise ValueError(f"height {value} > alloc_height {self._alloc_height}")
        self._height = value

    def init_image(self):
        if self.buffer is None:
            self.buffer = create_buffer(self._alloc_width, self._alloc_height)

    def free(self):
        if self.buffer is not None:
            free_buffer(self.buffer)
            self.buffer = None