import pygame
import random
import math
import time

pygame.init()

pygame.mixer.music.load("Tetris Theme.mp3")
pygame.mixer.music.set_volume(0.1)  # Define o volume (0.0 a 1.0)
pygame.mixer.music.play(-1) 

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TETRIS")

# fonte personalizada
pygame.font.init()
font_path = "PressStart2P.ttf"

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [(0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0), (255, 0, 0), (255, 165, 0), (0, 0, 255)]

# Tamanho do bloco
BLOCK_SIZE = 30

# Grade do Tetris
GRID_WIDTH = 10
GRID_HEIGHT = 20
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Definição das peças
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Função para desenhar gradiente no fundo
def draw_gradient_background(colors):
    """
    Desenha um gradiente de cores no fundo da tela.
    Técnica de Computação Gráfica: Interpolação de cores.
    """
    for y in range(SCREEN_HEIGHT):
        color = (
            int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / SCREEN_HEIGHT),
            int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / SCREEN_HEIGHT),
            int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / SCREEN_HEIGHT)
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

# Função para desenhar texto 3D
def draw_3d_text(text, font, x, y, color, depth):
    """
    Desenha texto com efeito 3D.
    Técnica de Computação Gráfica: Deslocamento e escurecimento de camadas.
    """
    for i in range(depth):
        text_surface = font.render(text, True, (color[0] // (i + 1), color[1] // (i + 1), color[2] // (i + 1)))
        screen.blit(text_surface, (x - i, y - i))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função para desenhar a grade
def draw_grid():
    """
    Desenha a grade do Tetris.
    Técnica de Computação Gráfica: Rasterização de retângulos.
    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, COLORS[grid[y][x] - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Função para desenhar uma peça
def draw_piece(piece, x, y, color):
    """
    Desenha uma peça do Tetris.
    Técnica de Computação Gráfica: Rasterização de retângulos.
    """
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                pygame.draw.rect(screen, color, ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Função para desenhar sombra da peça
def draw_shadow(piece, x, y, color):
    """
    Desenha a sombra da peça atual.
    Técnica de Computação Gráfica: Rasterização de retângulos com transparência.
    """
    shadow_y = y
    while not check_collision(piece, x, shadow_y + 1):
        shadow_y += 1
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                pygame.draw.rect(screen, (color[0] // 2, color[1] // 2, color[2] // 2), ((x + col) * BLOCK_SIZE, (shadow_y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Função para verificar colisão
def check_collision(piece, x, y):
    """
    Verifica se uma peça colide com a grade ou outras peças.
    Técnica de Computação Gráfica: Verificação de limites e sobreposição.
    """
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                if y + row >= GRID_HEIGHT or x + col < 0 or x + col >= GRID_WIDTH or grid[y + row][x + col]:
                    return True
    return False

# Função para rotacionar uma peça
def rotate_piece(piece):
    """
    Rotaciona uma peça do Tetris.
    Técnica de Computação Gráfica: Transformação geométrica (rotação de matriz).
    """
    return [list(row) for row in zip(*piece[::-1])]

# Função para remover linhas completas
def remove_complete_lines():
    """
    Remove linhas completas e exibe uma animação.
    Técnica de Computação Gráfica: Animação de piscar.
    """
    lines_removed = 0
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            for _ in range(3):  # Animação de piscar
                for x in range(GRID_WIDTH):
                    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.display.flip()
                pygame.time.wait(50)
                for x in range(GRID_WIDTH):
                    pygame.draw.rect(screen, COLORS[grid[row][x] - 1], (x * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.display.flip()
                pygame.time.wait(50)
            del grid[row]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_removed += 1
    return lines_removed

# Função para desenhar partículas (efeito visual)
def draw_particles(x, y, color):
    """
    Desenha partículas para efeitos visuais.
    Técnica de Computação Gráfica: Movimento com trigonometria.
    """
    for _ in range(20):  # 20 partículas
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        dx = int(speed * math.cos(angle))
        dy = int(speed * math.sin(angle))
        pygame.draw.circle(screen, color, (x + dx, y + dy), 2)

# Função para mostrar o menu principal
def show_menu():
    """
    Exibe o menu principal do jogo.
    Técnica de Computação Gráfica: Renderização de texto e botões.
    """
    font_title = pygame.font.Font(font_path, 48)
    font_options = pygame.font.Font(font_path, 24)
    title_text = "TETRIS"
    start_text = font_options.render("1 - Jogar", True, WHITE)
    highscores_text = font_options.render("2 - Recordes", True, WHITE)
    difficulty_text = font_options.render("3 - Dificuldade", True, WHITE)
    quit_text = font_options.render("4 - Sair", True, WHITE)

    while True:
        screen.fill(BLACK)
        draw_gradient_background([(0, 0, 0), (50, 50, 100)])
        title_render = font_title.render(title_text, True, WHITE)
        title_x = (SCREEN_WIDTH - title_render.get_width()) // 2
        draw_3d_text(title_text, font_title, title_x, SCREEN_HEIGHT // 4, COLORS[0], 5)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(highscores_text, (SCREEN_WIDTH // 2 - highscores_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(difficulty_text, (SCREEN_WIDTH // 2 - difficulty_text.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 210))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jogar"
                if event.key == pygame.K_2:
                    return "recordes"
                if event.key == pygame.K_3:
                    return "dificuldade"
                if event.key == pygame.K_4:
                    return "sair"

# Função para selecionar a dificuldade
def select_difficulty():
    """
    Exibe a tela de seleção de dificuldade.
    Técnica de Computação Gráfica: Renderização de texto e botões.
    """
    font_title = pygame.font.Font(font_path, 24)
    font_options = pygame.font.Font(font_path, 24)
    title_text = "Selecione a Dificuldade"
    easy_text = font_options.render("1 - Fácil", True, WHITE)
    medium_text = font_options.render("2 - Médio", True, WHITE)
    hard_text = font_options.render("3 - Difícil", True, WHITE)
    back_text = font_title.render("ESC para voltar", True, WHITE)

    while True:
        screen.fill(BLACK)
        draw_gradient_background([(0, 0, 0), (50, 50, 100)])
        title_render = font_title.render(title_text, True, WHITE)
        title_x = (SCREEN_WIDTH - title_render.get_width()) // 2
        draw_3d_text(title_text, font_title, title_x, SCREEN_HEIGHT // 4, COLORS[0], 5)
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "fácil"
                if event.key == pygame.K_2:
                    return "médio"
                if event.key == pygame.K_3:
                    return "difícil"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

# Função para mostrar a tela de recordes
def show_highscores():
    """
    Exibe a tela de recordes.
    Técnica de Computação Gráfica: Renderização de texto e listagem de dados.
    """
    font_title = pygame.font.Font(font_path, 36)
    font_scores = pygame.font.Font(font_path, 20)
    title_text = "Recordes"
    back_text = font_scores.render("ESC para voltar", True, WHITE)

    highscores = load_highscores()
    scroll_offset = 0  # Offset para rolagem

    while True:
        screen.fill(BLACK)
        draw_gradient_background([(0, 0, 0), (50, 50, 100)])
        title_render = font_title.render(title_text, True, WHITE)
        title_x = (SCREEN_WIDTH - title_render.get_width()) // 2
        draw_3d_text(title_text, font_title, title_x, SCREEN_HEIGHT // 4, COLORS[0], 5)

        # Exibir recordes com rolagem
        y_offset = SCREEN_HEIGHT // 3 + scroll_offset
        for i, (name, score, elapsed_time) in enumerate(highscores):
            score_text = font_scores.render(f"{i + 1}. {name}: {score} (Tempo: {elapsed_time}s)", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 50

        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Rolar para cima
                    scroll_offset += 20
                elif event.button == 5:  # Rolar para baixo
                    scroll_offset -= 20

# Função para carregar os recordes
def load_highscores():
    """
    Carrega os recordes do arquivo.
    Técnica de Computação Gráfica: Manipulação de arquivos e dados.
    """
    try:
        with open("highscores.txt", "r") as file:
            highscores = []
            for line in file.readlines():
                parts = line.strip().split(": ")
                if len(parts) == 3:  # Formato novo: nome, pontuação, tempo
                    name, score, elapsed_time = parts
                    highscores.append((name, int(score), elapsed_time))
                elif len(parts) == 2:  # Formato antigo: nome, pontuação
                    name, score = parts
                    highscores.append((name, int(score), "0"))  # Tempo padrão para entradas antigas
            # Ordenar pela pontuação (maior primeiro)
            highscores.sort(key=lambda x: x[1], reverse=True)
            return highscores
    except FileNotFoundError:
        return []

# Função para salvar a pontuação
def save_score(name, score, elapsed_time):
    """
    Salva a pontuação e o tempo decorrido no arquivo de recordes.
    Técnica de Computação Gráfica: Manipulação de arquivos e dados.
    """
    highscores = load_highscores()
    highscores.append((name, score, elapsed_time))
    highscores.sort(key=lambda x: x[1], reverse=True)
    highscores = highscores[:10]  # Mantém apenas os 10 melhores
    with open("highscores.txt", "w") as file:
        for name, score, elapsed_time in highscores:
            file.write(f"{name}: {score}: {elapsed_time}\n")

# Função para pedir o nome do jogador
def get_player_name():
    """
    Solicita o nome do jogador após o Game Over.
    Técnica de Computação Gráfica: Renderização de caixa de texto.
    """
    font = pygame.font.Font(font_path, 24)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    color_inactive = WHITE
    color_active = COLORS[0]
    color = color_inactive
    active = False
    text = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        draw_gradient_background([(0, 0, 0), (50, 50, 100)])
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text

# Função principal do jogo
def main(difficulty="médio"):
    """
    Função principal do jogo.
    Técnica de Computação Gráfica: Integração de todas as técnicas.
    """
    clock = pygame.time.Clock()
    piece = random.choice(SHAPES)
    next_piece = random.choice(SHAPES)
    piece_x = GRID_WIDTH // 2 - len(piece[0]) // 2
    piece_y = 0
    piece_color = random.choice(COLORS)
    next_piece_color = random.choice(COLORS)
    score = 0
    lines_cleared = 0  # Contador de linhas concluídas
    fall_speed = 1 if difficulty == "fácil" else 2 if difficulty == "médio" else 3
    running = True
    paused = False
    start_time = time.time()  # Inicia o cronômetro

    while running:
        elapsed_time = int(time.time() - start_time)  # Calcula o tempo decorrido

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(piece, piece_x - 1, piece_y):
                        piece_x -= 1
                if event.key == pygame.K_RIGHT:
                    if not check_collision(piece, piece_x + 1, piece_y):
                        piece_x += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(piece, piece_x, piece_y + 1):
                        piece_y += 1
                if event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(piece)
                    if not check_collision(rotated_piece, piece_x, piece_y):
                        piece = rotated_piece
                if event.key == pygame.K_SPACE:
                    while not check_collision(piece, piece_x, piece_y + 1):
                        piece_y += 1
                if event.key == pygame.K_p:  # Pausar o jogo
                    paused = not paused

        if paused:
            font = pygame.font.Font(font_path, 24)
            pause_text = font.render("PAUSADO", True, WHITE)
            resume_text = font.render("P - Continuar", True, WHITE)
            quit_text = font.render("Q - Sair da Fase", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Continuar o jogo
                        paused = False
                    elif event.key == pygame.K_q:  # Sair da fase
                        return "menu"
            continue

        if not check_collision(piece, piece_x, piece_y + 1):
            piece_y += 1
        else:
            for row in range(len(piece)):
                for col in range(len(piece[row])):
                    if piece[row][col]:
                        grid[piece_y + row][piece_x + col] = COLORS.index(piece_color) + 1
                        draw_particles((piece_x + col) * BLOCK_SIZE, (piece_y + row) * BLOCK_SIZE, piece_color)
            lines_removed = remove_complete_lines()
            score += lines_removed * 100
            lines_cleared += lines_removed  # Atualiza o contador de linhas concluídas
            piece = next_piece
            piece_color = next_piece_color
            next_piece = random.choice(SHAPES)
            next_piece_color = random.choice(COLORS)
            piece_x = GRID_WIDTH // 2 - len(piece[0]) // 2
            piece_y = 0
            if check_collision(piece, piece_x, piece_y):
                running = False

        # Desenhar tudo
        draw_gradient_background([(0, 0, 0), (50, 50, 100)])
        draw_grid()
        draw_shadow(piece, piece_x, piece_y, piece_color)
        draw_piece(piece, piece_x, piece_y, piece_color)

        # Exibir pontuação, tempo, linhas concluídas e dificuldade
        font = pygame.font.Font(font_path, 20)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Tempo: {elapsed_time}s", True, WHITE)
        lines_text = font.render(f"Linhas: {lines_cleared}", True, WHITE)
        difficulty_text = font.render(f"{difficulty.capitalize()}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 250, 50))
        screen.blit(time_text, (SCREEN_WIDTH - 250, 100))
        screen.blit(lines_text, (SCREEN_WIDTH - 250, 150))
        screen.blit(difficulty_text, (SCREEN_WIDTH - 250, 200))

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(fall_speed + 2)

    # Salvar pontuação e tempo
    player_name = get_player_name()
    if player_name:
        save_score(player_name, score, elapsed_time)

    # Reiniciar a grade após o Game Over
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = 0

    return "menu"

# Loop principal do jogo
if __name__ == "__main__":
    difficulty = "médio"  # Dificuldade padrão
    while True:
        action = show_menu()
        if action == "jogar":
            result = main(difficulty)
            if result == "menu":
                continue
        elif action == "recordes":
            result = show_highscores()
            if result == "menu":
                continue
        elif action == "dificuldade":
            difficulty = select_difficulty()
            if difficulty == "menu":
                continue
        elif action == "sair":
            break