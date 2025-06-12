import matplotlib.pyplot as plt
import numpy as np

def flood_fill(px, py, matriz, dimensao):
    pilha = [(px, py)] 

    while pilha:
        px, py = pilha.pop()

        if 0 <= px < matriz.shape[1] and 0 <= py < matriz.shape[0] and np.array_equal(matriz[dimensao - py - 1, px], [1, 1, 1]):
            matriz[dimensao - py - 1, px] = [0, 255, 0]  

            # adição dos pontos vizinhos na pilha
            pilha.append((px + 1, py))
            pilha.append((px - 1, py))
            pilha.append((px, py + 1))
            pilha.append((px, py - 1))

    return matriz

def draw_forma(ax, ay, bx, by, matriz, dimensao):
    delta_x = abs(bx - ax)
    delta_y = abs(by - ay)
    passo_x = 1 if ax < bx else -1
    passo_y = 1 if ay < by else -1
    erro = delta_x - delta_y

    while True:
        matriz[int(dimensao - ay - 1), ax] = [0, 0, 0] 

        if ax == bx and ay == by:
            break

        ajuste = 2 * erro
        if ajuste > -delta_y:
            erro -= delta_y
            ax += passo_x
        if ajuste < delta_x:
            erro += delta_x
            ay += passo_y

    return matriz

# tamanho da grade de pixels
resolucao = 101

matriz_imagem = np.ones((resolucao, resolucao, 3))


draw_forma(20, 40, 10, 70, matriz_imagem, resolucao)
draw_forma(10, 70, 60, 90, matriz_imagem, resolucao)
draw_forma(60, 90, 80, 75, matriz_imagem, resolucao)
draw_forma(80, 75, 85, 45, matriz_imagem, resolucao)
draw_forma(85, 45, 50, 30, matriz_imagem, resolucao)
draw_forma(50, 30, 45, 60, matriz_imagem, resolucao)
draw_forma(45, 60, 65, 65, matriz_imagem, resolucao)
draw_forma(65, 65, 60, 45, matriz_imagem, resolucao)
draw_forma(60, 45, 20, 40, matriz_imagem, resolucao)

flood_fill(70, 50, matriz_imagem, resolucao)

plt.imshow(matriz_imagem, extent=[0, resolucao, 0, resolucao])
plt.show()
