
import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

from Message import Message

class Semaforo:
    
    def __init__(self, x, y, z, scale, semaforo_id, direction):
        self.id = semaforo_id
        self.points = [[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]]
        self.scale = scale
        self.estado = "ROJO"
        self.TIEMPO_VERDE = 200
        self.TIEMPO_AMARILLO = 50
        self.TIEMPO_ROJO = 200

        self.temporizador = self.TIEMPO_ROJO
        self.Position = [x, y, z]
        
        self.esperando = False
        self.otros_semaforos = []
        self.direction = direction


    def take_msg(self):
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:
                if msg.performative == "activar":
                    self.temporizador -= 1

    def update(self, otros_semaforos):

        self.take_msg()

        # Verificar si otro semáforo está en verde

        semaforo_verde = any(semaforo.estado == "VERDE" for semaforo in otros_semaforos if semaforo.id != self)

        if not semaforo_verde or self.estado != "ROJO":
            self.temporizador -= 1

        if self.temporizador <= 0:
            if self.estado == "ROJO" and not semaforo_verde:
                self.estado = "VERDE"
                self.temporizador = self.TIEMPO_VERDE
            elif self.estado == "VERDE":
                self.estado = "AMARILLO"
                self.temporizador = self.TIEMPO_AMARILLO
            elif self.estado == "AMARILLO":
                self.estado = "ROJO"
                self.temporizador = self.TIEMPO_ROJO
    
    def recibir_solicitud(self):
        if self.estado == "ROJO":
            self.esperando = True


    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale,self.scale,self.scale)
        # Cambiar el color según el estado
        if self.estado == "ROJO":
            glColor3f(1.0, 0.0, 0.0)
        elif self.estado =="AMARILLO":
            glColor3f(1.0, 1.0, 0.0)
        elif self.estado == "VERDE":
            glColor3f(0.0, 1.0 ,0.0)
        
        self.drawFaces()
        glPopMatrix()
    
    def returnState(self, receiver):
        msg = Message(sender=self.id, receiver=receiver.id, performative="responder",content={"verde": self.estado == "VERDE"})
        msg.send()
        
