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

class CuboB(ap.Agent):

    def defineOnto(self):
        with self.onto: 
            class Agent(Thing):
                pass

            class AgentMover(Agent):
                pass

            class Box(Thing):
                pass

            class Position(Thing):
                pass

            class Direction(Thing):
                pass

            class has_position(FunctionalProperty, ObjectProperty):
                domain = [AgentMover]
                range = [Position]

            class has_position_x(FunctionalProperty, DataProperty):
                domain = [Position]
                range = [int]

            class has_position_z(FunctionalProperty, DataProperty):
                domain = [Position]
                range = [int]

            class has_direction(FunctionalProperty, ObjectProperty):
                domain = [AgentMover]
                range = [Direction]

            class has_direction_x(FunctionalProperty, DataProperty):
                domain = [Direction]
                range = [float]

            class has_direction_z(FunctionalProperty, DataProperty):
                domain = [Direction]
                range = [float]

            class has_id(FunctionalProperty, DataProperty):
                domain = [AgentMover]
                range = [int] 

            class has_collided(FunctionalProperty, DataProperty):
                domain = [AgentMover]
                range = [bool]

            

    def setup(self):
        self.onto = get_ontology("./Act Integradora/ontology.owl").load()

        #Si no se carga desde aqui como que no funciona. Si alguien puediera arreglar esto estaría bien :D
        self.defineOnto()

        #vertices del cubo
        self.points = [[0,0,0], [3,0,0], [3,0,2], [0,0,2], [0,1,0], [0,1,2], [3,1,0], [3,1,2], [1.8,2.5,2.0],[1.8,2.5,0.0],[0.2,2.5,2.0],[0.2,2.5,0.0], [2.0,1.0,2.0], [2.0,1.0,0.0],[2.0,1.5,0.0],[2.0,1.5,2.0],[3.0,1.5,0.0],[3.0,1.5,2.0],[0.0,0.0,0.5],[0.0,0.0,1.5],[0.0,3.0,1.5],[0.0,3.0,0.5],[0.8,1.0,0.0],[0.8,1.0,2.0],[0.8,1.3,2.0],[0.8,1.3,0.0],[0.0,1.3,0.0],[0.0,1.3,2.0],[0,0,-0.5], [0,0,2.5], [-1,0,2.5], [-1,0,-0.5]]
        #                0,       1,      2,        3,       4,      5,         6,       7,      8,              9,          10,             11,             12,         13,             14,         15,             16,         17,             18,          19,           20,             21,           22,          23,             24,           25,          26,          27,          28,          29,      30,      31,      32,      33
        
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
        #guardar los otros agentes 
        self.otrosagentes = []
        #TODO: cambiar valor de radio
        self.radio = 20

        #Si alguien puede mejorar esto estaría muy padre. en mi env no quiere jalar bien el import si no es en el mismo archivo
        self.myself = self.onto.AgentMover()
        self.myself.has_id = self.id
        self.myself.has_position = self.onto.Position(has_position_x = self.Position[0], has_position_z = self.Position[2])
        self.myself.has_direction = self.onto.Direction(has_direction_x= self.Direction[0], has_direction_z = self.Direction[2])
        self.myself.has_collided = False

        self.B = {
            "position": self.myself.has_position,
            "direction": self.myself.has_direction,
            "agents": self.otrosagentes,
            "boxes": self.model.cajas,
        }

        self.I = None
        self.D = None
        self.plan = []
        self.randomDirection()

        self.onto.save("./Act Integradora/ontology.owl")
        

    def setAgentes(self, agentes):
        self.otrosagentes = [i for i in agentes if i != self]

    def collision(self):
        self.myself.has_collided = False
        for agent in self.otrosagentes:
            #Encontrar distancia entre agentes
            dx = agent.myself.has_position.has_position_x - self.myself.has_position.has_position_x
            dz =agent.myself.has_position.has_position_z - self.myself.has_position.has_position_z
            dc = math.sqrt(dx ** 2 + dz**2)
            if dc < self.radio + agent.radio:
                self.myself.has_collided = True
                self.randomDirection()
                    
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
        glTranslatef(self.myself.has_position.has_position_x, self.Position[1], self.myself.has_position.has_position_z)
        glScaled(15,15,15)
        self.drawFaces()
        glPopMatrix()

    #Dirección aleatorio asignado
    def randomDirection(self):
        self.myself.has_direction.has_direction_x = random.random() * 2 - 1  # Dirección aleatoria entre -1 y 1
        self.myself.has_direction.has_direction_z = random.random() * 2 - 1  # Dirección aleatoria entre -1 y 1

        # Normalizamos la nueva dirección aleatoria
        magnitude = math.sqrt(self.myself.has_direction.has_direction_x ** 2 + self.myself.has_direction.has_direction_z ** 2)
        self.myself.has_direction.has_direction_x /= magnitude
        self.myself.has_direction.has_direction_z /= magnitude

    #movimiento
    def move(self):
        new_x = self.myself.has_position.has_position_x + self.myself.has_direction.has_direction_x
        new_z = self.myself.has_position.has_position_z + self.myself.has_direction.has_direction_z
        
        self.myself.has_position = self.onto.Position(has_position_x = new_x, has_position_z = new_z)

        #detecc de que el objeto no se salga del area de navegacion
        if(abs(new_x) > self.DimBoard):
            self.myself.has_direction = self.onto.Direction(has_direction_x = self.myself.has_direction.has_direction_x * -1, has_direction_z = self.myself.has_direction.has_direction_z)
            self.myself.has_position = self.onto.Position(has_position_x=self.myself.has_position.has_position_x + self.myself.has_direction.has_direction_x, has_position_z=self.myself.has_position.has_position_z)
        
        if(abs(new_z) > self.DimBoard):
            self.myself.has_direction = self.onto.Direction(has_direction_x = self.myself.has_direction.has_direction_x, has_direction_z = self.myself.has_direction.has_direction_z * -1)
            self.myself.has_position = self.onto.Position(has_position_x=self.myself.has_position.has_position_x, has_position_z=self.myself.has_position.has_position_z + self.myself.has_direction.has_direction_z)

    #Dirección hacia orígen
    def pointToOrigin(self):
        # Apunta hacia el origen
        direction_to_origin_x = -self.myself.has_position.has_position_x
        direction_to_origin_z = -self.myself.has_position.has_position_z

        # Normalizamos la dirección hacia el origen
        magnitude = math.sqrt(direction_to_origin_x ** 2 + direction_to_origin_z ** 2)
        self.myself.has_direction.has_direction_x = direction_to_origin_x / magnitude
        self.myself.has_direction.has_direction_z = direction_to_origin_z / magnitude
    
    def pointToPoint(self, x, z):
        # Apunta hacia el origen
        direction_to_origin_x = x-self.myself.has_position.has_position_x
        direction_to_origin_z = z-self.myself.has_position.has_position_z

        # Normalizamos la dirección hacia el origen
        magnitude = math.sqrt(direction_to_origin_x ** 2 + direction_to_origin_z ** 2)
        self.myself.has_direction.has_direction_x = direction_to_origin_x / magnitude
        self.myself.has_direction.has_direction_z = direction_to_origin_z / magnitude
    
    def pointToPoint(self, x, z):
        # Apunta hacia el origen
        direction_to_origin_x = x-self.myself.has_position.has_position_x
        direction_to_origin_z = z-self.myself.has_position.has_position_z

        # Normalizamos la dirección hacia el origen
        magnitude = math.sqrt(direction_to_origin_x ** 2 + direction_to_origin_z ** 2)
        self.myself.has_direction.has_direction_x = direction_to_origin_x / magnitude
        self.myself.has_direction.has_direction_z = direction_to_origin_z / magnitude

    #Verdadero si está en el orígen
    def atOrigin(self):
        return abs(self.myself.has_position.has_position_x) < 0.1 and abs(self.myself.has_position.has_position_z) < 0.1

    def pause(self):
        self.myself.has_direction.has_direction_x = 0
        self.myself.has_direction.has_direction_z = 0

    def execute(self):
        if (len(self.plan) > 0):
            action = self.plan.pop()
            if action is not None:
                action()

    def BDI(self):
        self.brf()
        self.options()
        self.filter()
        self.create_plan()
        self.create_plan()

    def brf(self):
        self.B["position"] = self.myself.has_position
        self.B["direction"] = self.myself.has_direction
        self.B["boxes"] = self.model.cajas

    def options(self):
        self.D = []
        self.I = None
        self.I = None
        for i in self.B["boxes"]:
            self.D.append(i.Position)
        if self.B["plataforma"].caja_cargada is not None:
            self.D = []
            self.I = self.pointToOrigin()
            print("got box")
        
    
    def filter(self):
        if self.I == self.pointToOrigin():
            return
        
        mindist = 400
        targetbox = None
        for box in self.B["boxes"]:
            dist = math.sqrt((box.Position[0] - self.myself.has_position.has_position_x)**2 + (box.Position[2] - self.myself.has_position.has_position_z)**2)
            if dist < mindist:
                mindist = dist
                targetbox = box
        
        if targetbox != None:
            self.I = self.pointToPoint(targetbox.Position[0], targetbox.Position[2])
        else:
            self.I = self.randomDirection()

    def create_plan(self):
        print(self.I)
        self.plan = []
        self.plan.append(self.collision())
        self.plan.append(self.I)
        self.plan.append(self.move())


    def step(self):

        if (len(self.plan) == 0):
            self.BDI()

        self.execute()
        
        
    
