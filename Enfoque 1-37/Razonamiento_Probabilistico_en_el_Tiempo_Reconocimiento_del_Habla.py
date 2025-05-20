import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt

# 1. Modelo Oculto de Markov (HMM) para reconocimiento de habla
class ReconocimientoHablaHMM:
    def __init__(self, n_estados=3, n_mfcc=13):
        """
        Inicializa un HMM para reconocimiento de habla
        :param n_estados: Número de estados ocultos (fonemas)
        :param n_mfcc: Número de coeficientes MFCC (características)
        """
        self.modelo = hmm.GaussianHMM(n_components=n_estados, covariance_type="diag", n_iter=100)
        self.n_mfcc = n_mfcc
        self.estados = None
        
    def entrenar(self, X, longitudes):
        """
        Entrena el HMM con datos de entrenamiento
        :param X: Secuencia de observaciones (MFCCs)
        :param longitudes: Longitud de cada muestra de entrenamiento
        """
        # X debe ser un array 2D de forma (n_muestras, n_mfcc)
        self.modelo.fit(X, lengths=longitudes)
        
    def decodificar(self, observaciones):
        """
        Decodifica la secuencia más probable de estados ocultos
        :param observaciones: Secuencia de MFCCs a decodificar
        :return: Secuencia de estados más probable
        """
        log_prob, estados = self.modelo.decode(observaciones)
        self.estados = estados
        return estados
    
    def predecir_proba(self, observaciones):
        """
        Calcula las probabilidades posteriores de cada estado
        :param observaciones: Secuencia de MFCCs
        :return: Matriz de probabilidades [n_muestras × n_estados]
        """
        return self.modelo.predict_proba(observaciones)
    
    def visualizar_transiciones(self):
        """Visualiza la matriz de transición entre estados"""
        plt.figure(figsize=(8, 6))
        plt.imshow(self.modelo.transmat_, cmap='viridis', interpolation='nearest')
        plt.colorbar()
        plt.title('Matriz de Transición de Estados')
        plt.xlabel('Estado destino')
        plt.ylabel('Estado origen')
        plt.show()

# 2. Simulación de datos MFCC (para ejemplo)
def simular_mfcc(n_muestras=100, n_mfcc=13):
    """
    Simula coeficientes MFCC para demostración
    :return: Datos simulados y longitudes de muestras
    """
    # Simular 3 muestras de habla de diferente longitud
    X1 = np.random.randn(30, n_mfcc) * 0.1 + np.arange(n_mfcc)
    X2 = np.random.randn(45, n_mfcc) * 0.1 + np.arange(n_mfcc)[::-1]
    X3 = np.random.randn(25, n_mfcc) * 0.1 + np.linspace(0, 1, n_mfcc)
    
    X = np.vstack([X1, X2, X3])
    longitudes = [len(X1), len(X2), len(X3)]
    return X, longitudes

# 3. Ejemplo de uso
if __name__ == "__main__":
    print("=== Reconocimiento de Habla con HMM ===")
    
    # Parámetros
    n_estados = 3  # Fonemas distintos
    n_mfcc = 13    # Coeficientes MFCC estándar
    
    # 1. Crear modelo
    reconocedor = ReconocimientoHablaHMM(n_estados, n_mfcc)
    
    # 2. Simular datos de entrenamiento (MFCCs)
    X_train, lengths = simular_mfcc(n_mfcc=n_mfcc)
    print(f"\nDatos de entrenamiento: {X_train.shape[0]} frames")
    
    # 3. Entrenar modelo
    reconocedor.entrenar(X_train, lengths)
    print("\nModelo entrenado con éxito")
    
    # 4. Visualizar matriz de transición
    reconocedor.visualizar_transiciones()
    
    # 5. Probar con nuevos datos
    X_test, _ = simular_mfcc(50, n_mfcc)
    estados = reconocedor.decodificar(X_test)
    probas = reconocedor.predecir_proba(X_test)
    
    print("\nSecuencia decodificada (primeros 10 estados):", estados[:10])
    print("\nProbabilidades de estado (primeros 5 frames):")
    print(probas[:5].round(3))
    
    # 6. Visualizar resultados
    plt.figure(figsize=(10, 4))
    plt.plot(estados, label='Estado decodificado')
    plt.title('Secuencia de Estados Ocultos Decodificada')
    plt.xlabel('Frame')
    plt.ylabel('Estado')
    plt.legend()
    plt.show()