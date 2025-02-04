import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys
import random

sys.path.append('..')
from Carro import Carro
from Semaforo import Semaforo
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
DimBoardHeight = 200
DimBoardWidth = 300

# Carros
cubos = []
ncubos =  0

semaforos = []
nsemaforos = 2


# Lista de objetos .OBJ (las casas)
#casas = []

# Lista de objetos .OBJ (los carros)
#carros = []

# Lista de objetos .OBJ (los arboles)
#arboles = []

traffic_light = []

# Control para la cámara orbital
theta  = 0.0
radius = 300

# Arreglo para manejo de texturas
textures = []
image1 = "Avance Reto/Modelos/grass.jpg"
image2 = "Avance Reto/Modelos/background.jpg"


# Dimensiones de las intersecciones
intersection_width = 50
intersection_height = 50

# Posiciones de las intersecciones
intersection_positions = [
    (150, 0),  # Primera intersección
    (-150, -0)  # Segunda intersección
]

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
    
def generar_carro():
    
    """Genera un carro solo en las posiciones definidas moviéndose de abajo hacia arriba."""
    puntos_generacion = [
        ([140, 1, -200], [0, 0, 1]),   # De abajo hacia arriba
        ([-160, 1, -200], [0, 0, 1]),  # De abajo hacia arriba
        ([160, 1, 200], [0, 0, -1]),   # De arriba hacia abajo
        ([-140, 1, 200], [0, 0, -1])   # De arriba hacia abajo
    ]
    
    
    position, direction = random.choice(puntos_generacion)  # Selecciona una de las posiciones iniciales
    velocidad = 1.0  # Velocidad del carro
    #direction = [0, 0, 1]  # Movimiento de abajo hacia arriba

    return Carro(position=position, vel=velocidad, direction=direction)


"""Genera un nuevo carro solo en los lados derecho (x+) e inferior (z-) en posiciones fijas"""
    #lado = random.choice(["x+", "z-"])  # Solo aparecen en dos lados
    #velocidad = 1.0  # Puedes ajustar según el tipo de vehículo

    #if lado == "x+":  # Desde la derecha hacia la izquierda
        #return Carro([DimBoardWidth, 0, 0], velocidad, [-1, 0, 0])  
    #elif lado == "z-":  # Desde abajo hacia arriba
        #return Carro([0, 0, -DimBoardHeight], velocidad, [0, 0, 1])  
    
import pygame
ultimo_spawn = 0  
intervalo_spawn = 4000  

def ha_salido_de_simulacion(carro):
    """Verifica si el carro ha pasado el área de simulación y debe ser eliminado"""
    #x, _, z = carro.Position
    _, _, z = carro.Position
    
    #limite1 = DimBoardWidth - 5  # 🔥 Ahora eliminamos antes de que lleguen al borde
    #limite2 = DimBoardHeight - 5  # 🔥 Ahora eliminamos antes de que lleguen al borde

    #if -x > limite1 or z > limite2:
        #return True
    #return False
    
#    if z > DimBoardHeight or z < DimBoardWidth:
    if z > DimBoardHeight or z < -DimBoardHeight:
        #print(f"Carro fuera de pantalla en {carro.Position}")  # 👀
        print(f"Carro eliminado en {carro.Position}")
        return True
    return False

def actualizar_carros():
    global cubos, ultimo_spawn
    
    # Eliminar carros que han salido de la simulación
    cubos = [carro for carro in cubos if not ha_salido_de_simulacion(carro)]

    # Verificar si han pasado 10 segundos desde el último spawn
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_spawn >= intervalo_spawn:
        # Generar 1 o 2 carros nuevos
        cantidad_carros = random.choice([2, 3])  
        for _ in range(cantidad_carros):
            nuevo_carro = generar_carro()
            nuevo_carro.setotrosagentes(cubos)
            nuevo_carro.setsemaforos(semaforos)
            cubos.append(nuevo_carro)
            print(f"Carro generado en {nuevo_carro.Position}")  # 👀 Verifica que se están creando
        
        ultimo_spawn = tiempo_actual 
    
