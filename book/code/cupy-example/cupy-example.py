import numpy as np
import cupy as cp

# Array APIs are the same though operating on different hardware devices
x_cpu = np.array([1, 2, 3])
x_gpu = cp.array([1, 2, 3])

l2_cpu = np.linalg.norm(x_cpu)
l2_gpu = cp.linalg.norm(x_gpu)

print(f"NumPy array {l2_cpu} on device: {x_cpu.device}")
print(f"CuPy array {l2_gpu} on device: {x_gpu.device}")
