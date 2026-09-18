class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


def inserir(raiz, valor):
    if raiz is None:
        return No(valor)

    if valor < raiz.valor:
        raiz.esquerda = inserir(raiz.esquerda, valor)
    elif valor > raiz.valor:
        raiz.direita = inserir(raiz.direita, valor)

    return raiz


def buscar_caminho(raiz, alvo):
    atual = raiz
    caminho = []

    while atual is not None:
        caminho.append(atual.valor)

        if alvo == atual.valor:
            return True, caminho

        if alvo < atual.valor:
            atual = atual.esquerda
        else:
            atual = atual.direita

    return False, caminho


# Exemplo usado no Mini GDD inspirado no jogo Tree Delivery
valores = [50, 30, 70, 20, 40, 60, 80]
raiz = None

for valor in valores:
    raiz = inserir(raiz, valor)

# O jogador precisa entregar um pacote no nó 60
alvo = 60
encontrado, caminho = buscar_caminho(raiz, alvo)

print("Destino do pacote:", alvo)
print("Caminho percorrido:", " -> ".join(map(str, caminho)))

if encontrado:
    print("Entrega concluída no nó correto!")
else:
    print("Destino não encontrado na árvore.")
