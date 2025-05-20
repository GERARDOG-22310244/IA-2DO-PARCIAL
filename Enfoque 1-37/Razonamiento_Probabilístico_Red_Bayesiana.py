from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt

# 1. Definir la estructura de la red bayesiana
def crear_red_bayesiana():
    """
    Crea una red bayesiana simple con relaciones de dependencia
    Ejemplo: Clima -> Riego -> Hierba mojada
    """
    modelo = BayesianNetwork([('Clima', 'Riego'), 
                             ('Riego', 'HierbaMojada'),
                             ('Clima', 'HierbaMojada')])
    
    # 2. Definir las probabilidades condicionales (CPDs)
    cpd_clima = TabularCPD(variable='Clima', variable_card=2,
                          values=[[0.7], [0.3]],  # 70% soleado, 30% lluvioso
                          state_names={'Clima': ['Soleado', 'Lluvioso']})
    
    cpd_riego = TabularCPD(variable='Riego', variable_card=2,
                          values=[[0.9, 0.2],   # P(Riego|Clima)
                                 [0.1, 0.8]],
                          evidence=['Clima'],
                          evidence_card=[2],
                          state_names={'Riego': ['Apagado', 'Encendido'],
                                      'Clima': ['Soleado', 'Lluvioso']})
    
    cpd_hierba = TabularCPD(variable='HierbaMojada', variable_card=2,
                           values=[[0.8, 0.1, 0.1, 0.01],  # P(Hierba|Clima,Riego)
                                  [0.2, 0.9, 0.9, 0.99]],
                           evidence=['Clima', 'Riego'],
                           evidence_card=[2, 2],
                           state_names={'HierbaMojada': ['Seco', 'Mojado'],
                                       'Clima': ['Soleado', 'Lluvioso'],
                                       'Riego': ['Apagado', 'Encendido']})
    
    # Asociar los CPDs al modelo
    modelo.add_cpds(cpd_clima, cpd_riego, cpd_hierba)
    
    # Verificar si el modelo es válido
    if modelo.check_model():
        print("Red bayesiana válida")
    else:
        print("Red bayesiana inválida")
    
    return modelo

# 3. Visualización de la red
def visualizar_red(modelo):
    nx.draw(modelo, with_labels=True, node_size=2000, 
            node_color='skyblue', font_size=10, 
            arrowsize=20)
    plt.title("Red Bayesiana")
    plt.show()

# 4. Inferencia probabilística
def inferencia_bayesiana(modelo):
    inferencia = VariableElimination(modelo)
    
    # a. Probabilidad marginal
    print("\nProbabilidad marginal de Clima:")
    print(inferencia.query(variables=['Clima']))
    
    # b. Probabilidad condicional
    print("\nProbabilidad de Riego dado que la Hierba está mojada:")
    print(inferencia.query(variables=['Riego'], 
                          evidence={'HierbaMojada': 'Mojado'}))
    
    # c. Explicación más probable
    print("\nExplicación más probable para Hierba mojada:")
    print(inferencia.map_query(variables=['Clima', 'Riego'],
                             evidence={'HierbaMojada': 'Mojado'}))

# Ejemplo de uso
if __name__ == "__main__":
    # Crear la red bayesiana
    red = crear_red_bayesiana()
    
    # Visualizar la estructura
    visualizar_red(red)
    
    # Realizar inferencias
    inferencia_bayesiana(red)