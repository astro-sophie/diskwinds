import numpy as np
wavelengths = np.linspace(4.69105, 4.69145, 10)
center_wavelengths = [(wavelengths[i+1]-wavelengths[i]) for i in range(0, len(wavelengths)-1)]
dlambda = np.diff(wavelengths)
print(dlambda)
