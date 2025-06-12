import pygame
import sys

def bresenham(x1, y1, x2, y2):
    points = []
    
    steep = abs(y2 - y1) > abs(x2 - x1) # verifica se a inclinação é mais vertical
    
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = abs(y2 - y1)
    
    ystep = 1 if y1 < y2 else -1  # define a direção do incremento de y
    p = 2 * dy - dx  # parâmetro de decisão inicial como no slide
    y = y1
    
    for x in range(x1, x2 + 1):
        if steep:
            points.append((y, x))  # inverte de volta
        else:
            points.append((x, y))

        # decisão
        if p >= 0:
            y += ystep
            p += 2 * (dy - dx)
        else:
            p += 2 * dy
    
    return points

def draw_linha_bresenham(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    
    points = bresenham(x1, y1, x2, y2)
    
    for point in points:
        surface.set_at(point, color)
        pygame.display.flip()
        pygame.time.delay(5)

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algoritmo de Bresenham")
screen.fill((255, 255, 255))

running = True
points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(event.pos)
            if len(points) == 2:
                draw_linha_bresenham(screen, (255, 0, 0), points[0], points[1])
                points = []
    
    pygame.display.flip()

pygame.quit()
sys.exit()
