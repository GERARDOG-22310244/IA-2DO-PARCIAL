import numpy as np
from collections import defaultdict

class PolicyIteration:
    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9):
        """
        Inicializa el algoritmo de iteración de política
        
        Args:
            estados: lista de estados posibles
            acciones: lista de acciones posibles
            transiciones: dict[estado][accion] = [(prob, s', recompensa), ...]
            recompensas: dict[estado] = recompensa
            gamma: factor de descuento
        """
        self.estados = estados
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.gamma = gamma
        
        # Inicializar política aleatoria
        self.politica = {s: np.random.choice(acciones) for s in estados}
        
        # Inicializar valores
        self.V = {s: 0 for s in estados}
    
    def evaluacion_politica(self, theta=1e-6):
        """Evalúa la política actual hasta convergencia"""
        while True:
            delta = 0
            for s in self.estados:
                v = self.V[s]
                a = self.politica[s]
                
                # Calcular nuevo valor para el estado
                nuevo_valor = 0
                for prob, s_prima, r in self.transiciones[s][a]:
                    nuevo_valor += prob * (r + self.gamma * self.V[s_prima])
                
                self.V[s] = nuevo_valor
                delta = max(delta, abs(v - self.V[s]))
            
            if delta < theta:
                break
    
    def mejora_politica(self):
        """Mejora la política basada en los valores actuales"""
        politica_estable = True
        
        for s in self.estados:
            accion_actual = self.politica[s]
            
            # Calcular Q-values para todas las acciones
            q_values = []
            for a in self.acciones:
                q = 0
                for prob, s_prima, r in self.transiciones[s][a]:
                    q += prob * (r + self.gamma * self.V[s_prima])
                q_values.append(q)
            
            # Seleccionar la mejor acción
            mejor_accion = self.acciones[np.argmax(q_values)]
            
            # Actualizar política
            if mejor_accion != accion_actual:
                self.politica[s] = mejor_accion
                politica_estable = False
        
        return politica_estable
    
    def iterar(self, max_iter=100):
        """Ejecuta iteración de política hasta convergencia"""
        for i in range(max_iter):
            self.evaluacion_politica()
            politica_estable = self.mejora_politica()
            
            if politica_estable:
                print(f"Convergencia alcanzada en iteración {i+1}")
                break
        
        return self.politica, self.V