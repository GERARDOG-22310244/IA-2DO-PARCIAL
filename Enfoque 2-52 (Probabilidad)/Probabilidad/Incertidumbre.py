import random
import matplotlib.pyplot as plt

# Simulamos lanzar un dado justo de 6 caras N veces
def lanzar_dado(n_lanzamientos=1000):
    resultados = [random.randint(1, 6) for _ in range(n_lanzamientos)]
    return resultados

# Calculamos la frecuencia de cada resultado
def calcular_frecuencias(resultados):
    frecuencias = {i: 0 for i in range(1, 7)}
    for resultado in resultados:
        frecuencias[resultado] += 1
    return frecuencias

# Visualización
def graficar_probabilidades(frecuencias, total_lanzamientos):
    caras = list(frecuencias.keys())
    probabilidades = [frecuencias[cara] / total_lanzamientos for cara in caras]

    plt.bar(caras, probabilidades, color='skyblue', edgecolor='black')
    plt.xlabel('Cara del dado')
    plt.ylabel('Probabilidad estimada')
    plt.title('Probabilidad de cada cara del dado (simulación)')
    plt.ylim(0, 0.3)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Parámetros
N = 10000  # número de lanzamientos
resultados = lanzar_dado(N)
frecuencias = calcular_frecuencias(resultados)

# Mostrar resultados
print("Probabilidades estimadas:")
for cara, frecuencia in frecuencias.items():
    print(f"Cara {cara}: {frecuencia / N:.4f}")

# Graficar
graficar_probabilidades(frecuencias, N)
