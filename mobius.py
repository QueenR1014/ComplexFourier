import numpy as np

t = np.linspace(-np.pi, np.pi, 1000)

z = np.exp(1j*t)

f_z = z / (z-2)

