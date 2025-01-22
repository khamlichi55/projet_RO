import numpy as np
import random
import tkinter as tk
from tkinter import ttk

def calculate_total_cost(transport_plan, transport_costs):
    """Calcule le coût total du plan de transport."""
    return np.sum(transport_plan * transport_costs)

def generate_data(num_factories, num_clients):
    """Génère des données aléatoires pour les usines et les clients."""
    factory_capacities = [random.randint(50, 150) for _ in range(num_factories)]
    client_demands = [random.randint(50, 150) for _ in range(num_clients)]
    transport_costs = np.random.randint(1, 10, size=(num_factories, num_clients))
    return factory_capacities, client_demands, transport_costs

def north_west_corner(factory_capacities, client_demands, transport_costs):
    """Applique l'algorithme North-West Corner."""
    num_factories = len(factory_capacities)
    num_clients = len(client_demands)
    transport_plan = np.zeros((num_factories, num_clients))

    i, j = 0, 0
    while i < num_factories and j < num_clients:
        amount = min(factory_capacities[i], client_demands[j])
        transport_plan[i][j] = amount
        factory_capacities[i] -= amount
        client_demands[j] -= amount

        if factory_capacities[i] == 0:
            i += 1
        if client_demands[j] == 0:
            j += 1

    return transport_plan

def run_north_west_corner(entry_factories, entry_clients, info_frame):
    """Exécute l'algorithme North-West Corner et affiche les résultats."""
    try:
        num_factories = int(entry_factories.get())
        num_clients = int(entry_clients.get())
        if num_factories <= 0 or num_clients <= 0:
            raise ValueError
    except ValueError:
        print("Veuillez entrer des nombres valides pour les usines et les clients.")
        return

    factory_capacities, client_demands, transport_costs = generate_data(num_factories, num_clients)
    transport_plan = north_west_corner(factory_capacities.copy(), client_demands.copy(), transport_costs)
    cost = calculate_total_cost(transport_plan, transport_costs)

    # Afficher les résultats dans l'interface graphique
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Créer un tableau pour afficher le plan de transport
    tree = ttk.Treeview(info_frame, columns=[f"Client {j+1}" for j in range(num_clients)], show="headings")
    for j in range(num_clients):
        tree.heading(f"Client {j+1}", text=f"Client {j+1}")
    for i in range(num_factories):
        tree.insert("", "end", values=[f"{transport_plan[i][j]}" for j in range(num_clients)])
    tree.pack(pady=10)

    # Afficher le coût total
    cost_label = tk.Label(info_frame,
                          text=f"Coût total (North-West Corner) : {cost}",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    cost_label.pack(pady=5)