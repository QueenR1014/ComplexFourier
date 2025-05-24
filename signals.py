import numpy as np
import matplotlib.pyplot as plt
np.random.seed(42)

#Creación de senos  aleatorios
# f(t) = sin(\omega t + \Phi)

parameters = [] 
for i in range(5):
    A = np.random.rand()
    omega = np.random.uniform(0.1,10)
    phi = np.random.uniform(0,2*np.pi)
    parameters.append((A,omega,phi))

print("Parámetros de Funciones Sinusoidales")
print(*parameters)

signal = []

for fun in parameters:
    np.lin