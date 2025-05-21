import numpy as np
import matplotlib.pyplot as plt

# Función objetivo f(x) = sin(x) en [0, pi]
def f(x):
    return np.sin(x)

# Función CDF inversa para muestreo directo (CDF F(x) = 1 - cos(x))
def inv_cdf(u):
    return np.arccos(1 - u)

# Muestreo Directo
def muestreo_directo(n):
    u = np.random.uniform(0, 1, n)
    samples = inv_cdf(u)
    return samples

# Muestreo por Rechazo
def muestreo_rechazo(n):
    samples = []
    M = 1.0  # cota superior para f(x) en [0, pi]
    while len(samples) < n:
        x = np.random.uniform(0, np.pi)
        y = np.random.uniform(0, M)
        if y <= f(x):
            samples.append(x)
    return np.array(samples)

# Número de muestras
n_samples = 10000

# Obtener muestras
samples_directo = muestreo_directo(n_samples)
samples_rechazo = muestreo_rechazo(n_samples)

# Graficar histogramas
x = np.linspace(0, np.pi, 1000)
plt.plot(x, f(x)/2, label='Distribución objetivo (normalizada)')
plt.hist(samples_directo, bins=50, density=True, alpha=0.5, label='Muestreo Directo')
plt.hist(samples_rechazo, bins=50, density=True, alpha=0.5, label='Muestreo por Rechazo')
plt.legend()
plt.xlabel('x')
plt.ylabel('Densidad')
plt.title('Muestreo Directo vs Muestreo por Rechazo')
plt.show()
