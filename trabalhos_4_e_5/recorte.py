import matplotlib.pyplot as plt

# função para verificar se um ponto está dentro da janela
def inside(p, borda):
    x, y = p
    borda_type, borda_value = borda
    if borda_type == "left":
        return x >= borda_value
    elif borda_type == "right":
        return x <= borda_value
    elif borda_type == "bottom":
        return y >= borda_value
    elif borda_type == "top":
        return y <= borda_value
    return False

# função para calcular a interseção de um segmento com a borda
def intersecao(p1, p2, borda):
    x1, y1 = p1
    x2, y2 = p2
    borda_type, borda_value = borda

    if borda_type in ["left", "right"]:
        x = borda_value
        y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    else:
        y = borda_value
        x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)

    return (x, y)

# algoritmo de Sutherland-Hodgman
def sutherland_hodgman_clip(poligono, clip_janela):
    clipped_poligono = poligono

    # 2. Para cada lado, observa-se a relação entre vértices sucessivos e as janelas (limites)
    # percorre os lados do polígono e compara cada vértice com as bordas da janela de recorte
    for borda in clip_janela:
        new_poligono = []
        for i in range(len(clipped_poligono)):
            current_point = clipped_poligono[i]
            prev_point = clipped_poligono[i - 1]

            current_inside = inside(current_point, borda)
            prev_inside = inside(prev_point, borda)

            if prev_inside and current_inside:
                new_poligono.append(current_point) # CASO 1: Um dos dois vértices é adicionado à lista de saídas (p)
            elif prev_inside and not current_inside:
                new_poligono.append(intersecao(prev_point, current_point, borda)) # CASO 2: O ponto “i” de interseção é tratado como um vértice de saída
            elif not prev_inside and current_inside:
                new_poligono.append(intersecao(prev_point, current_point, borda))
                new_poligono.append(current_point) # CASO 4: Os dois pontos “i” e “p” são colocados na lista de vértices de saída

        # 3. Lados definidos pelos vértices da lista de saídas serão apresentados na tela
        clipped_poligono = new_poligono

    return clipped_poligono

# 1. Suponha um polígono de lados dados por vértices: v1, v2,..., vn
# define os polígonos
poligonos = {
    "Retângulo": [(-1, 2), (1, 2), (1, 0.5), (0.5, 0.5), (0.5, 1.25), (-0.5, 1.25), (-0.5, 0.5), (-1, 0.5)],
    "Triangular Inclinado": [(-0.5, 2), (1.5, -0.5), (-0.5, -0.5)],
    "Cruz": [(-0.5, 0), (0.5, 0), (0.5, -0.5), (1, -0.5), (1, -1.5), (0.5, -1.5), (0.5, -2), (-0.5, -2), (-0.5, -1.5), (-1, -1.5), (-1, -0.5), (-0.5, -0.5)],
    "Pentágono": [(-1.5, -0.5), (-2, 0.5), (-1, 1.5), (0, 0.5), (-0.5, -0.5)]
}

# define da janela de recorte
clip_janela = [("left", -1), ("right", 1), ("bottom", -1), ("top", 1)]

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()   

for ax in axes:
    ax.set_facecolor('#f0f0f0')

for ax, (name, poligono) in zip(axes, poligonos.items()):
    # aplica o recorte
    clipped_poligono = sutherland_hodgman_clip(poligono, clip_janela)
    
    # exibe os novos pontos após o recorte
    print(f"\nPolígono {name}")
    for i, point in enumerate(clipped_poligono):
        print(f"Ponto {i}: {point}")

    # janela de recorte
    janela_x = [-1, 1, 1, -1, -1]
    janela_y = [-1, -1, 1, 1, -1]
    ax.plot(janela_x, janela_y, 'r', label="Janela de Recorte")

    poligono_x, poligono_y = zip(*poligono + [poligono[0]])
    ax.fill(poligono_x, poligono_y, color='#FFC300', label="Polígono Original")

    if clipped_poligono:
        clipped_x, clipped_y = zip(*clipped_poligono + [clipped_poligono[0]])
        ax.fill(clipped_x, clipped_y, color='#2C041C', label="Polígono Recortado")
        
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title(name)
    ax.legend()
    ax.grid(True)

plt.tight_layout()
fig.patch.set_facecolor('#f0f0f0')
plt.show()