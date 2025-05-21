import matplotlib.pyplot as plt

# Espacio muestral del dado
valores = [1, 2, 3, 4, 5, 6]

# Distribución de probabilidad (dado justo: todas con la misma probabilidad)
probabilidades = [1/6 for _ in valores]

# Mostrar distribución
for valor, prob in zip(valores, probabilidades):
    print(f"P(X = {valor}) = {prob:.3f}")

# Graficar la distribución de probabilidad
plt.bar(valores, probabilidades, color='skyblue', edgecolor='black')
plt.xlabel("Valor del dado (X)")
plt.ylabel("Probabilidad P(X)")
plt.title("Distribución de Probabilidad Discreta: Dado Justo")
plt.ylim(0, 0.25)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.show()
