"""Projeto ConectaUDF: análise de uma rede social por grafos não direcionados.

Autor: Lucas Yan Santana Caetano
Data: 16/10/2026
Execução: python conecta_udf.py
Dependências externas: nenhuma.
"""

from collections import deque


# Cada amizade é recíproca: se X é amigo de Y, Y é amigo de X.
REDE_ORIGINAL = {
    "Ana": ["Bruno", "Carla"],
    "Bruno": ["Ana", "Carla", "Diego"],
    "Carla": ["Ana", "Bruno", "Elisa"],
    "Diego": ["Bruno", "Elisa", "Felipe"],
    "Elisa": ["Carla", "Diego", "Felipe"],
    "Felipe": ["Diego", "Elisa"],
}

# Ampliação do desafio: quatro novos usuários e oito novas amizades.
NOVAS_AMIZADES = [
    ("Ana", "Gabriela"),
    ("Bruno", "Gabriela"),
    ("Bruno", "Henrique"),
    ("Diego", "Henrique"),
    ("Elisa", "Isabela"),
    ("Felipe", "Isabela"),
    ("Diego", "João"),
    ("Felipe", "João"),
]


def validar_rede(rede):
    """Verifica se o grafo é simples, não direcionado e coerente."""
    if not isinstance(rede, dict):
        raise ValueError("A rede deve ser um dicionário de listas.")
    for usuario, amigos in rede.items():
        if len(amigos) != len(set(amigos)):
            raise ValueError(f"Há amizades repetidas para {usuario}.")
        if usuario in amigos:
            raise ValueError(f"Um usuário não pode ser amigo de si mesmo: {usuario}.")
        for amigo in amigos:
            if amigo not in rede:
                raise ValueError(f"Usuário desconhecido: {amigo}.")
            if usuario not in rede[amigo]:
                raise ValueError(f"Amizade não recíproca: {usuario} e {amigo}.")


def graus(rede):
    """Retorna o número de amigos diretos de cada usuário."""
    validar_rede(rede)
    return {usuario: len(amigos) for usuario, amigos in rede.items()}


def total_arestas(rede):
    """Pelo lema do aperto de mãos, soma dos graus = 2 * arestas."""
    soma_graus = sum(graus(rede).values())
    return soma_graus // 2


def densidade(rede):
    """Densidade de um grafo simples não direcionado, entre 0 e 1."""
    n = len(rede)
    if n < 2:
        return 0.0
    return (2 * total_arestas(rede)) / (n * (n - 1))


def menor_caminho(rede, origem, destino):
    """Usa busca em largura (BFS) para achar um caminho com menos arestas."""
    validar_rede(rede)
    if origem not in rede or destino not in rede:
        raise ValueError("Origem ou destino não existe na rede.")
    fila = deque([[origem]])
    visitados = {origem}
    while fila:
        caminho = fila.popleft()
        atual = caminho[-1]
        if atual == destino:
            return caminho
        for vizinho in rede[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(caminho + [vizinho])
    return None


def ampliar_rede(rede, novos_usuarios, novas_amizades):
    """Cria uma cópia ampliada sem modificar a rede de origem."""
    ampliada = {usuario: list(amigos) for usuario, amigos in rede.items()}
    for usuario in novos_usuarios:
        if usuario in ampliada:
            raise ValueError(f"Usuário já existe: {usuario}.")
        ampliada[usuario] = []
    for usuario1, usuario2 in novas_amizades:
        if usuario1 not in ampliada or usuario2 not in ampliada:
            raise ValueError("Uma nova amizade contém um usuário não cadastrado.")
        if usuario1 == usuario2 or usuario2 in ampliada[usuario1]:
            raise ValueError("Nova amizade repetida ou ligação a si mesmo.")
        ampliada[usuario1].append(usuario2)
        ampliada[usuario2].append(usuario1)
    validar_rede(ampliada)
    return ampliada


def amigos_em_comum(rede, usuario1, usuario2):
    """Informa amigos em comum de dois usuários cadastrados."""
    validar_rede(rede)
    if usuario1 not in rede or usuario2 not in rede:
        raise ValueError("É necessário informar dois usuários cadastrados.")
    return sorted(set(rede[usuario1]) & set(rede[usuario2]))


def sugestoes_de_amizade(rede):
    """Indica pares ainda não conectados, priorizando amigos em comum."""
    validar_rede(rede)
    usuarios = list(rede)
    sugestoes = []
    for i, usuario1 in enumerate(usuarios):
        for usuario2 in usuarios[i + 1:]:
            if usuario2 not in rede[usuario1]:
                em_comum = amigos_em_comum(rede, usuario1, usuario2)
                if em_comum:
                    sugestoes.append((usuario1, usuario2, em_comum))
    return sorted(sugestoes, key=lambda item: (-len(item[2]), item[0], item[1]))


def exibir_rede(titulo, rede):
    print(f"\n{titulo}")
    print("-" * len(titulo))
    for usuario, amigos in rede.items():
        print(f"{usuario}: {', '.join(amigos)} | grau = {len(amigos)}")
    soma = sum(graus(rede).values())
    print(f"Total de usuários (vértices): {len(rede)}")
    print(f"Soma dos graus: {soma}")
    print(f"Total de amizades (arestas): {total_arestas(rede)}")
    print(f"Densidade decimal: {densidade(rede):.4f}")
    print(f"Densidade percentual: {densidade(rede):.2%}")
    maior_grau = max(graus(rede).values())
    destaque = [nome for nome, grau in graus(rede).items() if grau == maior_grau]
    print(f"Usuários com mais conexões ({maior_grau}): {', '.join(destaque)}")


def main():
    validar_rede(REDE_ORIGINAL)
    exibir_rede("REDE ORIGINAL", REDE_ORIGINAL)

    print("\nCAMINHO DE ANA ATÉ FELIPE")
    caminho = menor_caminho(REDE_ORIGINAL, "Ana", "Felipe")
    print("Caminho 1:", " -> ".join(caminho))
    print("Quantidade de arestas:", len(caminho) - 1)
    outro_caminho = ["Ana", "Carla", "Elisa", "Felipe"]
    assert all(b in REDE_ORIGINAL[a] for a, b in zip(outro_caminho, outro_caminho[1:]))
    print("Caminho 2:", " -> ".join(outro_caminho))
    print("Quantidade de arestas:", len(outro_caminho) - 1)

    rede_ampliada = ampliar_rede(
        REDE_ORIGINAL,
        ["Gabriela", "Henrique", "Isabela", "João"],
        NOVAS_AMIZADES,
    )
    exibir_rede("REDE AMPLIADA", rede_ampliada)
    print("\nCOMPARAÇÃO DA DENSIDADE")
    print(f"Antes: {densidade(REDE_ORIGINAL):.2%}")
    print(f"Depois: {densidade(rede_ampliada):.2%}")
    print(f"Variação: {(densidade(rede_ampliada) - densidade(REDE_ORIGINAL)) * 100:.2f} pontos percentuais")

    print("\nRECOMENDAÇÕES DE NOVAS AMIZADES")
    for usuario1, usuario2, amigos in sugestoes_de_amizade(rede_ampliada)[:5]:
        print(f"{usuario1} + {usuario2}: {len(amigos)} amigo(s) em comum: {', '.join(amigos)}")
    print("Observação: sugestões precisam respeitar privacidade e consentimento.")


if __name__ == "__main__":
    main()
