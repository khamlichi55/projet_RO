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

def moindre_cout(factory_capacities, client_demands, transport_costs):
    """Applique l'algorithme Moindre Coût."""
    num_factories = len(factory_capacities)
    num_clients = len(client_demands)
    transport_plan = np.zeros((num_factories, num_clients))

    cost_list = [(i, j, transport_costs[i][j]) for i in range(num_factories) for j in range(num_clients)]
    cost_list.sort(key=lambda x: x[2])  # Trier par coût croissant

    for i, j, _ in cost_list:
        if factory_capacities[i] > 0 and client_demands[j] > 0:
            amount = min(factory_capacities[i], client_demands[j])
            transport_plan[i][j] = amount
            factory_capacities[i] -= amount
            client_demands[j] -= amount

    return transport_plan

def run_moindre_cout(entry_factories, entry_clients, info_frame):
    """Exécute l'algorithme Moindre Coût et affiche les résultats."""
    try:
        num_factories = int(entry_factories.get())
        num_clients = int(entry_clients.get())
        if num_factories <= 0 or num_clients <= 0:
            raise ValueError
    except ValueError:
        print("Veuillez entrer des nombres valides pour les usines et les clients.")
        return

    factory_capacities, client_demands, transport_costs = generate_data(num_factories, num_clients)
    transport_plan = moindre_cout(factory_capacities.copy(), client_demands.copy(), transport_costs)
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
                          text=f"Coût total (Moindre Coût) : {cost}",
                          font=('Arial', 12),
                          bg='#f0f0f0',
                          fg='#008000')
    cost_label.pack(pady=5)