def Init():
    global cubos, semaforos, textures, traffic_light
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL
    )
    pygame.display.set_caption("Avance Reto: Ciudad")

    # Proyección en perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    # Cámara
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    #glClearColor(0, 0, 0, 0)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Azul claro
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Carga la textura usando la función loadTexture de la clase OBJ
    # y la agrega a la lista de texturas
    texture_id = OBJ.loadTexture(image1)
    textures.append(texture_id)
    
    background_texture = OBJ.loadTexture(image2)
    textures.append(background_texture)

    # Cargar la nueva textura para las intersecciones
    #intersection_texture_id = OBJ.loadTexture("Avance Reto/Modelos/Calle2.jpg")
    #textures.append(intersection_texture_id)

    """
    # Cubos de ejemplo
    for _ in range(ncubos):
        cubos.append(Cubo(DimBoard, 1.0, 5.0))
    for c in cubos:
        c.getCubos(cubos)
    """
    
    semaforos = [
        Semaforo(-160, 0, -50, 5.0, 0, [0, 0, 1]),
        Semaforo(140, 0, -50, 5.0, 1, [1, 0, 0]),
        Semaforo(-140, 0, 50, 5.0, 0, [0, 0, 1]),
        Semaforo(160, 0, 50, 5.0, 1, [1, 0, 0])
    ]
    
    for semaforo in semaforos:
        semaforo.otros_semaforos = [s for s in semaforos if s != semaforo]
    cubos = []


    # Configuramos iluminación
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 200.0, 0.0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    # Cargamos los modelos de las casas
    #casas.append(OBJ("Avance Reto\Modelos\edificio_chido\edificio_chido2.obj", swapyz=True))
    #casas[0].generate()
    #casas.append(OBJ("Avance Reto/Modelos/parque.obj", swapyz=True))
    #casas[1].generate()
    #casas.append(OBJ("Avance Reto/Modelos/Building,.obj", swapyz=True))
    #casas[2].generate()
    #casas.append(OBJ("Avance Reto/Modelos/building_05.obj", swapyz=True))
    #casas[3].generate()
    #casas.append(OBJ("Avance Reto/Modelos/Bambo_House.obj", swapyz=True))
    #casas[4].generate()
    
    # Cargamos los modelos de los carros
    #carros.append(OBJ("Avance Reto\Modelos\Chevrolet_Camaro_SS_Low.obj", swapyz=True))
    #carros[0].generate()
    #carros.append(OBJ("Avance Reto\Modelos\Jeep_Renegade_2016.obj", swapyz=True))
    #carros[1].generate()
    
    # Cargamos los modelos de los semaforos
    traffic_light.append(OBJ("Avance Reto\\Modelos\\traffic_light.obj", swapyz = True))
    traffic_light[0].generate()
    traffic_light.append(OBJ("Avance Reto\\Modelos\\traffic_light.obj", swapyz=True))
    print(f"Modelo del semáforo cargado: {traffic_light}")  # Verifica si se cargó


    # Cargamos los modelos de los arboles
    #arboles.append(OBJ("Avance Reto\Modelos\Trees\Trees2.obj", swapyz=True))
    #arboles[0].generate()
    #arboles.append(OBJ("Avance Reto\Modelos\Bench\white_bench.obj", swapyz=True))
    #arboles[1].generate()



def lookat():
    """
    Mueve la cámara en círculo alrededor del centro, altura fija EYE_Y.
    """
    global EYE_X, EYE_Z, radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)


