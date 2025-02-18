import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Carro import Carro
from Semaforo import Semaforo

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
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

#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 20

semaforos = []

#Variables para el control del observador
theta = 0.0
radius = 300


pygame.init()

def Axis():
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
    
def draw_intersection():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    # Horizontal road
    glVertex3f(-DimBoard, 0.1, -20)
    glVertex3f(-DimBoard, 0.1, 20)
    glVertex3f(DimBoard, 0.1, 20)
    glVertex3f(DimBoard, 0.1, -20)
    glEnd()
    
    glBegin(GL_QUADS)
    # Vertical road
    glVertex3f(-20, 0.1, -DimBoard)
    glVertex3f(20, 0.1, -DimBoard)
    glVertex3f(20, 0.1, DimBoard)
    glVertex3f(-20, 0.1, DimBoard)
    glEnd()


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        
    semaforos.append(Semaforo(10, 0, 0, 5.0, 30, [0, 0, 1]))
    
    for semaforo in semaforos:
        semaforo.otros_semaforos = [s for s in semaforos if s != semaforo]
    
    for i in range(ncubos):
        cubos.append(Carro(DimBoard, 1.0, i, 0, 200))
        
    for i in cubos:
        i.setotrosagentes(cubos)
        i.setsemaforos(semaforos)
    

#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    #glutPostRedisplay()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    
    # Dibuja intersección
    draw_intersection()
    
    # Dibuja cubos
    for obj in cubos:
        obj.draw()
        obj.update()
        
    # Dibuja semaforos
    for obj in semaforos:
        obj.draw()
        obj.update([s for s in semaforos if s != obj])

    
done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta += -1.0
        lookat()    
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookat()        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #CODIGO PARA LECTURA DE TECLADO NO CONTINUA
    #    if event.type == pygame.KEYDOWN:
    #        if event.key == pygame.K_RIGHT:
    #            if theta > 359.0:
    #                theta = 0
    #            else:
    #                theta += 1.0
    #            lookat()
    #        if event.key == pygame.K_LEFT:
    #            if theta < 1.0:
    #                theta = 360.0
    #            else:
    #                theta += -1.0
    #            lookat()
    #        if event.key == pygame.K_ESCAPE:
    #            done = True
    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()