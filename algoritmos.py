"""Implementações didáticas dos algoritmos usados na atividade."""

from __future__ import annotations


def dijkstra(nos: list[str], arestas: list[dict], origem: str, destino: str):
    """Retorna caminho, custo acumulado e predecessores em um grafo sem peso negativo."""
    adjacencia = {no: [] for no in nos}
    for aresta in arestas:
        u, v, peso = aresta["origem"], aresta["destino"], float(aresta["peso"])
        if peso < 0:
            raise ValueError("Dijkstra exige pesos não negativos.")
        adjacencia[u].append((v, peso))
        adjacencia[v].append((u, peso))

    distancias = {no: float("inf") for no in nos}
    anteriores = {no: None for no in nos}
    nao_visitados = set(nos)
    distancias[origem] = 0.0

    while nao_visitados:
        atual = min(nao_visitados, key=lambda no: distancias[no])
        if distancias[atual] == float("inf"):
            break
        nao_visitados.remove(atual)
        if atual == destino:
            break
        for vizinho, peso in adjacencia[atual]:
            if vizinho in nao_visitados:
                alternativa = distancias[atual] + peso
                if alternativa < distancias[vizinho]:
                    distancias[vizinho] = alternativa
                    anteriores[vizinho] = atual

    if distancias[destino] == float("inf"):
        return [], float("inf"), anteriores

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.reverse()
    return caminho, distancias[destino], anteriores


def prim(nos: list[str], arestas: list[dict], inicio: str):
    """Retorna a árvore geradora mínima alcançável a partir do vértice inicial."""
    adjacencia = {no: [] for no in nos}
    for aresta in arestas:
        u, v, peso = aresta["origem"], aresta["destino"], float(aresta["peso"])
        adjacencia[u].append((v, peso))
        adjacencia[v].append((u, peso))

    visitados = {inicio}
    selecionadas = []
    custo_total = 0.0
    while len(visitados) < len(nos):
        melhor = None
        for u in visitados:
            for v, peso in adjacencia[u]:
                if v not in visitados and (melhor is None or peso < melhor["peso"]):
                    melhor = {"origem": u, "destino": v, "peso": peso}
        if melhor is None:
            break
        selecionadas.append(melhor)
        visitados.add(melhor["destino"])
        custo_total += melhor["peso"]

    componentes = len(nos) - len(visitados) + 1
    return selecionadas, custo_total, componentes


def kruskal(nos: list[str], arestas: list[dict]):
    """Retorna as arestas da árvore geradora mínima em ordem de inclusão."""
    pai = {no: no for no in nos}
    altura = {no: 0 for no in nos}

    def encontrar(no: str) -> str:
        if pai[no] != no:
            pai[no] = encontrar(pai[no])
        return pai[no]

    def unir(a: str, b: str) -> bool:
        raiz_a, raiz_b = encontrar(a), encontrar(b)
        if raiz_a == raiz_b:
            return False
        if altura[raiz_a] < altura[raiz_b]:
            pai[raiz_a] = raiz_b
        elif altura[raiz_a] > altura[raiz_b]:
            pai[raiz_b] = raiz_a
        else:
            pai[raiz_b] = raiz_a
            altura[raiz_a] += 1
        return True

    selecionadas = []
    custo_total = 0.0
    for aresta in sorted(arestas, key=lambda item: float(item["peso"])):
        if unir(aresta["origem"], aresta["destino"]):
            selecionadas.append(aresta)
            custo_total += float(aresta["peso"])
            if len(selecionadas) == len(nos) - 1:
                break
    return selecionadas, custo_total
