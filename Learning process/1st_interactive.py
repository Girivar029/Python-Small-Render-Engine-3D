import pygame
import numpy as np

WIDTH, HEIGHT = 800,600
WHITE = (255,255,255)
BLACk = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Interactive cube')
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

angle_x, angleY = 0,0
distance = 5
mouse_sensitivity = 0.005

def project(point3d, angle_x, angle_y, distance):
    rx = np.array([
        [1,0,0],
        [0,np.cos(angle_x),-np.sin(angle_x)],
        [0,np.sin(angle_x), np.cos(angle_x)]
    ])

    ry = np.array([
        [np.cos(angle_y),0,np.sin(angle_y)],
        [0,1,0],
        [-np.sin(angle_y),0,np.cos(angle_y)]
    ])

    point3d = np.dot(rx, point3d)
    point3d = np.dot(ry, point3d)
    factor = 200 / (distance + point3d[2])
    x = int(WIDTH / 2 + point3d[0] * factor)
    y = int(HEIGHT/2 - point3d[1] * factor)
    return (x,y)

running = True
is_dragging = False
last_mouse_position = None

while running:
    screen.fill(BLACk)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_dragging = True
                last_mouse_position = pygame.mouse.get_pos()
            elif event.button == 4:
                distance = max(1,distance - 0.5)
            elif event.button == 5:
                distance+= 5
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                x,y = pygame.mouse.get_pos()
                dx,dy = -x - last_mouse_position[0],-y - last_mouse_position[1]
                angleY += dx * mouse_sensitivity
                angle_x += dy * mouse_sensitivity
                last_mouse_position = (-x,-y)
    projected = [project(v,angle_x, angleY, distance)for v in vertices]

    for edge in edges:
        pygame.draw.line(screen, WHITE, projected[edge[0]], projected[edge[1]],2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()