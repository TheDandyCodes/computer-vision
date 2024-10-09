import numpy as np

random_matrix = np.random.rand(3, 3)
simetric_matrix = (random_matrix + random_matrix.T)/2
print(simetric_matrix)