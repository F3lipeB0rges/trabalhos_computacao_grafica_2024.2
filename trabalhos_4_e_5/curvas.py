import numpy as np
import matplotlib.pyplot as plt
import scipy.special  

# calcula os polinômios de Bernstein
def bernstein(n, i, t):
    return scipy.special.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

# subdivide os pontos de controle igual ao slide
def subdivisao_curva(pontos):
    M01 = (pontos[0] + pontos[1]) / 2
    M12 = (pontos[1] + pontos[2]) / 2
    M23 = (pontos[2] + pontos[3]) / 2

    M012 = (M01 + M12) / 2
    M123 = (M12 + M23) / 2

    M0123 = (M012 + M123) / 2

    primeira_metade = [pontos[0], M01, M012, M0123]
    segunda_metade = [M0123, M123, M23, pontos[3]]

    return primeira_metade, segunda_metade, M0123

# calcula a curva de Bézier pela equação paramétrica
def parametrica(pontos, num_pontos=100):
    n = len(pontos) - 1
    t_values = np.linspace(0, 1, num_pontos) # array de valores (t) equidistantes entre 0 e 1, e define quantos valores de (t) serão gerados
    curva = np.zeros((num_pontos, 2)) # inicia com zeros e preenche com os valores da curva

    for i in range(n + 1):
        curva += np.outer(bernstein(n, i, t_values), pontos[i])

    return curva

# calcula a curva de Bézier pelo algoritmo de Casteljau
def casteljau(pontos, u=0.005):
    pontos_curva = []
    
    def subdivisao_recursiva(ctrl_pontos):
        p0, p3 = ctrl_pontos[0], ctrl_pontos[-1]
        dist = np.linalg.norm(p3 - p0)

        if dist > u:
            primeira_metade, segunda_metade, midpoint = subdivisao_curva(ctrl_pontos)
            
            subdivisao_recursiva(primeira_metade)
            subdivisao_recursiva(segunda_metade)
        else:
            pontos_curva.append(ctrl_pontos[-1])

    subdivisao_recursiva(pontos)
    return np.array(pontos_curva)

pontos_controle = np.array([[0, 0], [1, 3], [3, 3], [4, 0]])
pontos_controle_2 = np.array([[0, 0], [1, 3], [3, 3], [4, 0]])

# gera as curvas
curva_parametrica = parametrica(pontos_controle)
curva_casteljau = casteljau(pontos_controle_2)

plt.figure(figsize=(8, 6))

plt.plot(curva_parametrica[:, 0], curva_parametrica[:, 1], label="Bézier Paramétrica", linestyle="--", color="#2C041C", linewidth=2)

plt.plot(curva_casteljau[:, 0], curva_casteljau[:, 1], label="Bézier Casteljau", linestyle="-", color="#FFC300", linewidth=1) 

plt.plot(pontos_controle[:, 0], pontos_controle[:, 1], "ro-", label="Pontos de Controle")

plt.legend()
plt.title("Curvas de Bézier - Equação Paramétrica vs Casteljau")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid()
plt.show()