class Plataforma:
    def __init__(self, carrito, offset_x=0.0, offset_y=0.0, offset_z=10.0):
        self.carrito = carrito
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z

        self.size = 20  # Tamaño de la plataforma (ancho y largo)
        self.caja_cargada = None  # Referencia a la caja actual cargada (si hay alguna)
        self.posY = 0.0  # Altura inicial de la plataforma
        self.alzada = False  # Indica si la plataforma está arriba

        # Define los puntos de la plataforma para el método draw
        self.points = [
            [-1.0, 0.0, 1.0],  # Esquina delantera izquierda
            [0.0, 0.0, 1.0],   # Esquina delantera derecha
            [0.0, 0.0, -1.0],  # Esquina trasera derecha
            [-1.0, 0.0, -1.0], # Esquina trasera izquierda
        ]
        self.carrito.B["plataforma"] = self
        self.carrito.B["plataforma"] = self

    def detectar_colision(self, caja):
        """
        Detecta colisión con una caja (Cubo A).
        """
        # Posición de la plataforma
        px, py, pz = self.carrito.Position
        half_size = self.size  # Duplica el tamaño de detección

        # Posición de la caja
        cx, cy, cz = caja.Position

        # Duplica el rango de detección para colisión
        colision_x = (px - half_size * 2 <= cx <= px + half_size * 2)  # Aumenta el rango en X
        colision_z = (pz - half_size * 2 <= cz <= pz + half_size * 2)  # Aumenta el rango en Z
        colision_y = abs(cy - py) <= 20  # Mantén o ajusta el rango en Y si es necesario

        return colision_x and colision_y and colision_z

    def levantar_caja(self, caja):
        """
        Engancha la caja a la plataforma y comienza a subir.
        """
        self.caja_cargada = caja
        self.alzada = True  # Indica que la plataforma debe subir
        self.carrito.B["plataforma"] = self
        self.carrito.B["plataforma"] = self


    def update(self):
        """
        Actualiza el estado de la plataforma y la posición de la caja cargada.
        """
        # Controlar el movimiento vertical de la plataforma
        if self.alzada and self.posY < 20:  # Subir si está levantada
            self.posY += 0.2
        elif not self.alzada and self.posY > 0:  # Bajar si no está levantada
            self.posY -= 0.2

        # Sincronizar la posición de la caja cargada con la plataforma
        if self.caja_cargada:
            if self.carrito.myself.has_position.has_position_x < 20 and self.carrito.myself.has_position.has_position_z < 20:
                self.caja_cargada = None
            else:
                self.caja_cargada.Position[0] = self.carrito.myself.has_position.has_position_x + self.offset_x
                self.caja_cargada.Position[1] = self.carrito.Position[1] + self.posY + 5  # Ajuste de altura
                self.caja_cargada.Position[2] = self.carrito.myself.has_position.has_position_z + self.offset_z
            if self.carrito.myself.has_position.has_position_x < 20 and self.carrito.myself.has_position.has_position_z < 20:
                self.caja_cargada = None
            else:
                self.caja_cargada.Position[0] = self.carrito.myself.has_position.has_position_x + self.offset_x
                self.caja_cargada.Position[1] = self.carrito.Position[1] + self.posY + 5  # Ajuste de altura
                self.caja_cargada.Position[2] = self.carrito.myself.has_position.has_position_z + self.offset_z

    def draw(self):
        """
        Dibuja la plataforma.
        """
        cx = self.carrito.myself.has_position.has_position_x
        cy = 5
        cz = self.carrito.myself.has_position.has_position_z
        glPushMatrix()
        glTranslatef(cx + self.offset_x, cy + self.posY + self.offset_y, cz + self.offset_z)
        glScalef(20, 1, 20)

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)  # Rojo para distinguir
        for v in self.points:
            glVertex3fv(v)
        glEnd()

        glPopMatrix()
