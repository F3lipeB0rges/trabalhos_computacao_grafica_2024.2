import pygame
import sys
import math

# método Equação Paramétrica
def draw_circ_parametrica(surface, color, center, radius):
    cx, cy = center
    for angle in range(0, 360, 1):
        theta = math.radians(angle)
        x = int(cx + radius * math.cos(theta))
        y = int(cy + radius * math.sin(theta))
        surface.set_at((x, y), color)
        pygame.display.flip()
        pygame.time.delay(5)

# método Incremental com Simetria
def draw_circ_incremental(surface, color, center, radius):
    cx, cy = center
    x = radius
    y = 0
    theta = 1 / radius  # incremento angular
    C = math.cos(theta)
    S = math.sin(theta)

    while y <= x:
        points = [
            (int(cx + x), int(cy + y)), (int(cx - x), int(cy + y)), 
            (int(cx + x), int(cy - y)), (int(cx - x), int(cy - y)),
            (int(cx + y), int(cy + x)), (int(cx - y), int(cy + x)), 
            (int(cx + y), int(cy - x)), (int(cx - y), int(cy - x))
        ]
        for point in points:
            surface.set_at(point, color)
        pygame.display.flip()
        pygame.time.delay(5)

        xt = x
        x = x * C - y * S
        y = y * C + xt * S


# algoritmo de Bresenham
def draw_circ_bresenham(surface, color, center, radius):
    cx, cy = center
    x = 0
    y = radius
    d = 3 - 2 * radius
    while y >= x:
        points = [
            (cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)
        ]
        for point in points:
            surface.set_at(point, color)
        pygame.display.flip()
        pygame.time.delay(5)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

# grade
def draw_grade(surface, width, height, cell_size=20):
    grid_color = (200, 200, 200)

    for x in range(0, width, cell_size):
        pygame.draw.line(surface, grid_color, (x, 0), (x, height))

    for y in range(0, height, cell_size):
        pygame.draw.line(surface, grid_color, (0, y), (width, y))

pygame.init()

# tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desenhando Circunferências - Escolha o Algoritmo")
screen.fill((255, 255, 255))
draw_grade(screen, WIDTH, HEIGHT)

font = pygame.font.Font(None, 36)
text = font.render("1 - Paramétrico // 2 - Incremental // 3 - Bresenham", True, (0, 0, 0))
screen.blit(text, (20, 20))
pygame.display.flip()

running = True
points = []
algoritmo_selecionado = None

# loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        colors = {
            draw_circ_parametrica: (0, 0, 255),
            draw_circ_incremental: (0, 255, 0), 
            draw_circ_bresenham: (255, 0, 0) 
        }
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                algoritmo_selecionado = draw_circ_parametrica
            elif event.key == pygame.K_2:
                algoritmo_selecionado = draw_circ_incremental
            elif event.key == pygame.K_3:
                algoritmo_selecionado = draw_circ_bresenham
        
        if event.type == pygame.MOUSEBUTTONDOWN and algoritmo_selecionado:
            points.append(event.pos)
            if len(points) == 2:
                cx, cy = points[0]
                px, py = points[1]
                radius = int(math.sqrt((px - cx) ** 2 + (py - cy) ** 2))
                algoritmo_selecionado(screen, (0, 0, 0), (cx, cy), radius)
                points = []

                algoritmo_selecionado(screen, colors[algoritmo_selecionado], (cx, cy), radius)
                points = []
    
    pygame.display.flip()

pygame.quit()
sys.exit()
