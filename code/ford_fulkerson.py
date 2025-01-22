import random
from collections import deque
import networkx as nx
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def generer_graphe_aleatoire(nb_sommets, capacite_max=10):
    """
    Génère un graphe orienté aléatoire avec des capacités.
    """
    sommets = [chr(65 + i) for i in range(nb_sommets)]  # Utiliser des lettres comme noms de sommets
    graphe = {sommet: {} for sommet in sommets}
    for u in sommets:
        for v in sommets:
            if u != v and random.random() > 0.5:  # Décider aléatoirement s'il y a un arc
                capacite = random.randint(1, capacite_max)
                graphe[u][v] = capacite
    return graphe

def bfs_trouver_chemin(graphe, source, puits, parent):
    """
    Recherche en largeur pour trouver un chemin avec capacité disponible.
    """
    visites = set()
    file = deque([source])
    visites.add(source)

    while file:
        courant = file.popleft()
        for voisin, capacite in graphe[courant].items():
            if voisin not in visites and capacite > 0:  # Vérifier la capacité disponible
                file.append(voisin)
                visites.add(voisin)
                parent[voisin] = courant
                if voisin == puits:
                    return True
    return False

def ford_fulkerson(graphe, source, puits):
    """
    Implémente l'algorithme de Ford-Fulkerson pour trouver le flot maximum.
    """
    graphe_residuel = {u: v.copy() for u, v in graphe.items()}  # Capacités résiduelles
    parent = {}  # Pour stocker le chemin
    flot_max = 0

    while bfs_trouver_chemin(graphe_residuel, source, puits, parent):
        # Trouver la capacité du goulot d'étranglement
        flot_chemin = float('Inf')
        s = puits
        while s != source:
            flot_chemin = min(flot_chemin, graphe_residuel[parent[s]][s])
            s = parent[s]

        # Mettre à jour les capacités résiduelles
        v = puits
        while v != source:
            u = parent[v]
            graphe_residuel[u][v] -= flot_chemin
            if v not in graphe_residuel:
                graphe_residuel[v] = {}
            graphe_residuel[v][u] = graphe_residuel[v].get(u, 0) + flot_chemin
            v = parent[v]

        flot_max += flot_chemin

    return flot_max, graphe_residuel

def calculer_flots(graphe, graphe_residuel, source, puits):
    """
    Calcule le flot total sortant du source et entrant dans le puits.
    """
    flot_sortant = sum(graphe[source][v] - graphe_residuel[source].get(v, 0) for v in graphe[source])
    flot_entrant = sum(graphe[u][puits] - graphe_residuel[u].get(puits, 0) for u in graphe if puits in graphe[u])
    return flot_sortant, flot_entrant

def trouver_coupe_min(graphe, graphe_residuel, source):
    """
    Trouve la coupe minimale en utilisant BFS sur le graphe résiduel.
    """
    visites = set()
    file = deque([source])
    visites.add(source)

    while file:
        courant = file.popleft()
        for voisin, capacite in graphe_residuel[courant].items():
            if voisin not in visites and capacite > 0:  # Vérifier la capacité disponible
                file.append(voisin)
                visites.add(voisin)

    arêtes_coupe_min = []
    for u in visites:
        for v in graphe[u]:
            if v not in visites:
                arêtes_coupe_min.append((u, v))

    return visites, arêtes_coupe_min

def afficher_graphe_en_table(graphe):
    """
    Affiche le graphe sous forme de tableau.
    """
    table = []
    for u in graphe:
        for v, capacite in graphe[u].items():
            table.append([u, v, capacite])
    return tabulate(table, headers=["De", "Vers", "Capacité"], tablefmt="grid")

