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


def buscar(raiz, alvo):
    atual = raiz
    caminho = []

    while atual is not None:
        caminho.append(atual.valor)

        if alvo == atual.valor:
            return atual, caminho

        if alvo < atual.valor:
            atual = atual.esquerda
        else:
            atual = atual.direita

    return None, caminho


valores = [50, 30, 70, 20, 40, 60, 80]

raiz = None

for valor in valores:
    raiz = inserir(raiz, valor)

alvo = 60
resultado, caminho = buscar(raiz, alvo)

print("Valor procurado:", alvo)
print("Caminho percorrido:", caminho)

if resultado is not None:
    print("Resultado: valor encontrado!")
else:
    print("Resultado: valor não encontrado.")
