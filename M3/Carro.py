import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from owlready2 import *

import random
import math

class Carro:
    
    def __init__(self, dim, vel):
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        #Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        #Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        if (round(random.random(), 0) == 0):
            self.Direction.append(1)
            self.Direction.append(5.0)
            self.Direction.append(0)
        else:
            self.Direction.append(0)
            self.Direction.append(5.0)
            self.Direction.append(1)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        self.otrosagentes = []
        self.radio = 15
        self.initialvel = vel
        self.vel = vel

        self.has_collided = False

    def setotrosagentes(self, agentes):
        self.otrosagentes = [i for i in agentes if i != self]

    def collision(self):
        self.has_collided = False
        for agent in self.otrosagentes:
            dx = agent.Position[0] - self.Position[0]
            dz = agent.Position[2] - self.Position[2]
            dc = math.sqrt(dx ** 2 + dz**2)
            nextpositionx = self.Position[0] + self.Direction[0]
            nextpositiony = self.Position[2] + self.Direction[2]
            dx2 = agent.Position[0] - nextpositionx
            dz2 = agent.Position[2] - nextpositiony
            dc2 = math.sqrt(dx2 ** 2 + dz2**2)
            if dc < self.radio + agent.radio and dc2 < dc:
                self.has_collided = True

    def update(self):
        self.collision()
        if self.has_collided:
            self.Direction[0] = (self.Direction[0] / self.vel) * (self.vel - 0.1)
            self.Direction[2] = (self.Direction[2] / self.vel) * (self.vel - 0.1)
            self.vel -= 0.1
        else:
            if self.vel < self.initialvel:
                self.Direction[0] = (self.Direction[0] / self.vel) * (self.vel + 0.1)
                self.Direction[2] = (self.Direction[2] / self.vel) * (self.vel + 0.1)
                self.vel += 0.1

        
        """if (0 < self.Direction[0] and self.Direction[0] < 0.1) or (0 > self.Direction[0] and self.Direction[0] > -0.1):
            self.Direction[0] = 0

        if (0 < self.Direction[2] and self.Direction[2] < 0.1) or (0 > self.Direction[2] and self.Direction[2] > -0.1):
            self.Direction[2] = 0"""

        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        if(abs(new_x) <= self.DimBoard):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        
        if(abs(new_z) <= self.DimBoard):
            self.Position[2] = new_z
        else:
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]

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
    
