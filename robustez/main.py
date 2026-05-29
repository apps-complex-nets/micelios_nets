from networkx.linalg import laplacianmatrix
from matplotlib._api import deprecation
from networkx import generators
from networkx.algorithms import non_randomness
from networkx.algorithms import coloring
from re import T
import networkx as nx
import constantes as c
import random
from ast import literal_eval
from math import dist
import matplotlib.pyplot as plt



def average_two_terminal_realiability(G):
    n_nodes = G.number_of_nodes()
    if n_nodes < 2:
        return 0.0

    total_pares = n_nodes * (n_nodes - 1) // 2
    caminos = 0
    for componente in nx.connected_components(G):
        k = len(componente)
        if k >= 2:
            caminos += k * (k - 1) // 2
    return caminos / total_pares
    

def numero_componentes_conectados(G):
    return nx.number_connected_components(G)

def orden_componente_mayor(G):
    componente = max(nx.connected_components(G), key=len)
    return len(componente)

def tamano_componente_mayor(G):
    componente = max(nx.connected_components(G), key=len)
    return len(G.subgraph(componente).edges)

def longitud_componente_mayor(G):
    componente = max(nx.connected_components(G), key=len)
    longitud = 0
    for edge in G.subgraph(componente).edges():
        p1 = literal_eval(edge[0])
        p2 = literal_eval(edge[1])

        # convertir a flotantes
        p1 = tuple(map(float, p1))
        p2 = tuple(map(float, p2))

        d = dist(p1, p2)
        #print(edge)
        #print(d)
        longitud += d
    return longitud

def atacar_edge_aleatoriamente(G):
    removed_edge = random.sample(list(G.edges()), 1)
    return removed_edge

def atacar_red_aleatoriamente(G):
    removed_node = random.sample(list(G.nodes()), 1)
    return removed_node

def atacar_red_por_grado(G):
    removed_node = max(G.degree(), key=lambda x: x[1])[0]
    return [removed_node]

def grafica_medidas_robustez(lista_medida, medida, titulo, ejex):
    plt.figure(figsize=(12, 6))
    plt.plot(lista_medida, marker="o", linestyle="-")
    plt.xlabel(ejex)
    plt.ylabel(medida)
    plt.title(titulo)
    plt.savefig(tipo_nodo + "/" + medida + "_" + titulo + ".png")
    plt.show()

tipo_nodo = "Enlace"

for muestra in range(1,6):
    for red in c.REDES_NEUROESPORA[muestra]:
        G = nx.read_gexf(c.PATH_NEUROESPORA + red + ".gexf")
        n = G.number_of_nodes()
        m = G.number_of_edges()
        print("**** Procesando red:", red, "con", str(n), "nodos y", str(m), "aristas.")
        G_copy = G.copy()
        order_lcc = [orden_componente_mayor(G_copy)]
        size_lcc = [tamano_componente_mayor(G_copy)]
        length_lcc = [longitud_componente_mayor(G_copy)]
        num_cc = [numero_componentes_conectados(G_copy)]
        a2tr_list = [average_two_terminal_realiability(G_copy)]
        if tipo_nodo == "Enlace":
            ejex = "Número de enlaces eliminados"

            for i in range(G.number_of_edges()-1):
                removed_enlace = atacar_edge_aleatoriamente(G_copy)
                G_copy.remove_edges_from(removed_enlace)
                print("Número de nodos: ", str(G_copy.number_of_nodes()))
                l = longitud_componente_mayor(G_copy)
                o = orden_componente_mayor(G_copy)
                t = tamano_componente_mayor(G_copy)
                nc = numero_componentes_conectados(G_copy)
                a2tr = average_two_terminal_realiability(G_copy)
                order_lcc.append(o)
                size_lcc.append(t)
                length_lcc.append(l)
                num_cc.append(nc)
                a2tr_list.append(a2tr)
                print("Longitud CC: ",str(l), "Orden CC: ",str(o), "Tamaño CC: ", str(t), "Numero de CC: ", str(nc), "A2TR: ", str(a2tr))
        else:
            ejex = "Número de nodos eliminados"
            for i in range(G.number_of_nodes()-1):
                if tipo_nodo == "Aleatorio":
                    removed_node = atacar_red_aleatoriamente(G_copy)
                else:
                    removed_node = atacar_red_por_grado(G_copy)
                
                G_copy.remove_nodes_from(removed_node)
                print("Número de nodos: ", str(G_copy.number_of_nodes()))
                l = longitud_componente_mayor(G_copy)
                o = orden_componente_mayor(G_copy)
                t = tamano_componente_mayor(G_copy)
                nc = numero_componentes_conectados(G_copy)
                a2tr = average_two_terminal_realiability(G_copy)
                order_lcc.append(o)
                size_lcc.append(t)
                length_lcc.append(l)
                num_cc.append(nc)
                a2tr_list.append(a2tr)
                print("Longitud CC: ",str(l), "Orden CC: ",str(o), "Tamaño CC: ", str(t), "Numero de CC: ", str(nc), "A2TR: ", str(a2tr))
            
        # grafica  orden del componente mayor
        grafica_medidas_robustez(order_lcc, "Orden del componente mayor", red + "_" + tipo_nodo, ejex)
        
        # grafica  tamaño del componente mayor
        grafica_medidas_robustez(size_lcc, "Tamaño del componente mayor", red + "_" + tipo_nodo, ejex)

        # grafica  longitud del componente mayor
        grafica_medidas_robustez(length_lcc, "Longitud del componente mayor", red + "_" + tipo_nodo, ejex)

        # grafica numero de componentes conectados
        grafica_medidas_robustez(num_cc, "Numero de componentes conectados", red + "_" + tipo_nodo, ejex)

        # grafica A2TR
        grafica_medidas_robustez(a2tr_list, "A2TR", red + "_" + tipo_nodo, ejex)
