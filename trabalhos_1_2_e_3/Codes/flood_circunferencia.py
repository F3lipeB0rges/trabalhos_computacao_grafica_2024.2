import matplotlib.pyplot as plt
import numpy as np

def flood_fill(px, py, matriz, dim):
    pilha = [(px, py)]  # pilha de pontos
    
    while pilha:
        px, py = pilha.pop()
        
        if 0 <= px < matriz.shape[1] and 0 <= py < matriz.shape[0] and np.array_equal(matriz[dim - py - 1, px], [1, 1, 1]):
            matriz[dim - py - 1, px] = [255, 0, 0] 
            
            # adição dos vizinhos na pilha
            pilha.append((px + 1, py))
            pilha.append((px - 1, py))
            pilha.append((px, py + 1))
            pilha.append((px, py - 1))
    
    return matriz

def draw_circulo(cx, cy, raio, matriz, dim):
    x = 0
    y = raio
    erro = 1 - raio
    
    while x <= y:
        matriz[int(dim - (cy + y) - 1), int(cx + x)] = [0, 0, 0]  
        matriz[int(dim - (cy + x) - 1), int(cx + y)] = [0, 0, 0]  
        matriz[int(dim - (cy - x) - 1), int(cx + y)] = [0, 0, 0]  
        matriz[int(dim - (cy - y) - 1), int(cx + x)] = [0, 0, 0]  
        matriz[int(dim - (cy - y) - 1), int(cx - x)] = [0, 0, 0]
        matriz[int(dim - (cy - x) - 1), int(cx - y)] = [0, 0, 0]  
        matriz[int(dim - (cy + x) - 1), int(cx - y)] = [0, 0, 0]  
        matriz[int(dim - (cy + y) - 1), int(cx - x)] = [0, 0, 0]  
        
        if erro < 0:
            erro += 2 * x + 3
        else:
            erro += 2 * (x - y) + 5
            y -= 1
        
        x += 1
    
    return matriz

# tamanho da grade de pixels
resolucao = 200

canvas = np.ones((resolucao, resolucao, 3))

draw_circulo(100, 100, 75, canvas, resolucao)

flood_fill(100, 100, canvas, resolucao)

plt.imshow(canvas, extent=[0, resolucao, 0, resolucao])
plt.show()
