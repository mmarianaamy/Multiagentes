import agentpy as ap

class Vehiculo(ap.Agent):
    def setup(self):
        self.posicion = [0, 0]  # Posición inicial del vehículo
        self.velocidad = 0
        self.aceleracion = 1
        self.distancia_frenado = 5
        self.semaforo_actual = None

    def mover(self):
        if self.semaforo_actual and self.semaforo_actual.estado == "rojo":
            self.frenar()
        else:
            self.acelerar()

    def acelerar(self):
        self.velocidad += self.aceleracion

    def frenar(self):
        self.velocidad = max(self.velocidad - self.aceleracion, 0)

    def solicitar_verde(self, semaforo):
        semaforo.recibir_solicitud(self)

class Semaforo(ap.Agent):
    def setup(self):
        self.estado = "rojo"
        self.temporizador = 0

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.temporizador = 10  # Temporizador en iteraciones

    def recibir_solicitud(self, vehiculo):
        if self.estado == "rojo" and not self.conflicto_con_otros_semaforos():
            self.cambiar_estado("verde")

    def conflicto_con_otros_semaforos(self):
        # Lógica para verificar conflictos con otros semáforos
        return False