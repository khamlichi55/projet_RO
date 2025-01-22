import tkinter as tk
from tkinter import ttk
import random

# Fonctions de l'algorithme
def generate_random_costs(rows, cols):
    return [[random.randint(1, 20) for _ in range(cols)] for _ in range(rows)]

def northwest_corner_method(supply, demand, costs):
    rows, cols = len(supply), len(demand)
    allocation = [[0] * cols for _ in range(rows)]

    i, j = 0, 0
    while i < rows and j < cols:
        allocation[i][j] = min(supply[i], demand[j])
        if supply[i] < demand[j]:
            demand[j] -= supply[i]
            supply[i] = 0
            i += 1
        else:
            supply[i] -= demand[j]
            demand[j] = 0
            j += 1

    total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    return allocation, total_cost

def moindre_cout_method(supply, demand, costs):
    rows, cols = len(supply), len(demand)
    allocation = [[0] * cols for _ in range(rows)]
    
    while any(supply) and any(demand):
        # Trouver la cellule avec le coût minimum
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(rows):
            for j in range(cols):
                if supply[i] > 0 and demand[j] > 0 and costs[i][j] < min_cost:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        # Allouer autant que possible à la cellule avec le coût minimum
        allocation[min_i][min_j] = min(supply[min_i], demand[min_j])
        if supply[min_i] < demand[min_j]:
            demand[min_j] -= supply[min_i]
            supply[min_i] = 0
        else:
            supply[min_i] -= demand[min_j]
            demand[min_j] = 0

    total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    return allocation, total_cost

def stepping_stone_method(allocation, costs):
    rows, cols = len(allocation), len(allocation[0])

    def get_closed_path(allocation, start):
        visited = set()
        stack = [(start, [start])]
        while stack:
            (x, y), path = stack.pop()
            visited.add((x, y))
            if len(path) > 3 and path[0] == path[-1]:
                return path
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and
                        (nx, ny) not in visited and allocation[nx][ny] != 0):
                    stack.append(((nx, ny), path + [(nx, ny)]))
        return []

    while True:
        u = [None] * rows
        v = [None] * cols
        u[0] = 0

        for _ in range(rows + cols):
            for i in range(rows):
                for j in range(cols):
                    if allocation[i][j] != 0:
                        if u[i] is not None and v[j] is None:
                            v[j] = costs[i][j] - u[i]
                        elif v[j] is not None and u[i] is None:
                            u[i] = costs[i][j] - v[j]

        opportunity_costs = [
            [costs[i][j] - (u[i] + v[j]) if u[i] is not None and v[j] is not None else None for j in range(cols)]
            for i in range(rows)
        ]

        min_cost = min((val for row in opportunity_costs for val in row if val is not None and val < 0), default=None)
        if min_cost is None:
            break

        min_cell = None
        for i in range(rows):
            for j in range(cols):
                if opportunity_costs[i][j] == min_cost:
                    min_cell = (i, j)
                    break
            if min_cell:
                break

        path = get_closed_path(allocation, min_cell)
        if not path:
            break

        min_alloc = min(allocation[x][y] for x, y in path[1::2])
        for i, (x, y) in enumerate(path):
            allocation[x][y] += min_alloc if i % 2 == 0 else -min_alloc

    total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    return allocation, total_cost

