import networkx as nx
import math

PATH_NEUROESPORA = "redes/Neurospora_crassa/"
REDES_NEUROESPORA = {1:["Muestra1_M1N17h","Muestra1_M1N18h","Muestra1_M1N20h","Muestra1_M1N22h","Muestra1_M1N24h"],
    2:["Muestra2_M2N18h","Muestra2_M2N20h","Muestra2_M2N22h","Muestra2_M2N24h"],
    3:["Muestra3_M3N17h","Muestra3_M3N18h","Muestra3_M3N20h","Muestra3_M3N22h","Muestra3_M3N24h"],
    4:["Muestra4_M4N17h","Muestra4_M4N18h","Muestra4_M4N20h","Muestra4_M4N22h","Muestra4_M4N24h"],
    5:["Muestra5_M5N18h","Muestra5_M5N20h","Muestra5_M5N22h","Muestra5_M5N24h"]
}

PATH_TRICHODERMA = "redes/Trichoderma_atroviride/"
REDES_TRICHODERMA = {1:["Muestra1_M1T24h","Muestra1_M1T26h","Muestra1_M1T28h","Muestra1_M1T30h","Muestra1_M1T32h"],
    2:["Muestra2_M2T24h","Muestra2_M2T26h","Muestra2_M2T28h","Muestra2_M2T30h","Muestra2_M2T32h"],
    3:["Muestra3_M3T26h","Muestra3_M3T28h","Muestra3_M3T30h","Muestra3_M3T32h","Muestra3_M3T34h","Muestra3_M3T36h"],
    4:["Muestra4_M4T26h","Muestra4_M4T28h","Muestra4_M4T30h","Muestra4_M4T32h","Muestra4_M4T34h","Muestra4_M4T36h"],
    5:["Muestra5_M5T26h","Muestra5_M5T28h","Muestra5_M5T30h","Muestra5_M5T32h","Muestra5_M5T36h"]
}

path_miscelio = PATH_NEUROESPORA
redes_miscelio = REDES_NEUROESPORA

for muestra in range(1,6):
    prufer_seq = list()
    for red in redes_miscelio[muestra]:
        net_file = path_miscelio + red + ".gexf"
        G = nx.read_gexf(net_file)
        print("**** Procesando red:", red, "con", G.number_of_nodes(), "nodos y", G.number_of_edges(), "aristas.")
        print("Es árbol: ", nx.is_tree(G))
        for u, v in G.edges():
            # Obtener coordenadas de ambos nodos
            x1 = float(G.nodes[u].get("x"))
            y1 = float(G.nodes[u].get("y"))
            x2 = float(G.nodes[v].get("x"))
            y2 = float(G.nodes[v].get("y"))
            
            # Distancia euclidiana
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            # Agregarla como peso
            G.edges[u, v]["weight"] = dist

        # --- 3. Guardar nuevo archivo ---
        nx.write_gexf(G, net_file)