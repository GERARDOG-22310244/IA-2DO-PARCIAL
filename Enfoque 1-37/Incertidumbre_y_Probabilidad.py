import random
import numpy as np
from collections import Counter

# 1. Probabilidad básica - Lanzamiento de moneda
def lanzamiento_moneda(n=1):
    """
    Simula el lanzamiento de una moneda n veces
    Devuelve una lista de resultados (Cara o Cruz)
    """
    resultados = []
    for _ in range(n):
        resultado = random.choice(['Cara', 'Cruz'])
        resultados.append(resultado)
    return resultados

# 2. Probabilidad empírica
def probabilidad_empirica(eventos, evento_deseado):
    """
    Calcula la probabilidad empírica de un evento
    eventos: lista de eventos observados
    evento_deseado: el evento cuya probabilidad queremos calcular
    """
    ocurrencias = eventos.count(evento_deseado)
    return ocurrencias / len(eventos)

# 3. Distribución de probabilidad
def distribucion_probabilidad(eventos):
    """
    Calcula la distribución de probabilidad para un conjunto de eventos
    Devuelve un diccionario con cada evento y su probabilidad
    """
    contador = Counter(eventos)
    total = len(eventos)
    return {evento: cuenta/total for evento, cuenta in contador.items()}

# 4. Incertidumbre con Distribución Normal
def incertidumbre_normal(media, desviacion, n=1000):
    """
    Simula valores con incertidumbre usando distribución normal
    Devuelve una muestra de n valores aleatorios
    """
    return np.random.normal(media, desviacion, n)

# 5. Teorema de Bayes
def teorema_bayes(p_a, p_b_dado_a, p_b_dado_no_a):
    """
    Calcula P(A|B) usando el teorema de Bayes
    p_a: P(A)
    p_b_dado_a: P(B|A)
    p_b_dado_no_a: P(B|¬A)
    """
    p_no_a = 1 - p_a
    p_b = (p_b_dado_a * p_a) + (p_b_dado_no_a * p_no_a)
    return (p_b_dado_a * p_a) / p_b

# Ejemplos de uso
if __name__ == "__main__":
    print("\n1. Lanzamiento de moneda (10 veces):")
    lanzamientos = lanzamiento_moneda(10)
    print(lanzamientos)
    
    print("\n2. Probabilidad empírica de Cara:")
    prob_cara = probabilidad_empirica(lanzamientos, 'Cara')
    print(f"P(Cara) = {prob_cara:.2f}")
    
    print("\n3. Distribución de probabilidad:")
    distribucion = distribucion_probabilidad(lanzamientos)
    for evento, prob in distribucion.items():
        print(f"P({evento}) = {prob:.2f}")
    
    print("\n4. Incertidumbre con distribución normal (media=5, desv=2):")
    valores = incertidumbre_normal(5, 2, 10)
    print(valores)
    
    print("\n5. Teorema de Bayes (P(A)=0.1, P(B|A)=0.9, P(B|¬A)=0.2):")
    p_a_dado_b = teorema_bayes(0.1, 0.9, 0.2)
    print(f"P(A|B) = {p_a_dado_b:.4f}")