def draw_road():
    
    texture_id = OBJ.loadTexture("Avance Reto/Modelos/Calle.jpg")  # Cambia por el camino a tu imagen
    glEnable(GL_TEXTURE_2D)
    margin = 50
    road_width = 50
    y_street = 1.0

    # Escala y rotación
    scale_factor = 1.0  
    rotation_angle = 90  #  rotar la textura

    #glBindTexture(GL_TEXTURE_2D, texture_id)

    # Coordenadas de la carretera
    x1 = -DimBoardWidth #+ margin
    x2 =  DimBoardWidth #- margin
    z1 = -DimBoardHeight #+ margin
    z2 =  DimBoardHeight #- margin

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Mantén el color blanco para no alterar la textura

    # Aplicar rotación a las coordenadas de textura
    glMatrixMode(GL_TEXTURE)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.5, 0.5, 0.0)  # Trasladar el centro de rotación al medio de la textura
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotar la textura
    glTranslatef(-0.5, -0.5, 0.0)  # Regresar el centro de rotación

    glBegin(GL_QUADS)

    # ----- Franja central -----
    #glTexCoord2f(0.0, scale_factor); glVertex3f(x1-50, y_street, z2)
    #glTexCoord2f(scale_factor, scale_factor); glVertex3f(x2+50, y_street, z2)
    #glTexCoord2f(scale_factor, 0.0); glVertex3f(x2+50, y_street, z2 - ring_thickness)
    #glTexCoord2f(0.0, 0.0); glVertex3f(x1-50, y_street, z2 - ring_thickness)
    
    # ----- Franja central -----
    glTexCoord2f(0.0, 0.0); glVertex3f(x1, y_street, 0 - road_width/2)
    glTexCoord2f(1.0, 0.0); glVertex3f(x2, y_street, 0 - road_width/2)
    glTexCoord2f(1.0, 1.0); glVertex3f(x2, y_street, 0 + road_width/2)
    glTexCoord2f(0.0, 1.0); glVertex3f(x1, y_street, 0 + road_width/2)

    # ----- Franja izquierda -----
    glTexCoord2f(0.0, 0.0); glVertex3f(x1 - road_width/2 + 150, y_street, z1)
    glTexCoord2f(1.0, 0.0); glVertex3f(x1 - road_width/2 + 150, y_street, z2)
    glTexCoord2f(1.0, 1.0); glVertex3f(x1 + road_width/2 + 150, y_street, z2)
    glTexCoord2f(0.0, 1.0); glVertex3f(x1 + road_width/2 + 150, y_street, z1)

    # ----- Franja derecha -----
    glTexCoord2f(0.0, 0.0); glVertex3f(x2 - road_width/2 - 150, y_street, z1)
    glTexCoord2f(1.0, 0.0); glVertex3f(x2 - road_width/2 - 150, y_street, z2)
    glTexCoord2f(1.0, 1.0); glVertex3f(x2 + road_width/2 - 150, y_street, z2)
    glTexCoord2f(0.0, 1.0); glVertex3f(x2 + road_width/2 - 150, y_street, z1)

    glEnd()

    # Deshacer rotación
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glPopMatrix()

#"""
def draw_intersection(x, z, width, height):
    texture_id = OBJ.loadTexture("Avance Reto/Modelos/Calle2.jpg")  # Cambia por el camino a tu imagen
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
        
    y_level = 1.1  # Ligeramente por encima de la calle para evitar z-fighting

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Mantén el color blanco para no alterar la textura

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(x - width / 2, y_level, z - height / 2)
    glTexCoord2f(1.0, 0.0); glVertex3f(x + width / 2, y_level, z - height / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f(x + width / 2, y_level, z + height / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f(x - width / 2, y_level, z + height / 2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
"""



def displayobj_carro(x, y, z, a, b, c, i):
    
    #Dibuja los carros que van sobre la carretera.
    #Ajusta la rotación/traslación/escala según tu OBJ.
    
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)  # si tu modelo sale "acostado", ajusta
    glTranslatef(x, y, z)
    glScale(a,b,c)
    carros[i].render()
    glPopMatrix()


def displayobj_arboles(x, y, z, a, b, c, i):
    
    #Dibuja las casas en el plano.
    #Ajusta la rotación/traslación/escala según tu OBJ.
    
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90.0, 1.0, 0.0, 0.0)  # si tu modelo sale "acostado", ajusta
    glScale(a, b, c)
    arboles[i].render()
    glPopMatrix()

def displayobj_casa(x, y, z, a, b, c, i):
    
    #Dibuja las casas en el plano.
    #Ajusta la rotación/traslación/escala según tu OBJ.
    
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90.0, 1.0, 0.0, 0.0)  # si tu modelo sale "acostado", ajusta
    glScale(a, b, c)
    casas[i].render()
    glPopMatrix()
"""

def displayobj_semaforo(x, y, z, a, b, c, i):
    
    #Dibuja las casas en el plano.
    #Ajusta la rotación/traslación/escala según tu OBJ.
    
    glPushMatrix()
    glTranslatef(x, y, z)
    if z > 0:
        glRotatef(180, 0, 1, 0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)  # si tu modelo sale "acostado", ajusta
    glScale(a, b, c)
    traffic_light[i].render()
    glPopMatrix()


def Plano():
    # Plano gris (suelo)
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-DimBoardWidth/2, 0, -DimBoardHeight/2)
        glVertex3f(-DimBoardWidth/2, 0,  DimBoardHeight/2)
        glVertex3f( DimBoardWidth/2, 0,  DimBoardHeight/2)
        glVertex3f( DimBoardWidth/2, 0, -DimBoardHeight/2)
        glEnd()
        
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoardWidth, 0, -DimBoardHeight)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoardWidth, 0, DimBoardHeight)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoardWidth, 0, DimBoardHeight)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoardWidth, 0, -DimBoardHeight)
    glEnd()              
    glDisable(GL_TEXTURE_2D)
    
