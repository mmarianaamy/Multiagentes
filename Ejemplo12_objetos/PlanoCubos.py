import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys

sys.path.append('..')
from Cubo import Cubo
from objloader import OBJ

# ------------------------
# Parámetros de Ventana
screen_width  = 800
screen_height = 600

# Parámetros de la proyección
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0

# Posición de la cámara
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0

CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0

UP_X = 0
UP_Y = 1
UP_Z = 0

# Ejes de referencia
X_MIN=-500
X_MAX= 500
Y_MIN=-500
Y_MAX= 500
Z_MIN=-500
Z_MAX= 500

# Dimensión del “suelo” en XZ
DimBoard = 200

# Cubos (de ejemplo)
cubos = []
ncubos =  20

# Lista de objetos .OBJ (la casa)
objetos = []

# Control para la cámara orbital
theta  = 0.0
radius = 300

pygame.init()

def Axis():
    """Dibuja ejes X(rojo), Y(verde), Z(azul)."""
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)

    # Eje X en rojo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0, 0)
    glVertex3f(X_MAX, 0, 0)
    glEnd()

    # Eje Y en verde
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, Y_MIN, 0)
    glVertex3f(0, Y_MAX, 0)
    glEnd()

    # Eje Z en azul
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, Z_MIN)
    glVertex3f(0, 0, Z_MAX)
    glEnd()

    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL
    )
    pygame.display.set_caption("Calles en el plano XZ")

    # Proyección en perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    # Cámara
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Cubos de ejemplo
    for _ in range(ncubos):
        cubos.append(Cubo(DimBoard, 1.0, 5.0))
    for c in cubos:
        c.getCubos(cubos)

    # Configuramos iluminación
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 200.0, 0.0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    # Cargamos el modelo de la casa
    objetos.append(OBJ("BrickOutbuilding.obj", swapyz=True))
    objetos[0].generate()
    objetos.append(OBJ("parque.obj", swapyz=True))
    objetos[1].generate()


def lookat():
    """
    Mueve la cámara en círculo alrededor del centro, altura fija EYE_Y.
    """
    global EYE_X, EYE_Z, radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)


def draw_square_ring():
    """
    Dibuja un anillo cuadrado sobre el plano XZ, dejando el interior vacío.
    Puedes ajustar:
      - margin: para separarlo de las orillas del plano
      - ring_thickness: para el grosor del marco
      - y_street: altura sobre el suelo
    """
    margin = 50          # Espacio entre el borde externo y DimBoard (ajusta a gusto)
    ring_thickness = 30 # Grosor del anillo
    y_street = 1.0      # Altura para evitar z-fighting con el suelo
    outer = DimBoard
    
    
    # Coordenadas externas del anillo
    x1 = -DimBoard + margin
    x2 =  DimBoard - margin
    z1 = -DimBoard + margin
    z2 =  DimBoard - margin

    # Color del anillo (negro/gris oscuro, ajústalo si lo quieres más claro)
    glColor3f(0.1, 0.1, 0.1)

    glPushMatrix()
    # ----- Franja superior -----
    glBegin(GL_QUADS)
    glVertex3f(x1-50, y_street, z2)               
    glVertex3f(x2+50, y_street, z2)               
    glVertex3f(x2+50, y_street, z2 - ring_thickness)
    glVertex3f(x1-50, y_street, z2 - ring_thickness)
    glEnd()

    # ----- Franja inferior -----
    glBegin(GL_QUADS)
    glVertex3f(x1-50, y_street, z1 + ring_thickness)
    glVertex3f(x2+50, y_street, z1 + ring_thickness)
    glVertex3f(x2+50, y_street, z1)
    glVertex3f(x1-50, y_street, z1)
    glEnd()


    # ----- Franja derecha -----
    glBegin(GL_QUADS)
    glVertex3f(x2 - ring_thickness, y_street, z1-50)
    glVertex3f(x2 - ring_thickness, y_street, z2+50)
    glVertex3f(x2, y_street, z2+50)
    glVertex3f(x2, y_street, z1-50)
    glEnd()
    glPopMatrix()





def displayobj_central():
    """
    Dibuja la casa que va en el centro del plano (y=0).
    Ajusta la rotación/traslación/escala según tu OBJ.
    """
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)  # si tu modelo sale "acostado", ajusta
    glTranslatef(0.0, 0.0, 15.0)
    glScale(4.0, 4.0, 4.0)
    objetos[0].render()
    glPopMatrix()


def displayobjs_borders():
    """
    Dibuja la casa repetida en las orillas del plano XZ.
    Se usa la misma escala y rotación que la casa central.
    """
    spacing = 50  # Distancia entre casas
    positions = []

    # Borde superior e inferior
    for x in range(-DimBoard, DimBoard + 1, spacing):
        positions.append((x,  DimBoard))
        positions.append((x, -DimBoard))

    # Borde izquierdo y derecho
    for z in range(-DimBoard + spacing, DimBoard, spacing):
        positions.append((-DimBoard, z))
        positions.append(( DimBoard, z))

    for (x, z) in positions:
        glPushMatrix()
        glTranslatef(x, 0.0, z)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(0.0, 0.0, 15.0)
        glScale(10.0, 10.0, 10.0)
        objetos[0].render()
        glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    Axis()

    # Plano gris (suelo)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-DimBoard, 0, -DimBoard)
    glVertex3f(-DimBoard, 0,  DimBoard)
    glVertex3f( DimBoard, 0,  DimBoard)
    glVertex3f( DimBoard, 0, -DimBoard)
    glEnd()

    # Llamada al anillo (calle hueca) 
    draw_square_ring()

    # Dibujas cubos, casas en las orillas, casa central...
    for c in cubos:
        c.draw()
        c.update()

    displayobjs_borders()
    displayobj_central()



def main():
    done = False
    Init()
    global theta

    while not done:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if theta > 359.0:
                theta = 0
            else:
                theta += 1.0
            lookat()
        if keys[pygame.K_LEFT]:
            if theta < 1.0:
                theta = 360.0
            else:
                theta -= 1.0
            lookat()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        display()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
