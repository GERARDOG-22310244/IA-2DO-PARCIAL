# Definimos el espacio muestral y evento
espacio_muestral = [1, 2, 3, 4, 5, 6]  # dado de 6 caras

# Evento A: obtener un número par
evento_A = [2, 4, 6]

# Cálculo de probabilidad a priori
probabilidad_a_priori = len(evento_A) / len(espacio_muestral)

# Mostrar resultado
print("Espacio muestral:", espacio_muestral)
print("Evento A (número par):", evento_A)
print(f"Probabilidad a priori de A: {probabilidad_a_priori:.4f}")
