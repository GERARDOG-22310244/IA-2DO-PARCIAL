from collections import defaultdict
from sympy import symbols, And, Or, Not, Implies, Equivalent
from sympy.logic.inference import satisfiable
from itertools import product
import random

## ----------------------------
## 1. Sistema de Aprendizaje Basado en Reglas
## ----------------------------

class SistemaReglas:
    def __init__(self):
        self.reglas = []
        self.hechos = set()
        self.hipotesis = set()
    
    def agregar_regla(self, antecedente, consecuente):
        """Agrega una regla al sistema"""
        self.reglas.append((antecedente, consecuente))
    
    def agregar_hecho(self, hecho):
        """Agrega un hecho observado"""
        self.hechos.add(hecho)
    
    def encadenamiento_adelante(self):
        """Motor de inferencia hacia adelante"""
        nuevos_hechos = True
        while nuevos_hechos:
            nuevos_hechos = False
            for antecedente, consecuente in self.reglas:
                if antecedente.issubset(self.hechos) and consecuente not in self.hechos:
                    self.hechos.add(consecuente)
                    nuevos_hechos = True
    
    def generar_hipotesis(self, posibles_hipotesis):
        """Genera hipótesis basadas en los hechos"""
        self.hipotesis = set()
        for h in posibles_hipotesis:
            if h in self.hechos:
                self.hipotesis.add(h)
    
    def aprender_nueva_regla(self, min_confianza=0.7):
        """Aprende nuevas reglas basadas en patrones"""
        # Contar co-ocurrencias (simplificado)
        conteo = defaultdict(int)
        for hecho in self.hechos:
            if isinstance(hecho, tuple) and len(hecho) == 2:
                a, b = hecho
                conteo[(a, b)] += 1
        
        # Generar reglas potenciales
        for (a, b), count in conteo.items():
            total_a = sum(1 for h in self.hechos if h[0] == a)
            confianza = count / total_a if total_a > 0 else 0
            
            if confianza >= min_confianza:
                nueva_regla = (frozenset([a]), b)
                if nueva_regla not in self.reglas:
                    self.reglas.append(nueva_regla)
                    print(f"Aprendida nueva regla: {a} => {b} (confianza: {confianza:.2f})")

## ----------------------------
## 2. Aprendizaje Basado en Casos
## ----------------------------

class SistemaCBR:
    def __init__(self):
        self.casos = []
        self.soluciones = []
    
    def agregar_caso(self, caracteristicas, solucion):
        """Agrega un caso a la base de conocimiento"""
        self.casos.append(caracteristicas)
        self.soluciones.append(solucion)
    
    def recuperar_caso_similar(self, nuevo_caso, k=1):
        """Recupera los k casos más similares"""
        # Medida de similitud simplificada (distancia Hamming)
        def similitud(c1, c2):
            comunes = set(c1.items()) & set(c2.items())
            return len(comunes) / max(len(c1), len(c2))
        
        similitudes = []
        for i, caso in enumerate(self.casos):
            sim = similitud(nuevo_caso, caso)
            similitudes.append((sim, i))
        
        # Ordenar por similitud y tomar los top k
        similitudes.sort(reverse=True)
        return [self.soluciones[i] for (_, i) in similitudes[:k]]
    
    def adaptar_solucion(self, solucion, nuevo_caso):
        """Adapta una solución a un nuevo caso (simplificado)"""
        # En una implementación real, usaría reglas de adaptación
        return solucion  # Por ahora devuelve la solución sin cambios
    
    def resolver(self, nuevo_caso):
        """Resuelve un nuevo caso usando CBR"""
        if not self.casos:
            return None
        
        soluciones_similares = self.recuperar_caso_similar(nuevo_caso)
        mejor_solucion = soluciones_similares[0]
        return self.adaptar_solucion(mejor_solucion, nuevo_caso)

## ----------------------------
## 3. Aprendizaje Basado en Modelos Lógicos
## ----------------------------

