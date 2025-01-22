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
ncubosB = 5
plataforma_b = None

rows = 5
estantes = []
ncajas = 10
cajas = []

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
        gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        glClearColor(0,0,0,0)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        for i in range(ncubosB):
            new_cubo_b = CuboB(DimBoard, 1)
            cubos.append(new_cubo_b)

            plataforma_b = Plataforma(new_cubo_b, offset_z=10.0)
        
        for agente in cubos:
            agente.setAgentes(cubos)

        for i in range(rows):
            estantes.append(Estante(10, DimBoard/rows * i, 8))

        for i in range(ncajas):
            cajas.append(CuboA(DimBoard, 10, 10))

    def update(self):  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Axis()
        #Se dibuja el plano gris
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3d(-DimBoard, 0, -DimBoard)
        glVertex3d(-DimBoard, 0, DimBoard)
        glVertex3d(DimBoard, 0, DimBoard)
        glVertex3d(DimBoard, 0, -DimBoard)
        glEnd()

        #se dibujan estantes

        for estante in estantes:
            estante.draw()

        #Se dibuja cubos
        for obj in cubos:
            obj.draw()
            obj.update()
        
        if plataforma_b is not None:
            plataforma_b.draw()
            plataforma_b.update()
        
        for caja in cajas:
            caja.draw()

        pygame.display.flip()
        pygame.time.wait(10)

parameters = {
'agents': ncubosB,
'steps': 1000
}

model = AgentModel(parameters)
results = model.run()

pygame.quit()