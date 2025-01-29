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

class Carro:
    
    def __init__(self, position=None, vel=1.0, direction=None, dim=200):
        self.DimBoard = dim
        # Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        # Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        # Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        self.DimBoard = dim  # Se almacena la dimensión del tablero

        # Asegurar que la posición sea una lista de tres valores
        if position is None or not isinstance(position, (list, tuple)) or len(position) != 3:
            position = [random.randint(-1 * self.DimBoard, self.DimBoard), 5.0, random.randint(-1 * self.DimBoard, self.DimBoard)]
        
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
            dc = self.getDistance(agent.Position, self.Position)
            nextpositionx = self.Position[0] + self.Direction[0]
            nextpositiony = self.Position[2] + self.Direction[2]
            dc2 = self.getDistance(agent.Position, [nextpositionx, 0, nextpositiony])
            if dc < self.radio + agent.radio and dc2 < dc:
                self.has_collided = True

    def update(self):
        self.collision()

        # 🚗 Si el carro está cerca del borde, permitimos que siga sin restricciones
        borde_limite = self.DimBoard - 60  # 🔥 Ajustamos el umbral de borde
        if abs(self.Position[0]) > borde_limite or abs(self.Position[2]) > borde_limite:
            self.has_collided = False  # 🚀 Desactiva colisiones para salir

        # 🔥 Si no hay colisión, restauramos la velocidad original
        if not self.has_collided:
            self.vel = self.initialvel
        else:
            self.vel = max(0, self.vel - 0.1)

        # 🚦 Verificar semáforo cercano
        for semaforo in self.semaforos:
            distancia = self.getDistance(semaforo.Position, self.Position)
            if distancia < 10:
                if semaforo.estado == "ROJO":
                    self.vel = 0  # 🚗 Detener carro
                elif semaforo.estado == "VERDE" and self.vel == 0:
                    self.vel = self.initialvel  # ✅ Reanudar movimiento

        # ✅ Mover carro si tiene velocidad
        if self.vel > 0:
            self.Position[0] += self.Direction[0] * (self.vel / self.initialvel)
            self.Position[2] += self.Direction[2] * (self.vel / self.initialvel)


        
        

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()
    
