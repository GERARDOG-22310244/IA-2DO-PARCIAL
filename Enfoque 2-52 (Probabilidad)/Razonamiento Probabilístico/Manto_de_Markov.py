from pgmpy.models import BayesianNetwork
from pgmpy.utils import get_example_model

# Crear red bayesiana: A → B → D, A → C → D
modelo = BayesianNetwork([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])

# Función para obtener el manto de Markov de un nodo
def obtener_manto_de_markov(modelo, nodo):
    manto = set()
    
    # Padres del nodo
    padres = set(modelo.get_parents(nodo))
    manto.update(padres)
    
    # Hijos del nodo
    hijos = set(modelo.get_children(nodo))
    manto.update(hijos)
    
    # Padres de los hijos
    for hijo in hijos:
        manto.update(modelo.get_parents(hijo))
    
    # Eliminar el nodo en sí
    manto.discard(nodo)
    
    return manto

# Nodo de interés
nodo = "B"
manto_B = obtener_manto_de_markov(modelo, nodo)

print(f"Manto de Markov de '{nodo}': {manto_B}")
