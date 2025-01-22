import random
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def generer_tableau_taches(nombre_taches):
    tableau = []
    for i in range(nombre_taches):
        duree = random.randint(1, 10)
        anteriorite = random.sample(range(1, nombre_taches + 1), random.randint(0, min(3, i)))
        anteriorite = [ant for ant in anteriorite if ant < i + 1]
        tableau.append({"id": i + 1, "duree": duree, "anteriorite": anteriorite})
    return tableau

def potentiel_metra(taches):
    G = nx.DiGraph()
    
    # Ajouter les nœuds et les arêtes
    for tache in taches:
        G.add_node(tache["id"], duree=tache["duree"])
        for ant in tache["anteriorite"]:
            G.add_edge(ant, tache["id"])
    
    # Ajouter nœuds début et fin
    G.add_node(0, duree=0)
    G.add_node(len(taches) + 1, duree=0)
    
    # Connecter les nœuds isolés
    for tache in taches:
        if not list(G.predecessors(tache["id"])):
            G.add_edge(0, tache["id"])
        if not list(G.successors(tache["id"])):
            G.add_edge(tache["id"], len(taches) + 1)
    
    # Calculer les dates au plus tôt
    dates_tot = {}
    for node in nx.topological_sort(G):
        if node == 0:
            dates_tot[node] = 0
        else:
            pred_dates = [dates_tot[pred] + G.nodes[pred]['duree'] for pred in G.predecessors(node)]
            dates_tot[node] = max(pred_dates) if pred_dates else 0

    # Calculer les dates au plus tard
    dates_tard = {}
    duree_totale = dates_tot[len(taches) + 1]
    for node in reversed(list(nx.topological_sort(G))):
        if node == len(taches) + 1:
            dates_tard[node] = duree_totale
        else:
            succ_dates = [dates_tard[succ] - G.nodes[node]['duree'] for succ in G.successors(node)]
            dates_tard[node] = min(succ_dates) if succ_dates else duree_totale
    
    # Calculer les marges
    marges = {n: dates_tard[n] - dates_tot[n] for n in G.nodes()}
    
    # Identifier le chemin critique
    chemin_critique = [n for n in G.nodes() if marges[n] == 0]
    
    return G, dates_tot, dates_tard, marges, chemin_critique

def run_potentiel_metra(entry_tasks, info_frame):
    try:
        # Récupérer le nombre de tâches
        nombre_taches = int(entry_tasks.get())
        
        # Générer les tâches et exécuter l'algorithme
        taches = generer_tableau_taches(nombre_taches)
        G, dates_tot, dates_tard, marges, chemin_critique = potentiel_metra(taches)
        
        # Effacer le contenu précédent du cadre
        for widget in info_frame.winfo_children():
            widget.destroy()

        # Créer un cadre pour les résultats textuels
        text_frame = tk.Frame(info_frame, bg='#f0f0f0')
        text_frame.pack(fill='x', pady=10)

        # Afficher les dates au plus tôt
        dates_tot_frame = tk.Frame(text_frame, bg='#f0f0f0')
        dates_tot_frame.pack(fill='x', pady=5)
        tk.Label(dates_tot_frame, text="Dates au plus tôt :", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(side='left')
        for node, date in dates_tot.items():
            tk.Label(dates_tot_frame, text=f"T{node}({date}) ,", font=('Arial', 12), bg='#f0f0f0').pack(side='left', padx=5)

        # Afficher les dates au plus tard
        dates_tard_frame = tk.Frame(text_frame, bg='#f0f0f0')
        dates_tard_frame.pack(fill='x', pady=5)
        tk.Label(dates_tard_frame, text="Dates au plus tard :", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(side='left')
        for node, date in dates_tard.items():
            tk.Label(dates_tard_frame, text=f"T{node}({date}) ,", font=('Arial', 12), bg='#f0f0f0').pack(side='left', padx=5)

        # Afficher les marges
        marges_frame = tk.Frame(text_frame, bg='#f0f0f0')
        marges_frame.pack(fill='x', pady=5)
        tk.Label(marges_frame, text="Marges :", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(side='left')
        for node, marge in marges.items():
            tk.Label(marges_frame, text=f"T{node}({marge}) ,", font=('Arial', 12), bg='#f0f0f0').pack(side='left', padx=5)

        # Afficher le chemin critique
        chemin_critique_frame = tk.Frame(text_frame, bg='#f0f0f0')
        chemin_critique_frame.pack(fill='x', pady=5)
        tk.Label(chemin_critique_frame, text="Chemin critique : ", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(side='left')
        tk.Label(chemin_critique_frame, text=" ---> ".join(map(str, chemin_critique)), font=('Arial', 12), bg='#f0f0f0').pack(side='left')

        # Dessiner le graphe avec matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)

        # Dessiner les nœuds et les arêtes
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=800, node_color="lightblue", font_size=10, font_weight="bold")

        # Mettre en évidence le chemin critique
        critical_edges = [(u, v) for u, v in G.edges() if u in chemin_critique and v in chemin_critique]
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=critical_edges, edge_color="red", width=0.75)

        # Ajouter les labels pour les durées des tâches
        node_labels = {node: f"\n{node}\n({G.nodes[node]['duree']})" for node in G.nodes}
        nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=10, font_weight="bold")
        # Intégrer le graphe dans l'interface Tkinter
        canvas = FigureCanvasTkAgg(fig, master=info_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, pady=10)

    except ValueError:
        error_label = tk.Label(info_frame, text="Veuillez entrer un nombre valide.", font=('Arial', 12), bg='#f0f0f0', fg='red')
        error_label.pack(pady=10)