# Interface graphique
class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Problème de Transport")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Bouton pour ouvrir la fenêtre Stepping Stone
        open_stepping_stone_btn = tk.Button(
            self.root,
            text="Ouvrir Stepping Stone",
            font=('Arial', 12),
            bg='#008000',
            fg='white',
            relief='flat',
            command=self.open_stepping_stone
        )
        open_stepping_stone_btn.pack(pady=20)

    def open_stepping_stone(self):
        self.stepping_stone_window = tk.Toplevel(self.root)
        self.stepping_stone_window.title("Stepping Stone")
        self.stepping_stone_window.geometry("600x500")
        self.stepping_stone_window.configure(bg='#f0f0f0')

        self.center_window(self.stepping_stone_window, 600, 500)

        input_frame = tk.Frame(self.stepping_stone_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_factories = tk.Label(input_frame,
                                   text="Nombre d'usines :",
                                   font=('Arial', 12),
                                   bg='#f0f0f0',
                                   fg='#008000')
        label_factories.grid(row=0, column=0, padx=10, pady=5)

        self.entry_factories = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_factories.grid(row=0, column=1, padx=10, pady=5)

        label_clients = tk.Label(input_frame,
                                 text="Nombre de clients :",
                                 font=('Arial', 12),
                                 bg='#f0f0f0',
                                 fg='#008000')
        label_clients.grid(row=1, column=0, padx=10, pady=5)

        self.entry_clients = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_clients.grid(row=1, column=1, padx=10, pady=5)

        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=self.run_all_algorithms)
        execute_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.info_frame = tk.Frame(self.stepping_stone_window, bg='#f0f0f0')
        self.info_frame.pack(fill='both', expand=True, pady=10)

    def run_all_algorithms(self):
        try:
            num_factories = int(self.entry_factories.get())
            num_clients = int(self.entry_clients.get())

            # Générer des données aléatoires
            supply = [random.randint(50, 150) for _ in range(num_factories)]
            demand = [random.randint(50, 150) for _ in range(num_clients)]
            costs = generate_random_costs(num_factories, num_clients)

            # Exécuter les trois algorithmes
            nw_allocation, nw_total_cost = northwest_corner_method(supply.copy(), demand.copy(), costs)
            moindre_allocation, moindre_total_cost = moindre_cout_method(supply.copy(), demand.copy(), costs)

            # Sélectionner le résultat le plus optimal
            if nw_total_cost < moindre_total_cost:
                optimal_allocation = nw_allocation
                optimal_cost = nw_total_cost
                optimal_method = "Nord-Ouest"
            else:
                optimal_allocation = moindre_allocation
                optimal_cost = moindre_total_cost
                optimal_method = "Moindre Coût"

            # Appliquer la méthode Stepping Stone
            final_allocation, final_cost = stepping_stone_method(optimal_allocation, costs)

            # Afficher les résultats dans l'interface
            self.display_results(self.info_frame, nw_allocation, moindre_allocation, final_allocation,
                                nw_total_cost, moindre_total_cost, final_cost, optimal_method)

        except ValueError:
            print("Erreur : Veuillez entrer des valeurs numériques valides.")

    def display_results(self, info_frame, nw_allocation, moindre_allocation, final_allocation,
                       nw_total_cost, moindre_total_cost, final_cost, optimal_method):
        # Effacer le contenu précédent du cadre
        for widget in info_frame.winfo_children():
            widget.destroy()

        # Créer un cadre pour chaque algorithme
        frame_nw = tk.Frame(info_frame, bg='#f0f0f0')
        frame_mc = tk.Frame(info_frame, bg='#f0f0f0')
        frame_ss = tk.Frame(info_frame, bg='#f0f0f0')

        # Placer les cadres verticalement
        frame_nw.pack(fill='x', padx=10, pady=10)
        frame_mc.pack(fill='x', padx=10, pady=10)
        frame_ss.pack(fill='x', padx=10, pady=10)

        # Afficher les résultats pour chaque algorithme
        self.display_table(frame_nw, nw_allocation, "Nord-Ouest", nw_total_cost)
        self.display_table(frame_mc, moindre_allocation, "Moindre Coût", moindre_total_cost)
        self.display_table(frame_ss, final_allocation, f"Stepping Stone ({optimal_method})", final_cost)

    def display_table(self, frame, data, title, total_cost):
        # Ajouter un label pour le titre et le coût total
        title_label = tk.Label(frame, text=f"{title} - Coût total : {total_cost:.2f}", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=5)

        # Créer un tableau pour afficher les données
        columns = [f"Client {j+1}" for j in range(len(data[0]))]
        tree = ttk.Treeview(frame, columns=columns, show='headings')

        # Configurer les colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor='center')

        # Ajouter les données
        for i, row in enumerate(data):
            tree.insert("", "end", values=[f"{v:.0f}" for v in row])

        # Ajouter une barre de défilement verticale
        scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar_y.pack(side='right', fill='y')

        # Configurer le tableau pour la barre de défilement
        tree.configure(yscrollcommand=scrollbar_y.set)

        # Placer le tableau
        tree.pack(side='left', fill='both', expand=True)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

# Exécution de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()