def draw_background():
    #"""
    #Dibuja una imagen de fondo como skybox.
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    
    glPushMatrix()
    glLoadIdentity()
    #gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)  # Fija la vista
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-600, -200, -1000)
    glTexCoord2f(1, 0); glVertex3f(600, -200, -1000)
    glTexCoord2f(1, 1); glVertex3f(600, 400, -1000)
    glTexCoord2f(0, 1); glVertex3f(-600, 400, -1000)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    #"""

    
def draw_cars():
    for carro in cubos:
        carro.draw()
        carro.update()
        
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_background()
    Axis()
    PlanoTexturizado()

    draw_road()
    #draw_intersection()
    
    # Dibujar las intersecciones
    for pos in intersection_positions:
        draw_intersection(pos[0], pos[1], intersection_width, intersection_height)


    # Dibujas cubos, casas en las orillas, casa central...
    #for c in cubos:
        #c.draw()
        #c.update()
    draw_cars()
    # Dibuja semaforos
    for obj in semaforos:
        obj.draw()
        obj.update([s for s in semaforos if s != obj])

    #for tl in traffic_light:
        #tl.render()
    #displayobjs_casas()
    
    """
    # Dibujar carros
    displayobj_carro(135.0, -50.0, 5.0, 5.0, 5.0, 5.0, 0)
    displayobj_carro(140.0, 50.0, 5.0, 10.0, 10.0, 10.0, 1)
    
    # Dibujar casas
    displayobj_casa(-150, 0.0, -180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-100, 0.0, -180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-50, 0.0, -180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-0, 0.0, -180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(50, 0.0, -180, 5.0, 5.0, 5.0, 0)

    displayobj_casa(-150, 0.0, 180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-100, 0.0, 180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-50, 0.0, 180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(-0, 0.0, 180, 5.0, 5.0, 5.0, 0)
    displayobj_casa(50, 0.0, 180, 5.0, 5.0, 5.0, 0)
    
    displayobj_casa(180, 0.0, -30, 5.0, 5.0, 5.0, 0)
    displayobj_casa(180, 0.0, -80, 5.0, 5.0, 5.0, 0)
    
    displayobj_casa(180, 0.0, 80, 5.0, 5.0, 5.0, 0)
    displayobj_casa(180, 0.0, 30, 5.0, 5.0, 5.0, 0)
    
    # Dibujar arboles
    displayobj_arboles(180, 0.0, -180, 3.0, 3.0, 3.0, 0)
    displayobj_arboles(80, 0.0, 180, 3.0, 3.0, 3.0, 1) # banca

    displayobj_semaforo(160, 0, -100, 0.3, 0.3, 0.3, 0)
    """
    displayobj_semaforo(120, 0, -50, 2.0, 2.0, 2.0, 0)
    displayobj_semaforo(180, 0, 50, 2.0, 2.0, 2.0, 0)
    displayobj_semaforo(-120, 0, 50, 2.0, 2.0, 2.0, 0)
    displayobj_semaforo(-180, 0, -50, 2.0, 2.0, 2.0, 0)

    
    #displayobj_casa(50.0, 0.0, 50.0, 10.0, 10.0, 10.0, 1)
    #displayobj_casa(100.0, 0.0, 100.0, 10.0, 10.0, 10.0, 2)
    #displayobj_casa(150.0, 0.0, 150.0, 10.0, 10.0, 10.0, 3)
    #displayobj_casa(200.0, 0.0, 200.0, 10.0, 10.0, 10.0, 4)
"""

    # Dibujar carros
    if len(carros) > 0:
        displayobj_carro(135.0, -50.0, 5.0, 5.0, 5.0, 0)
    if len(carros) > 1:
        displayobj_carro(140.0, 50.0, 5.0, 10.0, 10.0, 1)

    # Dibujar casas
    if len(casas) > 0:
        displayobj_casa(0.0, 0.0, 0.0, 10.0, 10.0, 10.0, 0)
    if len(casas) > 1:
        displayobj_casa(50.0, 0.0, 50.0, 10.0, 10.0, 10.0, 1)
"""
    #pygame.display.flip()
    
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
                    
        actualizar_carros()
        #draw_cars()
        display()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
