import pygame
import numpy as np

WIDTH, HEIGHT = 800,600
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('3d Renderer...')
clock = pygame.time.Clock()

class Vector3:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x,y,z
    def to_array(self):
        return np.array([self.x,self.y,self.z])
    
class Camera:
    def __init__(self,position):
        self.position = position
        self.angle_x = 0
        self.angle_y = 0
        self.distance = 5

def rotation_matrix_x(angle):
    c,s = np.cos(angle),np.sin(angle)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def rotation_matrix_y(angle):
    c,s = np.cos(angle),np.sin(angle)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def project(point, camera):
    rotated = np.dot(rotation_matrix_x(camera.angle_x),point)
    rotated = np.dot(rotation_matrix_y(camera.angle_y),rotated)
    factor = 200 / (camera.distance + rotated[2])
    x = int(WIDTH / 2 + rotated[0] * factor)
    y = int(HEIGHT / 2 - rotated[1] * factor)
    return (x,y)

class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

cube_vertices = [
    Vector3(-1,-1,-1), Vector3(1,-1,-1), Vector3(1,1,-1),
    Vector3(-1,1,-1), Vector3(-1,-1,1), Vector3(1,-1,1),
    Vector3(1,1,1), Vector3(-1,1,1)
]

cube_faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (1, 2, 6, 5),
    (0, 3, 7, 4)   
]

mesh = Mesh(cube_vertices, cube_faces)
camera = Camera(Vector3(0,0,-5))

running = True
mouse_down = False
last_mouse_pos = (0,0)

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == pygame.MOUSEMOTION and mouse_down:
            x,y = pygame.mouse.get_pos()
            dx,dy = x - last_mouse_pos[0],y - last_mouse_pos[1]
            camera.angle_y += dx * 0.01
            camera.angle_x += dy * 0.01
            last_mouse_pos = (x,y)

    for face in mesh.faces:
        points = [project(mesh.vertices[i].to_array(),camera)for i in face]
        pygame.draw.polygon(screen, (255,255,255), points, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()     