def run_ford_fulkerson(entry_n, entry_source, entry_sink, graph_frame, info_frame):
    try:
        nb_sommets = int(entry_n.get())
        source = chr(65 + int(entry_source.get()))  # Convertir en lettre
        puits = chr(65 + int(entry_sink.get()))    # Convertir en lettre

        if source == puits:
            messagebox.showerror("Erreur", "La source et le puits doivent être différents.")
            return

        # Générer un graphe aléatoire
        graphe = generer_graphe_aleatoire(nb_sommets)

        # Appliquer l'algorithme de Ford-Fulkerson
        flot_max, graphe_residuel = ford_fulkerson(graphe, source, puits)

        # Calculer les flots
        flot_sortant, flot_entrant = calculer_flots(graphe, graphe_residuel, source, puits)

        # Trouver la coupe minimale
        coupe_min = trouver_coupe_min(graphe, graphe_residuel, source)

        # Créer un Notebook pour les onglets
        notebook = ttk.Notebook(graph_frame)
        notebook.pack(expand=True, fill='both')

        # Onglet 1 : Graphe
        graphe_tab = ttk.Frame(notebook)
        notebook.add(graphe_tab, text="Graphe")

        # Ajouter une barre de défilement à l'onglet Graphe
        canvas_graphe = tk.Canvas(graphe_tab)
        scrollbar_graphe = ttk.Scrollbar(graphe_tab, orient="vertical", command=canvas_graphe.yview)
        scrollable_frame_graphe = ttk.Frame(canvas_graphe)

        scrollable_frame_graphe.bind(
            "<Configure>",
            lambda e: canvas_graphe.configure(
                scrollregion=canvas_graphe.bbox("all")
            )
        )

        canvas_graphe.create_window((0, 0), window=scrollable_frame_graphe, anchor="nw")
        canvas_graphe.configure(yscrollcommand=scrollbar_graphe.set)

        canvas_graphe.pack(side="left", fill="both", expand=True)
        scrollbar_graphe.pack(side="right", fill="y")

        # Afficher le graphe avec matplotlib dans l'onglet Graphe
        fig, ax = plt.subplots(figsize=(10, 6))
        G = nx.DiGraph()
        for u in graphe:
            for v, capacite in graphe[u].items():
                flot = graphe[u][v] - graphe_residuel[u].get(v, 0)
                label = f"{flot}/{capacite}"
                G.add_edge(u, v, label=label)

        pos = nx.spring_layout(G)
        couleurs_noeuds = ['lightblue' if node not in coupe_min[0] else 'lightcoral' for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=couleurs_noeuds, edge_color='black', node_size=2000, font_size=10, ax=ax)
        etiquettes_arêtes = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquettes_arêtes, font_size=8, ax=ax)

        # Colorier les arêtes de la coupe minimale en rouge
        if coupe_min:
            arêtes_coupe_min = coupe_min[1]
            nx.draw_networkx_edges(G, pos, edgelist=arêtes_coupe_min, edge_color='red', width=0.75)

        # Intégrer le graphe dans l'onglet Graphe
        canvas = FigureCanvasTkAgg(fig, master=scrollable_frame_graphe)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Onglet 2 : Tableaux
        tableaux_tab = ttk.Frame(notebook)
        notebook.add(tableaux_tab, text="Tableaux")

        # Ajouter une barre de défilement à l'onglet Tableaux
        canvas_tableaux = tk.Canvas(tableaux_tab)
        scrollbar_tableaux = ttk.Scrollbar(tableaux_tab, orient="vertical", command=canvas_tableaux.yview)
        scrollable_frame_tableaux = ttk.Frame(canvas_tableaux)

        scrollable_frame_tableaux.bind(
            "<Configure>",
            lambda e: canvas_tableaux.configure(
                scrollregion=canvas_tableaux.bbox("all")
            )
        )

        canvas_tableaux.create_window((0, 0), window=scrollable_frame_tableaux, anchor="nw")
        canvas_tableaux.configure(yscrollcommand=scrollbar_tableaux.set)

        canvas_tableaux.pack(side="left", fill="both", expand=True)
        scrollbar_tableaux.pack(side="right", fill="y")

        # Afficher les résultats au-dessus du tableau
        resultats_label = tk.Label(scrollable_frame_tableaux,
                                   text=f"Flot maximal : {flot_max}\n"
                                        f"Flot sortant total du source ({source}) : {flot_sortant}\n"
                                        f"Flot entrant total du puits ({puits}) : {flot_entrant}\n"
                                        f"Coupe minimale : {coupe_min[1]}",
                                   font=('Arial', 12),
                                   bg='#f0f0f0',
                                   fg='#111211')
        resultats_label.pack(pady=10)

        # Afficher le tableau du graphe dans l'onglet Tableaux
        tableau_graphe = afficher_graphe_en_table(graphe)
        tableau_label = tk.Label(scrollable_frame_tableaux, text=tableau_graphe, font=('Courier', 10), bg='#f0f0f0', fg='#008000')
        tableau_label.pack(pady=10)

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")