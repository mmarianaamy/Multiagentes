#Autor: Ivan Olmos Pineda
#Curso: Multiagentes - Graficas Computacionales

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from CuboA import CuboA
from CuboB import CuboB
from CuboB import Plataforma
from Estante import Estante

import agentpy as ap

screen_width = 800
screen_height = 800
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200

pygame.init()

#cubo = Cubo(DimBoard, 1.0)
cubos = []
#ncubosA = 2
ncubosB = 2
plataforma_b = None

rows = 0
estantes = []
ncajas = 10

class AgentModel(ap.Model):
    def Axis(self):
        glShadeModel(GL_FLAT)
        glLineWidth(3.0)
        #X axis in red
        glColor3f(1.0,0.0,0.0)
        glBegin(GL_LINES)
        glVertex3f(X_MIN,0.0,0.0)
        glVertex3f(X_MAX,0.0,0.0)
        glEnd()
        #Y axis in green
        glColor3f(0.0,1.0,0.0)
        glBegin(GL_LINES)
        glVertex3f(0.0,Y_MIN,0.0)
        glVertex3f(0.0,Y_MAX,0.0)
        glEnd()
        #Z axis in blue
        glColor3f(0.0,0.0,1.0)
        glBegin(GL_LINES)
        glVertex3f(0.0,0.0,Z_MIN)
        glVertex3f(0.0,0.0,Z_MAX)
        glEnd()
        glLineWidth(1.0)

    def setup(self):
        screen = pygame.display.set_mode(
            (screen_width, screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Reto")

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        self.cajas = []

        # Crear los agentes (carritos)
        self.agents = ap.AgentList(self, self.p.agents, CuboB)
        self.agents.setAgentes(list(self.agents))

        # Crear plataformas asociadas a cada carrito
        global plataformas
        plataformas = [Plataforma(agent, offset_z=10.0) for agent in self.agents]

        for i in range(rows):
            estantes.append(Estante(10, DimBoard / rows * i, 8))

        for i in range(ncajas):
            self.cajas.append(CuboA(DimBoard, 10, 10))


    def step(self):
        self.agents.step()

    def update(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Axis()

        # Dibujar el plano gris
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3d(-DimBoard, 0, -DimBoard)
        glVertex3d(-DimBoard, 0, DimBoard)
        glVertex3d(DimBoard, 0, DimBoard)
        glVertex3d(DimBoard, 0, -DimBoard)
        glEnd()

        # Dibujar estantes
        for estante in estantes:
            estante.draw()

        # Dibujar cubos y actualizar lógica
        for obj in cubos:
            obj.update()
        
        if plataforma_b is not None:
            plataforma_b.draw()
            plataforma_b.update()
        
        for caja in self.cajas:
            obj.draw()

        # Detectar colisiones y levantar cajas
        for plataforma in plataformas:
            for caja in self.cajas:
                if plataforma.caja_cargada is None and plataforma.detectar_colision(caja):
                    print(f"Levantando la caja en {caja.Position}")
                    plataforma.levantar_caja(caja)

            # Actualizar la plataforma (y la caja cargada, si existe)
            plataforma.update()
            plataforma.draw()

        # Dibujar las cajas que no están cargadas
        for caja in self.cajas:
            caja.draw()


            # Actualizar la plataforma y sincronizar caja cargada (si la hay)
            plataforma.update()
            plataforma.draw()

        # Dibujar las cajas (las que no están cargadas se dibujan normalmente)
        for caja in cajas:
            if plataforma.caja_cargada != caja:  # No redibujar la caja cargada
                caja.draw()

        self.agents.draw()

        pygame.display.flip()
        pygame.time.wait(10)

parameters = {
'agents': ncubosB,
'steps': 1000
}

model = AgentModel(parameters)
results = model.run()

pygame.quit()