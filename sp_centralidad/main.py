import networkx as nx
import constantes as c
import utils

for muestra in range(1,6):
    prufer_seq = list()
    for red in c.REDES_NEUROESPORA[muestra]:
        G = nx.read_gexf(c.PATH_NEUROESPORA + red + ".gexf")
        print("**** Procesando red:", red, "con", G.number_of_nodes(), "nodos y", G.number_of_edges(), "aristas.")
        print("Es árbol: ", nx.is_tree(G))
        if not nx.is_tree(G):
            T = nx.minimum_spanning_tree(G)
            node_labels = utils.etiquetado_por_centralidad(G, c.CENTRALIDAD)
            H=T.copy()
        else:
            node_labels = utils.etiquetado_por_centralidad(G, c.CENTRALIDAD)
            H=G.copy()
        if node_labels != None:
            G_relabelled = nx.relabel_nodes(H, node_labels, copy=True)
        else:
            print("No genero etiquetas")
        ps = utils.prufer_sequence_from_tree(G_relabelled.edges())
        pos = {n:(G.nodes[n]['x'],G.nodes[n]['y']) for n in G.nodes()}
        #dibujar_arbol(G, red,pos, node_labels)
        #print("Secuencia de Prüfer:", ps)
        prufer_seq.append(ps)
    utils.muestra_secuencias(prufer_seq, c.REDES_NEUROESPORA[muestra], c.TIPO_HONGO, c.TIPOS_CENTRALIDADES[c.CENTRALIDAD])
