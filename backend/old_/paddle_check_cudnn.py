import paddle
print("Paddle compiled with CUDNN version:", paddle.version.cudnn())
print("Paddle is using GPU:", paddle.is_compiled_with_cuda())
import os
print(os.environ["PATH"])

import os
from glob import glob
import ctypes

dlls = []
for folder in os.environ["PATH"].split(";"):
    for f in glob(folder + "\\cudnn64_*.dll"):
        dlls.append(f)

print("FOUND DLL FILES:")
for dll in dlls:
    print(" -", dll)

print("\nVERSIONS:")
for dll in dlls:
    try:
        lib = ctypes.cdll.LoadLibrary(dll)
        v = lib.cudnnGetVersion()
        print(dll, "VERSION:", v)
    except Exception as e:
        print(dll, "→ ERROR loading:", e)

import sys
import os
import glob

paddle_path = None
for p in sys.path:
    if "paddle" in p and "site-packages" in p:
        paddle_path = p

print("Paddle path:", paddle_path)

libs = glob.glob(os.path.join(paddle_path, "libs", "*cudnn*"))
print("Internal Paddle libs:")
for lib in libs:
    print(" -", lib)
