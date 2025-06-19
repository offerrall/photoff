import subprocess
import os

lib_name = "photoff"


def compile_cuda_so():

    output_so = f"./{lib_name}.so"
    if os.path.exists(output_so):
        os.remove(output_so)

    source_file = f"./photoff_cuda_src/{lib_name}.cu"

    command = ["nvcc", "--shared", source_file, "-o", output_so, "-Xcompiler", "-fPIC"]

    print("Running command:")
    print(" ".join(command))

    try:
        subprocess.check_call(command)
        print("Shared object successfully compiled at:")
        print(output_so)
    except subprocess.CalledProcessError as e:
        print("Compilation error:")
        print(e)


if __name__ == "__main__":
    compile_cuda_so()
