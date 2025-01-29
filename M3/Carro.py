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
    
    def __init__(self, dim, vel, id, x=0, z=200):
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
        self.Position.append(x)
        self.Position.append(5.0)
        self.Position.append(z)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(0)
        self.Direction.append(5.0)
        self.Direction.append(-1)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m

        self.initialdirection = self.Direction
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        self.otrosagentes = []
        self.radio = 15
        self.initialvel = vel
        self.vel = vel

        self.has_collided = False
        self.semaforos = None
        self.id = id
        self.greensemaforo = None

    def setotrosagentes(self, agentes):
        self.otrosagentes = [i for i in agentes if i != self]
    
    def setsemaforos(self, semaforos):
        self.semaforos = semaforos

    def getDistance(self, point1, point2):
        dx = point1[0] - point2[0]
        dz = point1[2] - point2[2]
        return math.sqrt(dx ** 2 + dz ** 2)
    
    def take_msg(self):
        self.greensemaforo = None
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:
                if msg.performative == "responder":
                    self.greensemaforo = msg.content["verde"]

    def collision(self):
        self.has_collided = False
        for agent in self.otrosagentes:
            dc = self.getDistance(agent.Position, self.Position)
            nextpositionx = self.Position[0] + self.Direction[0]
            nextpositiony = self.Position[2] + self.Direction[2]
            dc2 = self.getDistance(agent.Position, [nextpositionx, 0, nextpositiony])
            if dc < self.radio + agent.radio and dc2 < dc:
                self.has_collided = True

    def decelerar(self):
        self.Direction[0] = (self.Direction[0] / self.vel) * (self.vel - 0.1)
        self.Direction[2] = (self.Direction[2] / self.vel) * (self.vel - 0.1)
        self.vel -= 0.1

    def update(self):
        self.collision()
        self.take_msg()
        
        if self.has_collided:
            self.decelerar()
        else:
            if self.vel < self.initialvel:
                self.Direction[0] = (self.Direction[0] / self.vel) * (self.vel + 0.1)
                self.Direction[2] = (self.Direction[2] / self.vel) * (self.vel + 0.1)
                self.vel += 0.1

        # actualiza la posición
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        self.Position[0] = new_x
        self.Position[2] = new_z

        for i in self.semaforos:
            if self.getDistance(i.Position, self.Position) < 50 and i.direction == self.initialdirection:
                msg = Message(sender=self.id, receiver=i.id, performative="askstate",content={})
                msg.send()
                if not self.greensemaforo:
                    self.decelerar()
                    msg = Message(sender=self.id, receiver=i.id, performative="activar",content={})
                    msg.send()
        
        

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
    
