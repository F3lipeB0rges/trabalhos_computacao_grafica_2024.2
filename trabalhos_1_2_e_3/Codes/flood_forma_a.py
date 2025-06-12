import matplotlib.pyplot as plt
import numpy as np

def flood_fill(px, py, matriz, dim):
    pilha = [(px, py)]  # pilha de pontos
    
    while pilha:
        px, py = pilha.pop()
        
        if 0 <= px < matriz.shape[1] and 0 <= py < matriz.shape[0] and np.array_equal(matriz[dim - py - 1, px], [1, 1, 1]):
            matriz[dim - py - 1, px] = [0, 255, 0] 
            
            # adição dos vizinhos na pilha
            pilha.append((px + 1, py))
            pilha.append((px - 1, py))
            pilha.append((px, py + 1))
            pilha.append((px, py - 1))
    
    return matriz

def draw_forma(x_ini, y_ini, x_fim, y_fim, matriz, dim):
    delta_x = abs(x_fim - x_ini)
    delta_y = abs(y_fim - y_ini)
    passo_x = 1 if x_ini < x_fim else -1
    passo_y = 1 if y_ini < y_fim else -1
    erro = delta_x - delta_y
    
    while True:
        matriz[int(dim - y_ini - 1), x_ini] = [0, 0, 0]
        
        if x_ini == x_fim and y_ini == y_fim:
            break
        
        erro_duplo = 2 * erro
        if erro_duplo > -delta_y:
            erro -= delta_y
            x_ini += passo_x
        if erro_duplo < delta_x:
            erro += delta_x
            y_ini += passo_y
    
    return matriz

# tamanho da grade de pixels
resolucao = 101

canvas = np.ones((resolucao, resolucao, 3))

draw_forma(0, 60, 50, 90, canvas, resolucao)
draw_forma(50, 90, 100, 50, canvas, resolucao)
draw_forma(100, 50, 90, 35, canvas, resolucao)
draw_forma(90, 35, 20, 20, canvas, resolucao)
draw_forma(20, 20, 40, 45, canvas, resolucao)
draw_forma(40, 45, 0, 60, canvas, resolucao)

flood_fill(50, 50, canvas, resolucao)

plt.imshow(canvas, extent=[0, resolucao, 0, resolucao])
plt.show()
