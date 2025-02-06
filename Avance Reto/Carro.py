import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from owlready2 import *

import random
import math

from Message import Message
from objloader import OBJ

import numpy as np


class Carro:

    def __init__(self, position=None, vel=1.0, direction=None, modelo=None, dimw=300, dimh=200, movimientos=[]):

        
        # Lista de modelos .OBJ (los carros)
        #modelos_carros = [
            #"Avance Reto\Modelos\Jeep_Renegade_2016.obj",
            #"Avance Reto\Modelos\Chevrolet_Camaro_SS_Low.obj",
        #]
        
        #carros.append(OBJ("Avance Reto\Modelos\Jeep_Renegade_2016.obj", swapyz=True))
        #carros[0].generate()
        
        # Cargar el modelo OBJ
        #self.model = OBJ("Avance Reto\Modelos\Jeep_Renegade_2016.obj", swapyz=True)  # Cambia el path al archivo OBJ de tu carro
        self.model = OBJ(modelo, swapyz=True) if modelo else None
        if self.model:
            self.model.generate()

        self.DimBoardW = dimw  # Se almacena la dimensión del tablero
        self.DimBoardH= dimh
        
        
        # Asegurar que la posición sea una lista de tres valores
        if position is None or not isinstance(position, (list, tuple)) or len(position) != 3:
            position = [random.randint(-1 * self.DimBoardW, self.DimBoardH), 5.0, random.randint(-1 * self.DimBoardW, self.DimBoardH)]
        
        self.Position = list(position)  # Convertimos a lista por seguridad

        # Asegurar que la dirección sea válida
        if direction is None or not isinstance(direction, (list, tuple)) or len(direction) != 3:
            direction = [1, 0, 0] if random.random() < 0.5 else [0, 0, 1]

        self.Direction = list(direction)
        
        # Normalización de dirección
        m = math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[0] /= m
        self.Direction[2] /= m
        self.Direction[0] *= vel
        self.Direction[2] *= vel

        self.vel = vel
        self.initialvel = vel
        self.radio = 15
        self.otrosagentes = []
        self.has_collided = False
        self.semaforos = None
        self.extra_movement = 0


        # 🚗 Si el carro está cerca del borde, permitimos que siga sin restricciones
        self.borde_limite1 = self.DimBoardW - 60  #5 🔥 Ajustamos el umbral de borde
        self.borde_limite2 = self.DimBoardH - 60  # 🔥 Ajustamos el umbral de borde

        self.movimientos = movimientos
        self.turningleft = False
        self.turningright = False

    def setotrosagentes(self, agentes):
        self.otrosagentes = [i for i in agentes if i != self]
    
    def setsemaforos(self, semaforos):
        self.semaforos = semaforos

    def getDistance(self, point1, point2):
        dx = point1[0] - point2[0]
        dz = point1[2] - point2[2]
        return math.sqrt(dx ** 2 + dz ** 2)

    def collision(self):
        self.has_collided = False
        for agent in self.otrosagentes:
            # Si este carro está girando y el otro agente está detenido (velocidad 0),
            # se asume que es un carro esperando el semáforo y se ignora la colisión.
            if (self.turningright or self.turningleft) and agent.vel == 0:
                continue

            dc = self.getDistance(agent.Position, self.Position)
            nextpositionx = self.Position[0] + self.Direction[0]
            nextpositiony = self.Position[2] + self.Direction[2]
            dc2 = self.getDistance(agent.Position, [nextpositionx, 0, nextpositiony])
            if dc < self.radio + agent.radio and dc2 < dc:
                self.has_collided = True


    def turn(self):
        # Si se tiene pendiente movimiento extra, aplicarlo gradualmente.
        if self.extra_movement > 0:
            # Incremento por frame (puedes ajustar este valor)
            increment = min(2, self.extra_movement)
            self.Position[0] += self.Direction[0] * increment
            self.Position[2] += self.Direction[2] * increment
            self.extra_movement -= increment
            # Una vez completado el avance extra, se reinician los flags de giro.
            if self.extra_movement <= 0:
                self.turningright = False
                self.turningleft = False
            return

        # Si hay movimientos en cola, y la dirección actual se acerca a la dirección objetivo...
        if self.movimientos:
            if abs(self.Direction[0] - self.movimientos[0][0]) < 0.1 and abs(self.Direction[2] - self.movimientos[0][2]) < 0.1:
                self.Direction = self.movimientos.pop(0)
                # Al terminar el giro (ya sea a la izquierda o a la derecha), se inicia el avance extra.
                if self.turningright or self.turningleft:
                    self.extra_movement = 30
                return

        # Si se está girando a la derecha, aplicar rotación incremental.
        if self.turningright:
            degturn = math.radians(1.77)
            turnmatrix = np.array([
                [math.cos(degturn), -math.sin(degturn)],
                [math.sin(degturn),  math.cos(degturn)]
            ])
            direction = np.array([[self.Direction[0]], [self.Direction[2]]])
            newpoints = turnmatrix @ direction
            self.Direction = [round(newpoints[0][0], 3), self.Direction[1], round(newpoints[1][0], 3)]
        # Si se está girando a la izquierda, aplicar rotación incremental.
        if self.turningleft:
            degturn = math.radians(-1.08)
            turnmatrix = np.array([
                [math.cos(degturn), -math.sin(degturn)],
                [math.sin(degturn),  math.cos(degturn)]
            ])
            direction = np.array([[self.Direction[0]], [self.Direction[2]]])
            newpoints = turnmatrix @ direction
            self.Direction = [round(newpoints[0][0], 3), self.Direction[1], round(newpoints[1][0], 3)]


    def update(self):
        self.collision()
        self.turn()

        # Si el carro se acerca al borde, desactivamos la detección de colisión
        if abs(self.Position[0]) > self.borde_limite1 or abs(self.Position[2]) > self.borde_limite2:
            self.has_collided = False

        # Velocidad según colisión
        if self.has_collided:
            self.vel = max(0, self.vel - 0.1)
        else:
            self.vel = self.initialvel

        # Variable para detectar semáforo en rojo
        red_light_detected = False

        # Procesar semáforos
        for semaforo in self.semaforos:
            distancia = self.getDistance(semaforo.Position, self.Position)
            if distancia < 5.5 and self._directions_match(self.Direction, semaforo.direction):
                if semaforo.estado == "ROJO":
                    red_light_detected = True
                elif semaforo.estado == "VERDE":
                    if self.movimientos:
                        posiblesDirecciones = [[0, 0, 1], [-1, 0, 0], [0, 0, -1], [1, 0, 0]]
                        present_index = self.find_direction_index(self.Direction, posiblesDirecciones)
                        next_index = self.find_direction_index(self.movimientos[0], posiblesDirecciones)
                        if present_index is not None and next_index is not None:
                            self.turningright = (present_index + 1 == next_index or (present_index == 3 and next_index == 0))
                            self.turningleft = not self.turningright

        # Si se detecta un semáforo en rojo, forzamos la detención
        if red_light_detected:
            self.vel = 0

        # Mover el carro (solo si la velocidad es mayor a cero)
        if self.vel > 0:
            self.Position[0] += self.Direction[0] * self.vel
            self.Position[2] += self.Direction[2] * self.vel

    def find_direction_index(self, vec, directions, tol=0.1):
        """
        Busca en la lista de direcciones 'directions' el índice de un vector que
        concuerde con 'vec' dentro de una tolerancia 'tol'.
        """
        for i, d in enumerate(directions):
            if abs(vec[0] - d[0]) < tol and abs(vec[2] - d[2]) < tol:
                return i
        return None

    def _directions_match(self, d1, d2, tol=2):
        """
        Retorna True si los componentes relevantes (índices 0 y 2) de d1 y d2
        difieren menos que la tolerancia 'tol'.
        """
        return abs(d1[0] - d2[0]) < tol and abs(d1[2] - d2[2]) < tol


        
        

    def draw(self):
        
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        
        # Calcular el ángulo de rotación en función de la dirección del vehículo
        angle = math.degrees(math.atan2(self.Direction[0], self.Direction[2]))  # Eje Y
        
        # Aplicar la rotación en función de la dirección
        glRotatef(angle, 0, 1, 0)
        
        # Corregir la orientación del modelo 3D (si está al revés)
        glRotatef(180, 0, 1, 0)  # Girar el modelo 180° para que el frente quede adelante

        glRotatef(-90.0, 1.0, 0.0, 0.0)  # ajusta si el modelo sale "acostado" 
        # Calcular el ángulo de rotación en función de la dirección
                
        glScaled(5, 5, 5)
        #self.model.render()  # Renderizar el modelo OBJ
        if self.model:
            self.model.render()
        glPopMatrix()