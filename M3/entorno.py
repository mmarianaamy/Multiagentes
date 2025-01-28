import agentpy as ap
from agentes import Vehiculo, Semaforo  # Importar las clases de agentes

class Interseccion(ap.Model):
    def setup(self):
        # Crear semáforos
        self.semaforos = ap.AgentList(self, 2, Semaforo)

        # Crear vehículos
        self.vehiculos = ap.AgentList(self, 10, Vehiculo)

    def step(self):
        # Actualizar estado de los vehículos y semáforos
        for vehiculo in self.vehiculos:
            vehiculo.mover()
            if vehiculo.velocidad == 0:
                vehiculo.solicitar_verde(self.semaforos[0])  # Ejemplo

        for semaforo in self.semaforos:
            if semaforo.temporizador > 0:
                semaforo.temporizador -= 1
            else:
                semaforo.cambiar_estado("rojo")