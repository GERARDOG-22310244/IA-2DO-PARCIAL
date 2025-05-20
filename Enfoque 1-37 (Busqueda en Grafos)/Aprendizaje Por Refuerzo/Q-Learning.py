import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Inicializa el agente Q-Learning
        
        Parámetros:
        - actions: lista de acciones posibles
        - alpha: tasa de aprendizaje (0 < alpha <= 1)
        - gamma: factor de descuento (0 < gamma <= 1)
        - epsilon: probabilidad de exploración (0 < epsilon < 1)
        """
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
    
    def get_action(self, state):
        """
        Selecciona una acción usando política ε-greedy
        
        Args:
        - state: estado actual del entorno
        
        Returns:
        - acción seleccionada
        """
        if random.random() < self.epsilon:
            # Exploración: acción aleatoria
            return random.choice(self.actions)
        else:
            # Explotación: mejor acción según Q-table
            return self.actions[np.argmax(self.q_table[state])]
    
    def learn(self, state, action, reward, next_state, done):
        """
        Actualiza la Q-table usando la regla de Q-Learning
        
        Args:
        - state: estado actual
        - action: acción tomada
        - reward: recompensa recibida
        - next_state: siguiente estado
        - done: si el episodio ha terminado
        """
        current_q = self.q_table[state][self.actions.index(action)]
        
        if done:
            # Si es terminal, no hay siguiente estado
            target = reward
        else:
            # Q-learning: usa el máximo Q-value del siguiente estado
            next_max = np.max(self.q_table[next_state])
            target = reward + self.gamma * next_max
        
        # Actualización de Q-value
        self.q_table[state][self.actions.index(action)] += self.alpha * (target - current_q)

    def get_policy(self):
        """Obtiene la política aprendida (acción óptima para cada estado)"""
        policy = {}
        for state in self.q_table:
            policy[state] = self.actions[np.argmax(self.q_table[state])]
        return policy

    def get_q_values(self):
        """Obtiene todos los valores Q aprendidos"""
        return dict(self.q_table)