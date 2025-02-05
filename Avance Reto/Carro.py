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
    
    def __init__(self, position=None, vel=1.0, direction=None, dimw=300, dimh=200, movimientos=[]):
        
        # Lista de objetos .OBJ (los carros)
        #carros = []
        
        #carros.append(OBJ("Avance Reto\Modelos\Jeep_Renegade_2016.obj", swapyz=True))
        #carros[0].generate()
        
        # Cargar el modelo OBJ
        self.model = OBJ("Avance Reto\Modelos\Jeep_Renegade_2016.obj", swapyz=True)  # Cambia el path al archivo OBJ de tu carro

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
            dc = self.getDistance(agent.Position, self.Position)
            nextpositionx = self.Position[0] + self.Direction[0]
            nextpositiony = self.Position[2] + self.Direction[2]
            dc2 = self.getDistance(agent.Position, [nextpositionx, 0, nextpositiony])
            if dc < self.radio + agent.radio and dc2 < dc:
                self.has_collided = True

    def turn(self):
        if self.movimientos:
            if abs(self.Direction[0] - self.movimientos[0][0]) < 0.1 and abs(self.Direction[2] - self.movimientos[0][2]) < 0.1:
                self.Direction = self.movimientos.pop(0)
                self.turningright = False
                self.turningleft = False
                return
        if self.turningright:
            degturn = math.radians(1.75)
            turnmatrix = np.array([[math.cos(degturn), -1 * math.sin(degturn)], [math.sin(degturn), math.cos(degturn)]])
            direction = np.array([[self.Direction[0]], [self.Direction[2]]])
            newpoints = turnmatrix @ direction
            self.Direction = [round(newpoints[0][0], 3), self.Direction[1], round(newpoints[1][0], 3)]
        if self.turningleft:
            degturn = math.radians(-0.9)
            turnmatrix = np.array([[math.cos(degturn), -1 * math.sin(degturn)], [math.sin(degturn), math.cos(degturn)]])
            direction = np.array([[self.Direction[0]], [self.Direction[2]]])
            newpoints = turnmatrix @ direction
            self.Direction = [round(newpoints[0][0], 3), self.Direction[1], round(newpoints[1][0], 3)]


    def update(self):
        self.collision()

        self.turn()

        if abs(self.Position[0]) > self.borde_limite1 or abs(self.Position[2]) > self.borde_limite2:
            self.has_collided = False  # 🚀 Desactiva colisiones para salir

        # 🔥 Si no hay colisión, restauramos la velocidad original
        if not self.has_collided:
            self.vel = self.initialvel
        else:
            self.vel = max(0, self.vel - 0.1)

        # 🚦 Verificar semáforo cercano
        for semaforo in self.semaforos:
            distancia = self.getDistance(semaforo.Position, self.Position)
            #newPosition = [self.Position[0] + (self.Direction[0] * self.vel), self.Position[1], self.Position[2] + (self.Direction[2] * self.vel)]
            #newDistance = self.getDistance(semaforo.Position, newPosition)
            if distancia < 10 and self.Direction == semaforo.direction:
                if semaforo.estado == "ROJO":
                    self.vel = 0  # 🚗 Detener carro
                elif semaforo.estado == "VERDE":
                    if self.vel == 0:
                        self.vel = self.initialvel  # ✅ Reanudar movimiento
                    if self.movimientos:
                        posiblesDirecciones = [[0, 0, 1], [-1, 0, 0], [0, 0, -1], [1, 0, 0]]
                        present = posiblesDirecciones.index(self.Direction)
                        next = posiblesDirecciones.index(self.movimientos[0])
                        self.turningright = (present + 1 == next or (present == 3 and next == 0))
                        self.turningleft = not self.turningright

        # ✅ Mover carro si tiene velocidad
        if self.vel > 0:
            self.Position[0] += self.Direction[0] * self.vel
            self.Position[2] += self.Direction[2] * self.vel


        
        

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
        self.model.render()  # Renderizar el modelo OBJ
        glPopMatrix()