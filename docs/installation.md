
# PhotoFF Installation Guide (Linux & Windows)

## Prerequisites

Before installing PhotoFF, ensure you have the following prerequisites:

- **Python 3.9 or newer**
- **NVIDIA GPU with CUDA support**
- **CUDA Toolkit 11.0 or newer** – Required for compiling the CUDA components
- **CFFI** – Used for interfacing between Python and the CUDA library
- **Pillow** – Used for image loading, saving, and text rendering

---

## Python Dependencies

Install the required Python packages:

```bash
pip install cffi pillow
```

---

## Installing CUDA Toolkit

1. Download the CUDA Toolkit from the [NVIDIA Developer website](https://developer.nvidia.com/cuda-downloads)
2. Follow the instructions for your OS (Linux or Windows)
3. Ensure `nvcc` is accessible:
   ```bash
   nvcc --version
   ```

---

## Compiling the CUDA Library

### 🐧 For Linux:

1. Clone the repository:
   ```bash
   git clone https://github.com/offerrall/photoff.git
   cd photoff
   ```

2. Compile the `.so` shared object:
   ```bash
   python3 photoff_cuda_src/compile_linux.py
   ```

3. You’ll get `photoff.so`.

4. Make it available to your system:

   Add to `~/.bashrc` or `~/.zshrc`:
   ```bash
   export LD_LIBRARY_PATH=/your/path/photoff:$LD_LIBRARY_PATH
   ```
   Replace `/your/path/photoff` with the actual path where `photoff.so` is located.
   Then run:
   ```bash
   source ~/.bashrc
   ```
   or
   ```bash
   source ~/.zshrc
   ```

---

### 🪟 For Windows:

1. Clone the repository:
   ```powershell
   git clone https://github.com/offerrall/photoff.git
   cd photoff
   ```

2. Compile the `.dll` using:
   ```powershell
   python photoff_cuda_src/compile_windows.py
   ```

3. Add the folder containing `photoff.dll` to your system PATH:
   - Search for “Environment Variables” in the Start menu
   - Edit the PATH variable, and add the folder path
   - Restart your terminal or IDE

---

## Installing the Python Package

Run this in the root of the project (after compilation):

```bash
pip install .
```

---

## Verifying the Installation

Test your installation with the following Python script:

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

If you see the image `red_square.png` and the message “Installation successful!”, your setup is working.

---

## Notes
- CFFI will load the appropriate file based on your OS

---

## License

PhotoFF is distributed under the MIT license.