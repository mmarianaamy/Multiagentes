import numpy as np
import random
import math

class AgenteCubo:
    def __init__(self, dim, vel, escala_inicial, riqueza_inicial=1):
        self.points = np.array([[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0]])
        self.escala_inicial = escala_inicial
        self.escala = escala_inicial
        self.radio = math.sqrt(self.escala * self.escala + self.escala * self.escala)
        self.dim_tablero = dim
        self.riqueza = riqueza_inicial
        
        # Posición inicial aleatoria en el tablero
        self.posicion = [
            random.randint(-1 * self.dim_tablero, self.dim_tablero),
            self.escala,
            random.randint(-1 * self.dim_tablero, self.dim_tablero)
        ]
        
        # Vector de dirección aleatorio
        self.direccion = [random.random(), 0, random.random()]
        magnitud = math.sqrt(self.direccion[0]**2 + self.direccion[2]**2)
        self.direccion[0] /= magnitud
        self.direccion[2] /= magnitud
        self.direccion[0] *= vel
        self.direccion[2] *= vel

        self.colision = False
        self.agentes = []

    def establecer_agentes(self, agentes):
        self.agentes = agentes

    def actualizar_riqueza(self, nueva_riqueza):
        self.riqueza = nueva_riqueza
        self.escala = self.escala_inicial * (self.riqueza / 1.0)

    def transferir_riqueza(self, receptor):
        if self.riqueza > 0:
            self.riqueza -= 1
            receptor.riqueza += 1
            receptor.actualizar_riqueza(receptor.riqueza)
            self.actualizar_riqueza(self.riqueza)

    def detectar_colisiones(self):
        for agente in self.agentes:
            if self != agente:
                d_x = self.posicion[0] - agente.posicion[0]
                d_z = self.posicion[2] - agente.posicion[2]
                distancia = math.sqrt(d_x**2 + d_z**2)
                if distancia - (self.radio + agente.radio) < 0.0:
                    self.transferir_riqueza(agente)

    def actualizar_posicion(self):
        self.detectar_colisiones()
        if not self.colision:
            nuevo_x = self.posicion[0] + self.direccion[0]
            nuevo_z = self.posicion[2] + self.direccion[2]

            if abs(nuevo_x) <= self.dim_tablero:
                self.posicion[0] = nuevo_x
            else:
                self.direccion[0] *= -1.0
                self.posicion[0] += self.direccion[0]

            if abs(nuevo_z) <= self.dim_tablero:
                self.posicion[2] = nuevo_z
            else:
                self.direccion[2] *= -1.0
                self.posicion[2] += self.direccion[2]
