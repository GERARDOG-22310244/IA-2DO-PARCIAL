class QLearningWithExploration:
    def __init__(self, actions, exploration_strategy='epsilon_greedy', **kwargs):
        self.actions = actions
        self.exploration_strategy = exploration_strategy
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.action_counts = defaultdict(lambda: np.zeros(len(actions)))
        
        # Parámetros de estrategias de exploración
        self.epsilon = kwargs.get('epsilon', 0.1)
        self.epsilon_decay = kwargs.get('epsilon_decay', 0.995)
        self.epsilon_min = kwargs.get('epsilon_min', 0.01)
        self.c = kwargs.get('c', 2)  # Para UCB
        self.temperature = kwargs.get('temperature', 1.0)  # Para Softmax
        self.step_count = 0
    
    def select_action(self, state):
        """Selecciona acción según la estrategia de exploración"""
        self.step_count += 1
        q_values = self.q_table[state]
        action_counts = self.action_counts[state]
        
        if self.exploration_strategy == 'epsilon_greedy':
            if np.random.random() < self.epsilon:
                return np.random.choice(self.actions)  # Exploración
            return self.actions[np.argmax(q_values)]  # Explotación
        
        elif self.exploration_strategy == 'ucb':
            # Upper Confidence Bound
            total_counts = np.sum(action_counts)
            if total_counts == 0:
                return np.random.choice(self.actions)
            ucb = q_values + self.c * np.sqrt(np.log(total_counts) / (action_counts + 1e-5))
            return self.actions[np.argmax(ucb)]
        
        elif self.exploration_strategy == 'softmax':
            # Softmax (Boltzmann)
            exp_q = np.exp(q_values / self.temperature)
            probs = exp_q / np.sum(exp_q)
            return np.random.choice(self.actions, p=probs)
        
        else:
            raise ValueError("Estrategia de exploración no válida")
    
    def update(self, state, action, reward, next_state, done):
        """Actualiza Q-values usando Q-learning"""
        action_idx = self.actions.index(action)
        self.action_counts[state][action_idx] += 1
        
        # Q-learning update
        current_q = self.q_table[state][action_idx]
        next_max = np.max(self.q_table[next_state]) if not done else 0
        target = reward + self.gamma * next_max
        self.q_table[state][action_idx] += self.alpha * (target - current_q)
        
        # Decaimiento de epsilon (para epsilon-greedy)
        if self.exploration_strategy == 'epsilon_greedy':
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def set_hyperparameters(self, alpha=0.1, gamma=0.9):
        self.alpha = alpha
        self.gamma = gamma