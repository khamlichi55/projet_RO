import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import tkinter as tk
from tkinter import messagebox

def generer_graphe_oriente(n, pourcentage_liaisons=0.3):
    """Génère un graphe orienté aléatoire avec des distances aléatoires."""
    G = nx.DiGraph()
    sommets = [f"x{i}" for i in range(n)]

    for sommet in sommets:
        G.add_node(sommet)

    for i in range(n):
        for j in range(n):
            if i != j and random.random() < pourcentage_liaisons:
                distance = random.randint(1, 100)
                G.add_edge(sommets[i], sommets[j], weight=distance)

    return G

def run_bellman_ford(entry_n, entry_pourcentage, entry_depart, entry_arrivee, graph_frame, info_frame):
    """Exécute l'algorithme de Bellman-Ford et affiche le graphe."""
    try:
        n = int(entry_n.get())
        pourcentage_liaisons = float(entry_pourcentage.get())
        sommet_depart = entry_depart.get()
        sommet_arrivee = entry_arrivee.get()

        if n <= 0 or pourcentage_liaisons < 0 or pourcentage_liaisons > 1:
            raise ValueError("Valeurs invalides.")
    except ValueError as e:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
        return

    for widget in graph_frame.winfo_children():
        widget.destroy()
    for widget in info_frame.winfo_children():
        widget.destroy()

    start_time = time.time()

    G = generer_graphe_oriente(n, pourcentage_liaisons)

    try:
        chemin, distance_totale = appliquer_bellman_ford(G, sommet_depart, sommet_arrivee)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    execution_time = time.time() - start_time

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    pos = nx.spring_layout(G)
    edges = G.edges(data=True)
    edge_colors = ['red' if (u, v) in zip(chemin, chemin[1:]) else 'black' for u, v, d in edges]
    node_colors = ['green' if node in chemin else 'lightblue' for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=10, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in edges})

    ax.set_title("Chemin le plus court (Bellman-Ford)", fontsize=14, fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=10)

    chemin_label = tk.Label(info_frame,
                            text=f"Chemin le plus court : {' -> '.join(chemin)}",
                            font=('Arial', 12),
                            bg='#f0f0f0',
                            fg='#008000')
    chemin_label.pack(pady=5)

    distance_label = tk.Label(info_frame,
                              text=f"Distance totale : {distance_totale}",
                              font=('Arial', 12),
                              bg='#f0f0f0',
                              fg='#008000')
    distance_label.pack(pady=5)

    time_label = tk.Label(info_frame,
                          text=f"Temps d'exécution : {execution_time:.4f} secondes",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    time_label.pack(pady=5)

def appliquer_bellman_ford(G, sommet_depart, sommet_arrivee):
    """Applique l'algorithme de Bellman-Ford et retourne le chemin et la distance."""
    try:
        distances, chemins = nx.single_source_bellman_ford(G, sommet_depart, weight='weight')
        chemin = chemins[sommet_arrivee]
        distance_totale = distances[sommet_arrivee]
        return chemin, distance_totale
    except nx.NetworkXNoPath:
        raise ValueError(f"Aucun chemin entre {sommet_depart} et {sommet_arrivee}.")
    except nx.NetworkXUnbounded:
        raise ValueError(f"Le graphe contient un cycle négatif accessible depuis {sommet_depart}.")