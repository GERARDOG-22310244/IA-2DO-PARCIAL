import tensorflow as tf
from collections import deque
import random

class DQNAgent:
    def __init__(self, estado_dim, accion_dim):
        self.estado_dim = estado_dim
        self.accion_dim = accion_dim
        self.memoria = deque(maxlen=2000)
        self.gamma = 0.95  # Factor de descuento
        self.epsilon = 1.0  # Exploración inicial
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.modelo = self._construir_modelo()
    
    def _construir_modelo(self):
        """Construye una red neuronal simple"""
        modelo = tf.keras.Sequential([
            tf.keras.layers.Dense(24, input_dim=self.estado_dim, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.accion_dim, activation='linear')
        ])
        modelo.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return modelo
    
    def memorizar(self, estado, accion, recompensa, estado_siguiente, terminado):
        self.memoria.append((estado, accion, recompensa, estado_siguiente, terminado))
    
    def elegir_accion(self, estado):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.accion_dim)
        estado = np.array(estado).reshape(1, -1)
        act_values = self.modelo.predict(estado, verbose=0)
        return np.argmax(act_values[0])
    
    def entrenar(self, batch_size=32):
        if len(self.memoria) < batch_size:
            return
        
        minibatch = random.sample(self.memoria, batch_size)
        estados = np.array([t[0] for t in minibatch])
        acciones = np.array([t[1] for t in minibatch])
        recompensas = np.array([t[2] for t in minibatch])
        estados_siguientes = np.array([t[3] for t in minibatch])
        terminados = np.array([t[4] for t in minibatch])
        
        objetivos = self.modelo.predict(estados, verbose=0)
        Q_futuros = np.max(self.modelo.predict(estados_siguientes, verbose=0), axis=1)
        
        for i in range(batch_size):
            if terminados[i]:
                objetivos[i][acciones[i]] = recompensas[i]
            else:
                objetivos[i][acciones[i]] = recompensas[i] + self.gamma * Q_futuros[i]
        
        self.modelo.fit(estados, objetivos, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Ejemplo simplificado de uso de DQN
# (Nota: Requiere adaptación para el GridWorld anterior)
estado_dim = 2  # (x, y)
accion_dim = 4  # N, S, E, O

dqn_agent = DQNAgent(estado_dim, accion_dim)

# Aquí iría el bucle de entrenamiento interactuando con el entorno
# Para simplificar, no lo incluimos completo en este ejemplo