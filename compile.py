import subprocess
import os

lib_name = "photoff"

def compile_cuda_dll():

    # delete the previous dll
    if os.path.exists(f"./{lib_name}.dll"):
        os.remove(f"./{lib_name}.dll")

    source_file = f"./cuda_src/{lib_name}.cu"
    output_dll = f"./{lib_name}.dll"
    
    command = ["nvcc",
               "--shared",
               source_file,
               "-o", output_dll,
               "-Xcompiler", "/MD"
               ]
    
    print("Ejecutando comando:")
    print(" ".join(command))
    
    try:
        subprocess.check_call(command)
        print("DLL compilado con éxito en:")
        print(output_dll)
    except subprocess.CalledProcessError as e:
        print("Error en la compilación:")
        print(e)
    
    # Delete the intermediate files
    os.remove(f"./{lib_name}.exp")
    os.remove(f"./{lib_name}.lib")

if __name__ == "__main__":
    compile_cuda_dll()
