import tkinter as tk
from tkinter import ttk
from welsh_powel import run_welsh_powel

class AlgorithmGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorithmes de Recherche Opérationnelle")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Centrer la fenêtre principale
        self.center_window(self.root, 600, 400)
        
        self.create_welcome_page()
        
    def center_window(self, window, width, height):
        """Centre une fenêtre Tkinter sur l'écran."""
        screen_width = window.winfo_screenwidth()  # Largeur de l'écran
        screen_height = window.winfo_screenheight()  # Hauteur de l'écran

        # Calculer les coordonnées (x, y) pour centrer la fenêtre
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Appliquer la géométrie pour centrer la fenêtre
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_welcome_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.root, bg='#f0f0f0')
        welcome_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(welcome_frame,
                         text="Bienvenue ",
                         font=('Arial', 18, 'bold'),
                         bg='#f0f0f0',
                         fg='#008000')
        title.pack(pady=10)
        
        inner_frame = tk.Frame(welcome_frame, bg='white', bd=2, relief='solid')
        inner_frame.pack(padx=20, pady=20)
        
        algo_label = tk.Label(inner_frame,
                              text="Algorithme de Recherche operationnelle",
                              font=("Arial", 12),
                              bg='white',
                              fg='#008000')
        algo_label.pack(pady=10)
        
        button_frame = tk.Frame(inner_frame, bg='white')
        button_frame.pack(pady=10)
        
        entree_btn = tk.Button(button_frame,
                               text="Entree",
                               command=self.show_algorithms,
                               width=10,
                               relief="flat",
                               bg='#008000',
                               fg='white',
                               font=('Arial', 11))
        entree_btn.pack(side=tk.LEFT, padx=10)
        
        sortie_btn = tk.Button(button_frame,
                               text="Sortie",
                               command=self.root.quit,
                               width=10,
                               relief="flat",
                               bg='#008000',
                               fg='white',
                               font=('Arial', 11))
        sortie_btn.pack(side=tk.LEFT, padx=10)
        
        signature = tk.Label(welcome_frame,
                             text="idrissi khamlichi abdelhadi",
                             font=('Arial', 10, 'italic'),
                             bg='#f0f0f0',
                             fg='#008000')
        signature.pack(side=tk.BOTTOM, pady=10)
        
    def show_algorithms(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(main_frame,
                         text="Algorithmes",
                         font=('Arial', 18, 'bold'),
                         bg='#f0f0f0',
                         fg='#008000')
        title.pack(pady=10)
        
        algorithms = [
            "Welsh Powel", "Dijkstra", "Potentiel Metra",
            "Kruskal", "Bellman Ford", "Ford Fulckerson",
            "Nord-Ouest", "Moindre Cout", "Steepping-Stone"
        ]
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(expand=True, fill='both', padx=20)
        
        for i, algo in enumerate(algorithms):
            btn = tk.Button(button_frame,
                            text=algo,
                            font=('Arial', 11),
                            bg='#008000',
                            fg='white',
                            relief='flat',
                            width=15,
                            height=2,
                            command=lambda a=algo: self.open_algorithm(a))
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#006400'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#008000'))
        
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)
            
        retour_btn = tk.Button(button_frame,
                               text="Retour",
                               font=('Arial', 11),
                               bg='#008000',
                               fg='white',
                               relief='flat',
                               width=15,
                               height=2,
                               command=self.create_welcome_page)
        retour_btn.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

        retour_btn.bind('<Enter>', lambda e, b=retour_btn: b.configure(bg='#006400'))
        retour_btn.bind('<Leave>', lambda e, b=retour_btn: b.configure(bg='#008000'))

        for i in range(4):
            button_frame.grid_rowconfigure(i, weight=1)
        
        signature = tk.Label(main_frame,
                             text="idrissi khamlichi abdelhadi",
                             font=('Arial', 10, 'italic'),
                             bg='#f0f0f0',
                             fg='#008000')
        signature.pack(side=tk.BOTTOM, pady=10)
        
    def open_algorithm(self, algorithm_name):
        if algorithm_name == "Welsh Powel":
            self.open_welsh_powel_page()
        else:
            print(f"Ouverture de l'algorithme {algorithm_name}")

    def open_welsh_powel_page(self):
        # Créer une nouvelle fenêtre pour l'algorithme de Welsh-Powell
        self.welsh_powel_window = tk.Toplevel(self.root)
        self.welsh_powel_window.title("Welsh-Powell")
        self.welsh_powel_window.geometry("600x500")  # Taille fixe pour la fenêtre
        self.welsh_powel_window.configure(bg='#f0f0f0')

        # Centrer la fenêtre de Welsh-Powell
        self.center_window(self.welsh_powel_window, 600, 500)

        # Champ d'entrée pour le nombre de sommets
        input_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label = tk.Label(input_frame,
                         text="Entrez le nombre de sommets :",
                         font=('Arial', 12),
                         bg='#f0f0f0',
                         fg='#008000')
        label.pack(side=tk.LEFT, padx=10)

        self.entry = tk.Entry(input_frame, font=('Arial', 12), width=20)  # Champ d'entrée plus large
        self.entry.pack(side=tk.LEFT, padx=10)

        # Bouton pour exécuter l'algorithme
        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=lambda: run_welsh_powel(self.entry, self.graph_frame, self.info_frame))
        execute_btn.pack(side=tk.LEFT, padx=10)

        # Zone pour afficher le graphe (initialement vide)
        self.graph_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # Zone pour afficher les informations (nombre de couleurs et temps d'exécution)
        self.info_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AlgorithmGUI()
    app.run()