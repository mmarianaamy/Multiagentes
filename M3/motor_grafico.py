import agentpy as ap
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Configuración de la ventana gráfica
screen_width = 800
screen_height = 600

# Configuración de la simulación
spawn_rate = 20  # Iteraciones entre la aparición de nuevos vehículos

class Vehiculo(ap.Agent):
    def setup(self):
        # Generar posición inicial en el centro (0,0) y mover hacia los bordes
        self.posicion = [0, 0]
        # Direcciones aleatorias hacia los bordes
        self.direccion = random.choice([
            [1, 0],   # Hacia la derecha
            [-1, 0],  # Hacia la izquierda
            [0, 1],   # Hacia arriba
            [0, -1]   # Hacia abajo
        ])

        self.velocidad = random.uniform(1, 3)
        self.aceleracion = random.uniform(0.1, 0.5)
        self.tipo = random.choice(["rápido", "lento", "pesado", "maniobrable"])
        self.semaforo_actual = None

    def mover(self):
        if self.semaforo_actual and self.semaforo_actual.estado == "rojo":
            self.frenar()
        else:
            self.acelerar()
        
        # Actualizar posición en la dirección establecida
        self.posicion[0] += self.direccion[0] * self.velocidad
        self.posicion[1] += self.direccion[1] * self.velocidad

        # Eliminar vehículos si llegan a los bordes
        if abs(self.posicion[0]) > 200 or abs(self.posicion[1]) > 200:
            self.model.vehiculos.remove(self)

    def acelerar(self):
        self.velocidad = min(self.velocidad + self.aceleracion, 5)

    def frenar(self):
        self.velocidad = max(self.velocidad - self.aceleracion, 0)

    def solicitar_verde(self, semaforo):
        if self.semaforo_actual is None:
            semaforo.recibir_solicitud(self)
            self.semaforo_actual = semaforo


class Semaforo(ap.Agent):
    def setup(self):
        self.estado = "rojo"
        self.temporizador = random.randint(10, 30)
        self.vehiculos_esperando = 0

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.temporizador = 20 if nuevo_estado == "verde" else 10

    def recibir_solicitud(self, vehiculo):
        self.vehiculos_esperando += 1

    def step(self):
        if self.temporizador > 0:
            self.temporizador -= 1
        else:
            if self.estado == "verde":
                self.cambiar_estado("rojo")
            elif self.vehiculos_esperando > 0:
                self.cambiar_estado("verde")
                self.vehiculos_esperando = 0


class Interseccion(ap.Model):
    def setup(self):
        self.semaforos = ap.AgentList(self, 2, Semaforo)
        self.vehiculos = ap.AgentList(self, 10, Vehiculo)

    def step(self):
        # Crear nuevos vehículos en cada intervalo de tiempo
        if self.t % spawn_rate == 0:
            self.vehiculos.append(Vehiculo(self))

        # Actualizar semáforos
        for semaforo in self.semaforos:
            semaforo.step()

        # Actualizar vehículos
        for vehiculo in self.vehiculos:
            vehiculo.mover()
            for semaforo in self.semaforos:
                if abs(vehiculo.posicion[1]) < 10 and abs(vehiculo.posicion[0]) < 10:
                    vehiculo.solicitar_verde(semaforo)


def Init():
    pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulación de Intersección con Semáforos Inteligentes")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (screen_width / screen_height), 0.1, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 300, 300, 0, 0, 0, 0, 1, 0)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)


def draw_axes():
    # Dibujar los ejes X, Y, Z
    glBegin(GL_LINES)
    # Eje X (rojo)
    glColor3f(1, 0, 0)
    glVertex3f(-200, 0, 0)
    glVertex3f(200, 0, 0)

    # Eje Z (azul)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -200)
    glVertex3f(0, 0, 200)

    # Eje Y (verde)
    glColor3f(0, 1, 0)
    glVertex3f(0, -200, 0)
    glVertex3f(0, 200, 0)
    glEnd()


def draw_intersection():
    # Dibujar las calles del cruce
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Color gris para las calles
    glVertex3f(-200, 0, -10)
    glVertex3f(200, 0, -10)
    glVertex3f(200, 0, 10)
    glVertex3f(-200, 0, 10)

    glVertex3f(-10, 0, -200)
    glVertex3f(10, 0, -200)
    glVertex3f(10, 0, 200)
    glVertex3f(-10, 0, 200)
    glEnd()


def draw_vehicle(vehicle):
    glPushMatrix()
    glTranslatef(vehicle.posicion[0], 0.5, vehicle.posicion[1])
    glScalef(5, 5, 5)  # Escalar el vehículo 5 veces más grande
    glColor3f(1, 0, 0) if vehicle.tipo == "rápido" else glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()
    glPopMatrix()


def display(model):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_axes()  # Dibujar los ejes
    draw_intersection()
    for vehicle in model.vehiculos:
        draw_vehicle(vehicle)
    pygame.display.flip()


def main():
    Init()
    model = Interseccion()
    model.setup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        model.step()
        display(model)
        pygame.time.wait(100)

    pygame.quit()

if __name__ == "__main__":
    main()
