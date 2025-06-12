import pygame
import sys
import math

# ordena os pontos pelo ângulo em relação ao centro
def ord_pontos_polig(points):
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    return sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

# polígonos
def varredura(surface, color, points):
    points = ord_pontos_polig(points)
    edges = sorted(points, key=lambda p: p[1])
    y_min, y_max = edges[0][1], edges[-1][1]

    for y in range(y_min, y_max):
        intersections = []
        for i in range(len(points)):
            p1, p2 = points[i], points[(i + 1) % len(points)]
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(int(x))

        intersections.sort()
        if len(intersections) % 2 == 0:
            for i in range(0, len(intersections), 2):
                pygame.draw.line(surface, color, (intersections[i], y), (intersections[i + 1], y))
                pygame.display.flip()
                pygame.time.delay(10)

    pygame.display.flip()

# retângulo
def varredura_retangulo(surface, color, rect):
    x_min, y_min, width, height = rect
    for y in range(y_min, y_min + height):
        pygame.draw.line(surface, color, (x_min, y), (x_min + width, y))
        pygame.display.flip()
        pygame.time.delay(10)
    pygame.display.flip()

# circunferência
def varredura_circunferencia(surface, color, center, radius):
    cx, cy = center
    for y in range(cy - radius, cy + radius):
        dx = math.sqrt(radius**2 - (y - cy)**2)
        x1, x2 = int(cx - dx), int(cx + dx)
        pygame.draw.line(surface, color, (x1, y), (x2, y))
        pygame.display.flip()
        pygame.time.delay(10)
    pygame.display.flip()

# seleção dos pontos para polígonos
def pontos_poligonos():
    points = []
    capturing = True
    while capturing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = ajusta_vertice(pygame.mouse.get_pos())  
                points.append(pos)
                pygame.draw.circle(screen, (0, 0, 255), pos, 5)
                pygame.display.flip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                capturing = False
    return points

# grade e o plano cartesiano
def draw_grade(surface):
    grid_color = (200, 200, 200)
    for x in range(0, WIDTH, tam_celula):
        pygame.draw.line(surface, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, tam_celula):
        pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y))

    axis_color = (0, 0, 0)
    pygame.draw.line(surface, axis_color, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.line(surface, axis_color, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)
    pygame.display.flip()

# ajusta um ponto ao vertice da grade mais próximo
def ajusta_vertice(pos):
    x, y = pos
    grid_x = round(x / tam_celula) * tam_celula
    grid_y = round(y / tam_celula) * tam_celula
    return (grid_x, grid_y)

pygame.init()

# tela
WIDTH, HEIGHT = 800, 600
tam_celula = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Preenchimento com Varredura com Análise Geométrica")
screen.fill((255, 255, 255))

running = True
polygon_points = None
selected_algorithm = None
draw_grade(screen)  
colors = {
    'varredura': (0, 255, 0)  
}

# loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_algorithm = 'varredura'
            elif event.key == pygame.K_2:
                varredura_retangulo(screen, (0, 0, 255), (200, 150, 200, 100))
            elif event.key == pygame.K_3:
                varredura_circunferencia(screen, (255, 0, 0), (400, 300), 80)

        if event.type == pygame.MOUSEBUTTONDOWN and polygon_points is None:
            polygon_points = pontos_poligonos()

        if polygon_points:
            if selected_algorithm == 'varredura':
                varredura(screen, colors['varredura'], polygon_points)

            polygon_points = None  

    pygame.display.flip()

pygame.quit()
sys.exit()
