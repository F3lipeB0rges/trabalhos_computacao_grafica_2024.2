import matplotlib.pyplot as plt
import numpy as np

def flood_fill(x_inicial, y_inicial, matriz, dim):
    pilha = [(x_inicial, y_inicial)]  

    while pilha:
        x_atual, y_atual = pilha.pop()
        
        if 0 <= x_atual < matriz.shape[1] and 0 <= y_atual < matriz.shape[0] and np.array_equal(matriz[dim - y_atual - 1, x_atual], [1, 1, 1]):
            matriz[dim - y_atual - 1, x_atual] = [0, 0, 255]
            
            # adição dos pontos vizinhos na pilha
            pilha.append((x_atual + 1, y_atual))
            pilha.append((x_atual - 1, y_atual))
            pilha.append((x_atual, y_atual + 1))
            pilha.append((x_atual, y_atual - 1))
    
    return matriz

def draw_retangulo(x_inicio, y_inicio, x_fim, y_fim, matriz, dim):
    dist_x = abs(x_fim - x_inicio)
    dist_y = abs(y_fim - y_inicio)
    passo_x = 1 if x_inicio < x_fim else -1
    passo_y = 1 if y_inicio < y_fim else -1
    erro = dist_x - dist_y
    
    # loop
    while True:
        matriz[int(dim - y_inicio - 1), x_inicio] = [0, 0, 0]  
        
        if x_inicio == x_fim and y_inicio == y_fim:
            break
        
        erro_duplo = 2 * erro
        if erro_duplo > -dist_y:
            erro -= dist_y
            x_inicio += passo_x
        if erro_duplo < dist_x:
            erro += dist_x
            y_inicio += passo_y
    
    return matriz

# tamanho da grade de pixels
resolucao = 101

matriz_img = np.ones((resolucao, resolucao, 3))

draw_retangulo(10, 10, 10, 80, matriz_img, resolucao)
draw_retangulo(10, 80, 80, 80, matriz_img, resolucao)
draw_retangulo(80, 80, 80, 10, matriz_img, resolucao)
draw_retangulo(80, 10, 10, 10, matriz_img, resolucao)


flood_fill(50, 50, matriz_img, resolucao)


plt.imshow(matriz_img, extent=[0, resolucao, 0, resolucao])
plt.show()
