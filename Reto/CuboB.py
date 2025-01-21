#Autor: Ivan Olmos Pineda


import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class CuboB:
    
    def __init__(self, dim, vel):
        #vertices del cubo
        self.points = [[0,0,0], [3,0,0], [3,0,2], [0,0,2], [0,2,0], [0,2,2], [1,0,0], [1,0,2], [1,2,0], [1,2,2], [3,1,2], [3,1,0],[1,1,0],[1,1,2]]

        self.DimBoard = dim
        ncol = 4
        dimcol = self.DimBoard / ncol
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard / dimcol, self.DimBoard / dimcol) * dimcol)
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard / dimcol, self.DimBoard / dimcol) * dimcol)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(1)
        self.Direction.append(5.0)
        self.Direction.append(0)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        #guardar los otros agentes 
        self.otrosagentes = []
        #TODO: cambiar valor de radio
        self.radio = 20
        #Collision detection
        self.paused = False

    def setAgentes(self, agentes):
        self.otrosagentes = agentes

    def collision(self):
        self.paused = False
        for agent in self.otrosagentes:
            if self != agent:
                #Encontrar distancia entre agentes
                dx = agent.Position[0] - self.Position[0]
                dz = agent.Position[2] - self.Position[2]
                dc = math.sqrt(dx ** 2 + dz**2)
                #Si si estan cercas y el está detenido, cambian de direccion. Sino, pausan. Por ahorita, solo rebotan. 
                if dc < self.radio + agent.radio:
                    if agent.paused:
                        self.Direction[0] *= -1
                        self.Direction[2] *= -1
                    else:
                        self.paused = True
                    


    def update(self):
        self.collision()
        if not self.paused:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]
            
            #detecc de que el objeto no se salga del area de navegacion
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

    def drawFaces(self):
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[8])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[9])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[8])
        glVertex3fv(self.points[9])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[9])
        glVertex3fv(self.points[8])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[11])
        glVertex3fv(self.points[12])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[10])
        glVertex3fv(self.points[11])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[13])
        glVertex3fv(self.points[10])
        glEnd()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(10,10,10)
        self.drawFaces()
        glPopMatrix()
        
class Plataforma:
    def __init__(self, carrito, offset_z=5.0):
        self.carrito = carrito
        self.offset_z = offset_z
        
        self.points = [
            [ 0, 0,  1],
            [ 0, 0, -1],
            [-1, 0, -1],
            [-1, 0,  1]
        ]

        # Posición de la plataforma en Y
        self.posY = 0.0       

    def update(self):
        """
        En lugar de usar tiempo o frames, usaremos
        la posición en X del carrito para determinar
        si sube (2.0) o baja (0.0).
        """
        cx, cy, cz = self.carrito.Position

        # Si cx >= 0, plataforma sube
        if cx >= 0 and self.posY < 20:
            self.posY += 0.1   # Sube lentamente, 0.1 cada frame
        elif cx < 0 and self.posY > 0:
            self.posY -= 0.1   # Baja lentamente, 0.1 cada frame


    def draw(self):
        cx, cy, cz = self.carrito.Position
        
        glPushMatrix()
        # Trasladamos según posición del carrito,
        # offset en Z, y la posY calculada.
        glTranslatef(cx, cy + self.posY, cz + self.offset_z)
        glScalef(20, 1, 20)

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        for v in self.points:
            glVertex3fv(v)
        glEnd()
        
        glPopMatrix()
