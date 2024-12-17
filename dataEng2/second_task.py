import numpy as np
import os

matrix = np.load('second_task.npy')
x = []
y = []
z = []

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] > 529:
            x.append(i)
            y.append(j)
            z.append(matrix[i, j])

x = np.array(x)
y = np.array(y)
z = np.array(z)

np.savez('arrays.npz', x=x, y=y, z=z)
np.savez_compressed('arrays_compressed.npz', x=x, y=y, z=z)

size_uncompressed = os.path.getsize('arrays.npz')
size_compressed = os.path.getsize('arrays_compressed.npz')

print(f"Размер несжатого файла: {size_uncompressed} байт")
print(f"Размер сжатого файла: {size_compressed} байт")
