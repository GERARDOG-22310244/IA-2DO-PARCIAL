class SubastaVickrey:
    def __init__(self, participantes):
        self.participantes = participantes  # Diccionario {nombre: valoración}
    
    def realizar_subasta(self):
        if len(self.participantes) < 2:
            return None, 0
        
        # Ordenar participantes por valoración descendente
        ordenados = sorted(self.participantes.items(), key=lambda x: -x[1])
        ganador = ordenados[0][0]
        precio = ordenados[1][1]  # Segundo precio más alto
        
        return ganador, precio

# Ejemplo de uso
participantes = {
    "Alice": 120,
    "Bob": 100,
    "Charlie": 150,
    "David": 90
}

subasta = SubastaVickrey(participantes)
ganador, precio = subasta.realizar_subasta()
print(f"\nGanador de la subasta: {ganador} con un precio de {precio}")