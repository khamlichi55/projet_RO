import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import tkinter as tk

def generate_random_graph(x):
    """Génère un graphe aléatoire avec x sommets."""
    G = nx.Graph()
    G.add_nodes_from(range(x))
    for i in range(x):
        for j in range(i + 1, x):
            if random.choice([True, False]):
                G.add_edge(i, j)
    return G

def welsh_powell_algorithm(G):
    """Applique l'algorithme de Welsh-Powell pour colorer le graphe."""
    sorted_nodes = sorted(G.nodes, key=lambda x: G.degree[x], reverse=True)
    color_map = {}
    current_color = 0
    for node in sorted_nodes:
        if node not in color_map:
            color_map[node] = current_color
            for neighbor in sorted_nodes:
                if neighbor not in color_map and not any((neighbor, adj) in G.edges() or (adj, neighbor) in G.edges() for adj in color_map if color_map[adj] == current_color):
                    color_map[neighbor] = current_color
            current_color += 1
    return color_map

def run_welsh_powel(entry, graph_frame, info_frame):
    """Exécute l'algorithme de Welsh-Powell et affiche le graphe."""
    try:
        x = int(entry.get())
        if x <= 0:
            raise ValueError
    except ValueError:
        print("Veuillez entrer un nombre valide de sommets.")
        return

    # Effacer le contenu précédent du graph_frame et info_frame
    for widget in graph_frame.winfo_children():
        widget.destroy()
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Mesurer le temps d'exécution
    start_time = time.time()

    # Générer le graphe aléatoire
    G = generate_random_graph(x)

    # Appliquer l'algorithme de Welsh-Powell
    colors = welsh_powell_algorithm(G)

    # Calculer le temps d'exécution
    execution_time = time.time() - start_time

    # Afficher le graphe dans la fenêtre Tkinter
    display_graph(graph_frame, G, colors)

    # Afficher les informations (nombre de couleurs et temps d'exécution)
    display_info(info_frame, execution_time, colors)

def display_graph(graph_frame, G, colors):
    """Affiche le graphe dans la fenêtre Tkinter."""
    fig = plt.figure(figsize=(6, 4))  # Taille du graphe
    ax = fig.add_subplot(111)

    # Dessiner le graphe
    pos = nx.spring_layout(G)  # Positionnement des nœuds
    nx.draw(G, pos, with_labels=True, node_color=[colors[node] for node in G.nodes()],
            node_size=500, font_size=12, font_weight='bold', edge_color='gray',
            cmap=plt.cm.rainbow, font_color='black', width=2, alpha=0.8, ax=ax)
    ax.set_title("Graphe Coloré avec l'Algorithme de Welsh-Powell", fontsize=14, fontweight='bold')

    # Intégrer le graphe dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=10)

def display_info(info_frame, execution_time, colors):
    """Affiche le nombre de couleurs utilisées et le temps d'exécution."""
    min_colors_used = max(colors.values()) + 1  # Nombre de couleurs utilisées

    # Afficher le nombre de couleurs utilisées
    colors_label = tk.Label(info_frame,
                            text=f"Nombre de couleurs utilisées : {min_colors_used}",
                            font=('Arial', 12),
                            bg='#f0f0f0',
                            fg='#008000')
    colors_label.pack(pady=5)

    # Afficher le temps d'exécution
    time_label = tk.Label(info_frame,
                          text=f"Temps d'exécution : {execution_time:.4f} secondes",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    time_label.pack(pady=5)