import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import tkinter as tk

def generer_etiq_sommets(n):
    etiqs = []
    i = 0
    while len(etiqs) < n:
        etiq = ''
        temp = i
        while temp >= 0:
            etiq = chr(temp % 26 + 65) + etiq
            temp = temp // 26 - 1
        etiqs.append(etiq)
        i += 1
    return etiqs

def generer_graphe_aleatoire(nb_sommets):
    G = nx.Graph()
    etiquettes = generer_etiq_sommets(nb_sommets)

    for etiquette in etiquettes:
        G.add_node(etiquette)

    for _ in range(nb_sommets * 2):
        u = random.choice(etiquettes)
        v = random.choice(etiquettes)
        if u != v:
            poids = random.randint(1, 100)
            G.add_edge(u, v, weight=poids)

    return G

def kruskal(graphe):
    arbre_couvrant = []
    edges = sorted(graphe.edges(data=True), key=lambda x: x[2]['weight'])
    union_find = {i: i for i in graphe.nodes}

    def find(u):
        if union_find[u] != u:
            union_find[u] = find(union_find[u])
        return union_find[u]

    def union(u, v):
        parent_u = find(u)
        parent_v = find(v)
        if parent_u != parent_v:
            union_find[parent_u] = parent_v

    for u, v, data in edges:
        if find(u) != find(v):
            arbre_couvrant.append((u, v, data['weight']))
            union(u, v)

    return arbre_couvrant

def afficher_graphe(graphe, arbre_couvrant):
    pos = nx.spring_layout(graphe)
    plt.figure(figsize=(8, 8))

    nx.draw(graphe, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=12, font_weight='bold')
    labels = nx.get_edge_attributes(graphe, 'weight')
    nx.draw_networkx_edge_labels(graphe, pos, edge_labels=labels)

    arbre_edges = [(u, v) for u, v, _ in arbre_couvrant]
    nx.draw_networkx_edges(graphe, pos, edgelist=arbre_edges, edge_color='red', width=0.75)

    plt.title("Arbre couvrant minimal (Kruskal)")
    plt.show()

def run_kruskal(entry, graph_frame, info_frame):
    try:
        nb_sommets = int(entry.get())
        if nb_sommets <= 0:
            raise ValueError
    except ValueError:
        print("Veuillez entrer un nombre valide de sommets.")
        return

    for widget in graph_frame.winfo_children():
        widget.destroy()
    for widget in info_frame.winfo_children():
        widget.destroy()

    start_time = time.time()

    graphe = generer_graphe_aleatoire(nb_sommets)
    arbre_couvrant = kruskal(graphe)
    cout_total = sum([poids for _, _, poids in arbre_couvrant])

    execution_time = time.time() - start_time

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    pos = nx.spring_layout(graphe)
    nx.draw(graphe, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold', ax=ax)
    labels = nx.get_edge_attributes(graphe, 'weight')
    nx.draw_networkx_edge_labels(graphe, pos, edge_labels=labels)

    arbre_edges = [(u, v) for u, v, _ in arbre_couvrant]
    nx.draw_networkx_edges(graphe, pos, edgelist=arbre_edges, edge_color='red', width=1, ax=ax)

    ax.set_title("Arbre couvrant minimal (Kruskal)", fontsize=14, fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=10)

    cout_label = tk.Label(info_frame,
                          text=f"Coût total des arêtes choisies : {cout_total}",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    cout_label.pack(pady=5)

    time_label = tk.Label(info_frame,
                          text=f"Temps d'exécution : {execution_time:.4f} secondes",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    time_label.pack(pady=5)