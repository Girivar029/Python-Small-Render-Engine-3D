import pygame
import numpy as np
import math


WIDTH, HEIGHT = 800,600
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('1st Attempt Basic Render')

clock = pygame.time.Clock()

vertices = np.array([
    [-1,-1,-1],
    [1,-1,-1],
    [1,1,-1],
    [-1,1,-1],
    [-1,-1,1],
    [1,-1,1],
    [1,1,1],
    [-1,1,1]
])

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

def project(point3d, angle_x, angle_y):
    rx = np.array([
        [1,0,0],
        [0,np.cos(angle_x),-np.sin(angle_x)],
        [0,np.sin(angle_x),np.cos(angle_x)]
    ])

    ry = np.array ([
        [np.cos(angle_y),0,np.sin(angle_y)],
        [0,1,0],
        [-np.sin(angle_y),0,np.cos(angle_y)]
    ])
    point3d = np.dot(rx,point3d)
    point3d = np.dot(ry,point3d)
    distance = 5
    factor = 200 / (distance+point3d[2])
    x = int(WIDTH // 2 + point3d[0] * factor)
    y = int(HEIGHT // 2 - point3d[1] * factor)
    return(x,y)

running = True
angle_x, angle_y = 0,0

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle_x += 0.1
    angle_y += 0.1

    projected = []
    for vertex in vertices:
        projected.append(project(vertex, angle_x, angle_y))

    for edge in edges:
        pygame.draw.line(screen, WHITE, projected[edge[0]],projected[edge[1]],2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()