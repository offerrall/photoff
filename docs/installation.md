# PhotoFF Installation Guide

## Prerequisites

Before installing PhotoFF, ensure you have the following prerequisites:

- **Python 3.9 or newer**
- **NVIDIA GPU with CUDA support**
- **CUDA Toolkit 11.0 or newer** - Required for compiling the CUDA components
- **Visual Studio with C++ support** (Windows) - Required for the CUDA compiler
- **CFFI** - Used for interfacing between Python and the CUDA library
- **Pillow** - Used for I/O operations and text rendering
- **NumPy** - Used only for memory management when transferring images from Pillow to CUDA

## Python Dependencies

Install the required Python packages:

```bash
pip install cffi pillow numpy
```

Note:
- **CFFI** is essential for PhotoFF as it provides the bridge between Python and the CUDA-accelerated DLL
- **Pillow** is used for loading and saving images, as well as text rendering functions
- **NumPy** is only used for efficient memory management when transferring image data between Pillow and CUDA buffers

## Installing CUDA Toolkit

1. Download the CUDA Toolkit from the [NVIDIA Developer website](https://developer.nvidia.com/cuda-downloads)
2. Follow the installation instructions for your operating system
3. Make sure the CUDA binaries are in your system PATH (this usually happens automatically during installation)
4. Verify your installation by running `nvcc --version` in your terminal

## Install from Source

This method builds and installs the package from source code:

1. Clone the repository:
   ```bash
   git clone https://github.com/offerrall/photoff.git
   cd photoff
   ```

2. Compile the CUDA DLL:
   ```bash
   python photoff_cuda_src/compile.py
   ```

3. Move the compiled `photoff.dll` to a directory in your system PATH or add the directory containing the DLL to your PATH environment variable.

4. Install the Python package:
   ```bash
   pip install .
   ```

## Verifying the Installation

To verify your installation, run the following Python code:

```python
from photoff.operations.fill import fill_color
from photoff.io import save_image
from photoff.core.types import CudaImage, RGBA

# Create a 200x200 red square
img = CudaImage(200, 200)
fill_color(img, RGBA(255, 0, 0, 255))
save_image(img, "red_square.png")
img.free()

print("Installation successful!")
```

If you see a 200x200 red square image saved as "red_square.png" and the message "Installation successful!" printed to the console, your installation is working correctly.