from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Cubo:
    def __init__(self, agente):
        self.agente = agente

    def dibujar_caras(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[0])
        glVertex3fv(self.agente.points[1])
        glVertex3fv(self.agente.points[2])
        glVertex3fv(self.agente.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[4])
        glVertex3fv(self.agente.points[5])
        glVertex3fv(self.agente.points[6])
        glVertex3fv(self.agente.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[0])
        glVertex3fv(self.agente.points[1])
        glVertex3fv(self.agente.points[5])
        glVertex3fv(self.agente.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[1])
        glVertex3fv(self.agente.points[2])
        glVertex3fv(self.agente.points[6])
        glVertex3fv(self.agente.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[2])
        glVertex3fv(self.agente.points[3])
        glVertex3fv(self.agente.points[7])
        glVertex3fv(self.agente.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.agente.points[3])
        glVertex3fv(self.agente.points[0])
        glVertex3fv(self.agente.points[4])
        glVertex3fv(self.agente.points[7])
        glEnd()

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.agente.posicion[0], self.agente.posicion[1], self.agente.posicion[2])
        glScaled(self.agente.escala, self.agente.escala, self.agente.escala)

        # Cambiar color dinámicamente basado en riqueza
        riqueza_normalizada = max(0.1, self.agente.riqueza / 10)  # Normalizar para colores más visibles
        glColor3f(1.0 - riqueza_normalizada, riqueza_normalizada, 0.0)  # Gradiente rojo-amarillo-verde
        
        self.dibujar_caras()
        glPopMatrix()

    def actualizar(self):
        self.agente.actualizar_posicion()
