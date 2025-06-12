import pygame
import sys

# método Analítico
def draw_linha_analitica(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == 0:  # tratamento da reta vertical
        for y in range(y1, y2 + 1):
            surface.set_at((x1, y), color)
            pygame.display.flip()
            pygame.time.delay(5)
    else:
        m = dy / dx
        b = y1 - m * x1
        for x in range(x1, x2 + 1):
            y = round(m * x + b)
            surface.set_at((x, y), color)
            pygame.display.flip()
            pygame.time.delay(5)

# método DDA
def draw_linha_dda(surface, color, start, end, cell_size=20):
    x1, y1 = start
    x2, y2 = end

    x1, y1 = x1 // cell_size * cell_size, y1 // cell_size * cell_size
    x2, y2 = x2 // cell_size * cell_size, y2 // cell_size * cell_size

    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return

    Xinc = dx / steps
    Yinc = dy / steps

    x, y = x1, y1
    for _ in range(steps):
        surface.set_at((round(x), round(y)), color)
        pygame.display.flip()
        pygame.time.delay(5)
        x += Xinc
        y += Yinc

# algoritmo de Bresenham (Incorreto)
# def draw_linha_bresenham(surface, color, start, end, cell_size=20):
#    x1, y1 = start
#    x2, y2 = end
#
#    x1, y1 = x1 // cell_size * cell_size, y1 // cell_size * cell_size
#    x2, y2 = x2 // cell_size * cell_size, y2 // cell_size * cell_size
#
#    dx = abs(x2 - x1)
#    dy = abs(y2 - y1)
#    sx = 1 if x1 < x2 else -1
#    sy = 1 if y1 < y2 else -1
#    err = dx - dy
#
#    while True:
#        surface.set_at((x1, y1), color)
#        pygame.display.flip()
#        pygame.time.delay(5)
#
#        if x1 == x2 and y1 == y2:
#            break
#
#        e2 = 2 * err
#        if e2 > -dy:
#            err -= dy
#            x1 += sx
#        if e2 < dx:
#            err += dx
#            y1 += sy

# grade
def draw_grade(surface, width, height, cell_size=20):
    grid_color = (200, 200, 200)  # Cinza claro

    for x in range(0, width, cell_size):
        pygame.draw.line(surface, grid_color, (x, 0), (x, height))

    for y in range(0, height, cell_size):
        pygame.draw.line(surface, grid_color, (0, y), (width, y))

pygame.init()

# tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desenho de Retas")
screen.fill((255, 255, 255))
draw_grade(screen, WIDTH, HEIGHT)

font = pygame.font.Font(None, 36)
text = font.render("1 - Analítico // 2 - Método DDA", True, (0, 0, 0))
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
            draw_linha_analitica: (0, 0, 255),
            draw_linha_dda: (0, 255, 0),
            # draw_linha_bresenham: (255, 0, 0)
        }
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                algoritmo_selecionado = draw_linha_analitica
            elif event.key == pygame.K_2:
                algoritmo_selecionado = draw_linha_dda
            # elif event.key == pygame.K_3:
            #    algoritmo_selecionado = draw_linha_bresenham

        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(event.pos)
            if len(points) == 2:
                if algoritmo_selecionado == draw_linha_analitica:
                    draw_linha_analitica(screen, colors[algoritmo_selecionado], points[0], points[1])
                elif algoritmo_selecionado == draw_linha_dda:
                    draw_linha_dda(screen, colors[algoritmo_selecionado], points[0], points[1])
                # elif algoritmo_selecionado == draw_linha_bresenham:
                #    draw_linha_bresenham(screen, colors[algoritmo_selecionado], points[0], points[1])
                points = []
    
pygame.display.flip()

pygame.quit()
sys.exit()