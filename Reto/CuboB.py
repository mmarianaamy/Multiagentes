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

from owlready2 import *
import agentpy as ap

onto = get_ontology("./Reto/ontology.owl").load()

class CuboB(ap.Agent):

    def setup(self):
        #self.myself = onto.Agent(has_id = self.id)
        #self.myself.has_position = onto.Position(has_position_x = self.Position[0], has_position_z = self.Position[2])
        #vertices del cubo
        #self.points = [[0,0,0], [3,0,0], [3,0,2], [0,0,2], [0,2,0], [0,2,2], [1,0,0], [1,0,2], [1,2,0], [1,2,2], [3,1,2], [3,1,0],[1,1,0],[1,1,2]]
        self.points = np.array([[0,0,0], [3,0,0], [3,0,2], [0,0,2], [0,1,0], [0,1,2], [3,1,0], [3,1,2], [1.8,2.5,2.0],[1.8,2.5,0.0],[0.2,2.5,2.0],[0.2,2.5,0.0], [2.0,1.0,2.0], [2.0,1.0,0.0],[2.0,1.5,0.0],[2.0,1.5,2.0],[3.0,1.5,0.0],[3.0,1.5,2.0],[0.0,0.0,0.5],[0.0,0.0,1.5],[0.0,3.0,1.5],[0.0,3.0,0.5],[0.8,1.0,0.0],[0.8,1.0,2.0],[0.8,1.3,2.0],[0.8,1.3,0.0],[0.0,1.3,0.0],[0.0,1.3,2.0],[0,0,-0.5], [0,0,2.5], [-1,0,2.5], [-1,0,-0.5]])
        #                           0,       1,      2,        3,       4,      5,         6,       7,      8,              9,          10,             11,             12,         13,             14,         15,             16,         17,             18,          19,           20,             21,           22,          23,             24,           25,          26,          27,          28,          29,      30,      31,      32,      33
        self.DimBoard = 200
        ncol = 4
        dimcol = self.DimBoard / ncol
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
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
        self.Direction[0] *= 10
        self.Direction[2] *= 10
        #guardar los otros agentes 
        self.otrosagentes = []
        #TODO: cambiar valor de radio
        self.radio = 20
        #Collision detection
        self.paused = False
        self.at_origin = False
        

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
        if not self.at_origin:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]

            # Detección de que el objeto no se salga del área de navegación
            if(abs(new_x) <= self.DimBoard and abs(new_z) <= self.DimBoard):
                self.Position[0] = new_x
                self.Position[2] = new_z
            else:
                # Si el cubo toca un límite, rebota hacia el origen (0, 0, 0)
                direction_to_origin_x = -self.Position[0]
                direction_to_origin_z = -self.Position[2]

                # Normalizamos la dirección hacia el origen
                magnitude = math.sqrt(direction_to_origin_x ** 2 + direction_to_origin_z ** 2)
                self.Direction[0] = direction_to_origin_x / magnitude
                self.Direction[2] = direction_to_origin_z / magnitude

                # Ajustamos la posición para "rebotar" al origen
                self.Position[0] += self.Direction[0]
                self.Position[2] += self.Direction[2]

                # Si el objeto está cerca del origen, lo marcamos y asignamos nueva dirección aleatoria
                if abs(self.Position[0]) < 0.1 and abs(self.Position[2]) < 0.1:  # Consideramos un pequeño margen de error
                    self.at_origin = True
                    # Nueva dirección aleatoria
                    self.Direction[0] = random.random() * 2 - 1  # Dirección aleatoria entre -1 y 1
                    self.Direction[2] = random.random() * 2 - 1  # Dirección aleatoria entre -1 y 1

                    # Normalizamos la nueva dirección aleatoria
                    magnitude = math.sqrt(self.Direction[0] ** 2 + self.Direction[2] ** 2)
                    self.Direction[0] /= magnitude
                    self.Direction[2] /= magnitude
        else:
            # Si ya hemos llegado al origen, reiniciamos la posición y esperamos para seguir moviéndonos
            self.Position = [0.0, 5.0, 0.0]
            self.at_origin = False




    def drawFaces(self):
        #base
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        #cara1
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[4])
        glEnd()
        #cara2
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        #cara3
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[7])
        glEnd()
        #cara4
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glEnd()
        
        
        #tapa
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.4, 0.0)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[5])
        glEnd()
        
        #cajuela
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[13])
        glVertex3fv(self.points[12])
        glVertex3fv(self.points[15])
        glVertex3fv(self.points[14])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[13])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[16])
        glVertex3fv(self.points[14])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[17])
        glVertex3fv(self.points[16])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[12])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[17])
        glVertex3fv(self.points[15])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3fv(self.points[14])
        glVertex3fv(self.points[15])
        glVertex3fv(self.points[17])
        glVertex3fv(self.points[16])
        glEnd()
        
        
        
        # Dibujar cabina
        glShadeModel(GL_FLAT)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glColor3f(0.0,0.0,0.0)
        #glVertex3fv(self.points[7])
        glVertex3fv(self.points[8])
        glVertex3fv(self.points[12])
        
        #glVertex3fv(self.points[6])
        glVertex3fv(self.points[9])
        glVertex3fv(self.points[13])
        
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[10])
        
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[11])
        glEnd()
        #techo cabina
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[8])
        glVertex3fv(self.points[10])
        glVertex3fv(self.points[11])
        glVertex3fv(self.points[9])
        glEnd()
                
        #dibujar mastil
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[18])
        glVertex3fv(self.points[19])
        glVertex3fv(self.points[20])
        glVertex3fv(self.points[21])
        glEnd()
        
        #dibujar controles cabina
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[23])
        glVertex3fv(self.points[24])
        glVertex3fv(self.points[27])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        glVertex3fv(self.points[22])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[26])
        glVertex3fv(self.points[25])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[27])
        glVertex3fv(self.points[26])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        glVertex3fv(self.points[27])
        glVertex3fv(self.points[24])
        glVertex3fv(self.points[25])
        glVertex3fv(self.points[26])
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        glVertex3fv(self.points[23])
        glVertex3fv(self.points[22])
        glVertex3fv(self.points[25])
        glVertex3fv(self.points[24])
        glEnd()
        
        
        
        # Dibujar aristas con color negro
        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3fv(self.points[8])
        glVertex3fv(self.points[10])
        glVertex3fv(self.points[11])
        glVertex3fv(self.points[9])
        glEnd()
        
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(15,15,15)
        self.drawFaces()
        glPopMatrix()


    def step(self):
        #self.collision()
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
        
    
class Plataforma:
    def __init__(self, carrito, offset_z=5.0):
        self.carrito = carrito
        self.offset_z = offset_z
        
        self.points = [
            [ 0, 1,  1],
            [ 0, -1, -1],
            [-1, -1, -1],
            [-1, 1,  1]
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
