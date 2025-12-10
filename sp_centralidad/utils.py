import networkx as nx
import matplotlib.pyplot as plt
import heapq

def generar_arbol_regular_balanceado(k=3, altura=2):
    G = nx.Graph()
    node_id = 0
    edges = []
    niveles = [[node_id]]
    node_id += 1

    for _ in range(altura):
        nivel_actual = []
        for padre in niveles[-1]:
            hijos = [node_id + i for i in range(k)]
            edges.extend((padre, h) for h in hijos)
            nivel_actual.extend(hijos)
            node_id += k
        niveles.append(nivel_actual)
    G.add_edges_from(edges)
    return G

def dibujar_arbol(G, titulo,pos, node_labels):
    nx.draw(G, pos, node_size=600)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='white')
    plt.title(titulo)
    plt.show()

def etiquetado_por_centralidad(G, centralidad):
    if centralidad == 1:
        centralidad = nx.degree_centrality(G)
    elif centralidad == 2:
        centralidad = nx.closeness_centrality(G)
    elif centralidad == 3:
        centralidad = nx.harmonic_centrality(G)
    elif centralidad == 4:
        centralidad = nx.betweenness_centrality(G)
    elif centralidad == 5:
        centralidad = nx.load_centrality(G)
    elif centralidad == 6:
        centralidad = nx.eigenvector_centrality(G)
    elif centralidad == 7:
        centralidad = nx.katz_centrality(G)
    elif centralidad == 8:
        centralidad = nx.pagerank(G)
    elif centralidad == 9:
        centralidad = nx.subgraph_centrality(G)
    elif centralidad == 10:
        centralidad = nx.current_flow_closeness_centrality(G)
    elif centralidad == 11:
        centralidad = nx.current_flow_betweenness_centrality(G)
    elif centralidad == 12:
        centralidad = nx.information_centrality(G)
    elif centralidad == 13:
        centralidad = nx.communicability_betweenness_centrality(G)
    elif centralidad == 14:
        centralidad = nx.percolation_centrality(G)
    elif centralidad == 15:
        centralidad = nx.estrada_index(G)
    elif centralidad == 16:
        centralidad = nx.second_order_centrality(G)
    else:
        return None
    centralidad_ordenada = sorted(centralidad.items(), key=lambda item: item[1])
    #print(centralidad_ordenada)
    node_labels = {centralidad_ordenada[i][0]:i for i in range(len(centralidad_ordenada))}
    return node_labels

def prufer_sequence_from_tree(edges):
    """
    Obtiene la sucesión de Prüfer de un árbol dado.

    Parámetros:
      - edges: lista de tuplas (u, v) que representan las aristas de un árbol etiquetado.

    Retorna:
      - prufer_seq: lista que representa la sucesión de Prüfer del árbol.
    """
    # 1. Determinar el conjunto de nodos y el número total de vértices.
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    n = len(nodes)

    # 2. Crear la lista de adyacencia y calcular el grado de cada nodo.
    adj = {node: [] for node in nodes}
    degree = {node: 0 for node in nodes}

    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # 3. Inicializar un heap (min-heap) con todas las hojas (nodos con grado 1)
    heap = []
    for node in nodes:
        if degree[node] == 1:
            heapq.heappush(heap, node)

    prufer_seq = []

    # 4. Realizar n-2 iteraciones para construir la sucesión de Prüfer.
    for _ in range(n - 2):
        # a) Extraer la hoja de menor etiqueta.
        leaf = heapq.heappop(heap)

        # b) Su hoja tendrá un único vecino; se toma el primer (y único) de su lista de adyacencia.
        neighbor = adj[leaf][0]
        prufer_seq.append(neighbor)

        # c) Actualizar el grado del vecino, eliminando la conexión con la hoja.
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)

        # d) La hoja se elimina del árbol; (podríamos marcarla con grado 0).
        degree[leaf] = 0

        # e) Si el vecino ahora es una hoja (grado 1), se agrega al heap.
        if degree[neighbor] == 1:
            heapq.heappush(heap, neighbor)

    return prufer_seq

def muestra_secuencias(secuencias, etiquetas, tipo_hongo, centralidad):
    plt.figure(figsize=(12, 6))
    for i, seq in enumerate(secuencias):
        plt.plot(seq, label=etiquetas[i], marker="o", linestyle="-")
    plt.xlabel("Índice en la secuencia")
    plt.ylabel("Etiqueta del vértice")
    plt.title(tipo_hongo + " - Secuencias de Prüfer - " + centralidad)
    plt.legend()
    plt.grid()
    plt.show()