import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from AgentModel import AgenteCubo
from Cubo import Cubo

# Parámetros de la simulación
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 800
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 1000.0

# Parámetros de la cámara
EYE_X, EYE_Y, EYE_Z = 300.0, 200.0, 300.0
CENTER_X, CENTER_Y, CENTER_Z = 0.0, 0.0, 0.0
UP_X, UP_Y, UP_Z = 0.0, 1.0, 0.0

# Dimensiones del plano
DIM_TABLERO = 200

# Inicialización de agentes y cubos
NUM_CUBOS = 30
VELOCIDAD = 2.0
ESCALA_INICIAL = 5.0

pygame.init()

cubos = []
agentes = []

# Ejes del sistema

def dibujar_ejes():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # Eje X (rojo)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-DIM_TABLERO, 0, 0)
    glVertex3f(DIM_TABLERO, 0, 0)
    # Eje Y (verde)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, -DIM_TABLERO, 0)
    glVertex3f(0, DIM_TABLERO, 0)
    # Eje Z (azul)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, -DIM_TABLERO)
    glVertex3f(0, 0, DIM_TABLERO)
    glEnd()

# Inicialización de OpenGL
def inicializar():
    screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulación 3D: Transferencia de Riqueza")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, ANCHO_PANTALLA / ALTO_PANTALLA, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Crear agentes y cubos
    for _ in range(NUM_CUBOS):
        agente = AgenteCubo(DIM_TABLERO, VELOCIDAD, ESCALA_INICIAL)
        agentes.append(agente)
        cubos.append(Cubo(agente))

    # Compartir referencias entre agentes
    for agente in agentes:
        agente.establecer_agentes(agentes)

def dibujar_escena():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    dibujar_ejes()

    # Dibujar plano
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-DIM_TABLERO, 0, -DIM_TABLERO)
    glVertex3f(-DIM_TABLERO, 0, DIM_TABLERO)
    glVertex3f(DIM_TABLERO, 0, DIM_TABLERO)
    glVertex3f(DIM_TABLERO, 0, -DIM_TABLERO)
    glEnd()

    # Dibujar cubos
    for cubo in cubos:
        cubo.dibujar()
        cubo.actualizar()

def simulacion():
    inicializar()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                ejecutando = False

        dibujar_escena()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    simulacion()
