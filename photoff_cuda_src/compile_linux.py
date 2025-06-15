import subprocess
import os

lib_name = "photoff"


def compile_cuda_so():
    # delete the previous .so
    output_so = f"./{lib_name}.so"
    if os.path.exists(output_so):
        os.remove(output_so)

    source_file = f"./photoff_cuda_src/{lib_name}.cu"

    command = [
        "nvcc", "--shared", source_file, "-o", output_so, "-Xcompiler", "-fPIC"
    ]

    print("Ejecutando comando:")
    print(" ".join(command))

    try:
        subprocess.check_call(command)
        print("SO compilado con éxito en:")
        print(output_so)
    except subprocess.CalledProcessError as e:
        print("Error en la compilación:")
        print(e)


if __name__ == "__main__":
    compile_cuda_so()