class AprendizajeInductivo:
    def __init__(self):
        self.reglas_aprendidas = []
    
    def aprender_hipotesis(self, ejemplos_positivos, ejemplos_negativos, vocabulario):
        """Algoritmo FOIL simplificado para aprendizaje inductivo"""
        # Convertir ejemplos a conjuntos
        pos = set(ejemplos_positivos)
        neg = set(ejemplos_negativos)
        
        # Aprender reglas una por una
        while pos:
            # Crear una regla inicial (sin precondiciones)
            regla_actual = []
            cubiertos_pos = pos.copy()
            cubiertos_neg = neg.copy()
            
            # Añadir literales hasta que la regla sea consistente
            while cubiertos_neg:
                # Evaluar todos los literales posibles
                mejor_literal = None
                mejor_ganancia = -1
                mejor_cubiertos_pos = set()
                mejor_cubiertos_neg = set()
                
                for literal in vocabulario:
                    # Calcular cobertura del literal
                    nuevos_pos = {e for e in cubiertos_pos if literal in e}
                    nuevos_neg = {e for e in cubiertos_neg if literal in e}
                    
                    # Calcular ganancia de información (simplificada)
                    ganancia = len(nuevos_pos) - len(nuevos_neg)
                    
                    if ganancia > mejor_ganancia:
                        mejor_literal = literal
                        mejor_ganancia = ganancia
                        mejor_cubiertos_pos = nuevos_pos
                        mejor_cubiertos_neg = nuevos_neg
                
                if mejor_literal is None:
                    break  # No se puede mejorar más
                
                # Añadir el mejor literal a la regla
                regla_actual.append(mejor_literal)
                cubiertos_pos = mejor_cubiertos_pos
                cubiertos_neg = mejor_cubiertos_neg
            
            if regla_actual and cubiertos_pos:
                # Añadir la regla aprendida
                self.reglas_aprendidas.append(regla_actual)
                pos -= cubiertos_pos
            else:
                break
        
        return self.reglas_aprendidas

## ----------------------------
## Ejemplos de Uso
## ----------------------------

if __name__ == "__main__":
    print("=== Aprendizaje Basado en Reglas ===")
    sr = SistemaReglas()
    
    # Reglas iniciales
    sr.agregar_regla(frozenset(['pájaro', 'vuela_alto']), 'águila')
    sr.agregar_regla(frozenset(['pájaro', 'vuela_bajo']), 'pingüino')
    
    # Hechos observados
    sr.agregar_hecho('pájaro')
    sr.agregar_hecho('vuela_alto')
    sr.agregar_hecho(('pájaro', 'águila'))  # Ejemplo de co-ocurrencia
    
    # Inferencia y aprendizaje
    sr.encadenamiento_adelante()
    sr.generar_hipotesis(['águila', 'pingüino', 'halcón'])
    print("Hipótesis generadas:", sr.hipotesis)
    
    # Aprender nuevas reglas de los datos
    sr.agregar_hecho(('pájaro', 'vuela_alto'))
    sr.agregar_hecho(('pájaro', 'vuela_alto'))
    sr.agregar_hecho(('pájaro', 'vuela_bajo'))
    sr.aprender_nueva_regla()
    
    print("\n=== Aprendizaje Basado en Casos ===")
    cbr = SistemaCBR()
    
    # Casos históricos
    cbr.agregar_caso({'temperatura': 'alta', 'humedad': 'baja'}, 'deshidratación')
    cbr.agregar_caso({'temperatura': 'baja', 'humedad': 'alta'}, 'hipotermia')
    cbr.agregar_caso({'temperatura': 'media', 'humedad': 'media'}, 'normal')
    
    # Nuevo caso
    nuevo_caso = {'temperatura': 'alta', 'humedad': 'media'}
    solucion = cbr.resolver(nuevo_caso)
    print(f"Para {nuevo_caso}, solución sugerida: {solucion}")
    
    print("\n=== Aprendizaje Inductivo ===")
    ail = AprendizajeInductivo()
    
    # Ejemplos positivos y negativos
    positivos = [
        {'grande', 'verde', 'cuadrado'},  # Ejemplo 1
        {'grande', 'azul', 'redondo'},    # Ejemplo 2
        {'pequeño', 'rojo', 'cuadrado'}   # Ejemplo 3
    ]
    
    negativos = [
        {'pequeño', 'verde', 'triangular'},  # Contraejemplo 1
        {'grande', 'amarillo', 'redondo'}    # Contraejemplo 2
    ]
    
    # Vocabulario de características
    vocabulario = {'grande', 'pequeño', 'verde', 'azul', 'rojo', 'cuadrado', 'redondo', 'triangular'}
    
    # Aprender reglas
    reglas = ail.aprender_hipotesis(positivos, negativos, vocabulario)
    print("Reglas aprendidas:")
    for i, regla in enumerate(reglas, 1):
        print(f"Regla {i}: Si {' y '.join(regla)} entonces positivo")