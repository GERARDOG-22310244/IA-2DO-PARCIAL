class MonteCarlo:
    def __init__(self, mdp):
        self.mdp = mdp
        self.returns = {s: [] for s in mdp.estados}
        self.V = {s: 0 for s in mdp.estados}
    
    def generar_episodio(self, politica):
        episodio = []
        s = np.random.choice(self.mdp.estados[:-1])  # No empezar en estado terminal
        
        while s != 'D':  # Asumiendo que 'D' es el estado terminal
            a = politica[s]
            transiciones = self.mdp.transiciones[s][a]
            probs = [t[0] for t in transiciones]
            indices = range(len(transiciones))
            idx = np.random.choice(indices, p=probs)
            prob, s_prima, recompensa = transiciones[idx]
            episodio.append((s, a, recompensa))
            s = s_prima
        
        return episodio
    
    def evaluacion_politica_mc(self, politica, num_episodios=1000):
        for _ in range(num_episodios):
            episodio = self.generar_episodio(politica)
            G = 0
            visitados = set()
            
            for t in reversed(range(len(episodio))):
                s, a, r = episodio[t]
                G = self.mdp.gamma * G + r
                
                if s not in visitados:
                    self.returns[s].append(G)
                    self.V[s] = np.mean(self.returns[s])
                    visitados.add(s)
        
        return self.V

# Ejemplo de uso
mc = MonteCarlo(mdp)
valores_mc = mc.evaluacion_politica_mc(politica, num_episodios=10000)

print("\nEvaluación de Política con Monte Carlo:")
for estado, valor in valores_mc.items():
    print(f"V({estado}) = {valor:.2f}")