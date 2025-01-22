import tkinter as tk
from tkinter import ttk
from welsh_powel import run_welsh_powel
from kruskal import run_kruskal
from bellman_ford import run_bellman_ford
from dijkstra import run_dijkstra
from north_west_corner import run_north_west_corner
from potentiel_metra import run_potentiel_metra
from moindre_cout import run_moindre_cout
from stepping_stone import generate_random_costs, northwest_corner_method, moindre_cout_method, stepping_stone_method
import random


from ford_fulkerson import run_ford_fulkerson# Ajout de Ford-Fulkerson
from PIL import Image, ImageTk

class AlgorithmGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorithmes de Recherche Opérationnelle")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Centrer la fenêtre principale
        self.center_window(self.root, 700, 500)
        
        self.create_welcome_page()
        
    def center_window(self, window, width, height):
        """Centre une fenêtre Tkinter sur l'écran."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_welcome_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.root, bg='#f0f0f0')
        welcome_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
         
        
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
                              font=("Georgia", 15),
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
        
        # Correction du bouton "Sortie"
        sortie_btn = tk.Button(button_frame,
                               text="Sortie",
                               command=self.exit_application,
                               width=10,
                               relief="flat",
                               bg='#008000',
                               fg='white',
                               font=('Arial', 11))
        sortie_btn.pack(side=tk.LEFT, padx=10)
             # Create a frame for the image with a red border
        image_frame = tk.Frame(welcome_frame, relief='solid')
        image_frame.pack(pady=10)
       
        # Load and display the image
        img = Image.open("E:/MonProjet/python/logo-1.png")
        img = img.resize((500, 90))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(img)
       
        img_label = tk.Label(image_frame, image=photo, bg='#f0f0f0')
        img_label.image = photo  # Keep a reference to prevent garbage collection
        img_label.pack()
        
        signature = tk.Label(welcome_frame,
                             text="Etudiant : Idrissi Khamlichi Abdelhadi \nEncadrant : El mkhalet Mouna",
                             font=('Arial', 10, 'bold'),
                             bg='#f0f0f0',
                             fg='#475447')
        signature.pack(side=tk.BOTTOM, pady=10)

    def exit_application(self):
        """Ferme proprement l'application."""
        self.root.destroy() 
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
            "Nord-Ouest", "Moindre Cout", "Stepping-Stone"
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
                             text="Etudiant : Idrissi Khamlichi Abdelhadi \nEncadrant : El mkhalet Mouna",
                             font=('Arial', 10, 'bold'),
                             bg='#f0f0f0',
                             fg='#475447')
        signature.pack(side=tk.BOTTOM, pady=10)
        
        
    def open_algorithm(self, algorithm_name):
        if algorithm_name == "Welsh Powel":
            self.open_welsh_powel_page()
        elif algorithm_name == "Kruskal":
            self.open_kruskal_page()
        elif algorithm_name == "Bellman Ford":
            self.open_bellman_ford_page()
        elif algorithm_name == "Dijkstra":
            self.open_dijkstra_page()
        elif algorithm_name == "Nord-Ouest":
            self.open_north_west_page()
        elif algorithm_name == "Moindre Cout":
            self.open_moindre_cout_page()
        elif algorithm_name == "Stepping-Stone":
            self.open_stepping_stone()
        elif algorithm_name == "Ford Fulckerson":  
            self.open_ford_fulkerson_page()
        elif algorithm_name == "Potentiel Metra":  
            self.open_potentiel_metra_page()
        else:
            print(f"Ouverture de l'algorithme {algorithm_name}")
            
            
    def open_welsh_powel_page(self):
        self.welsh_powel_window = tk.Toplevel(self.root)
        self.welsh_powel_window.title("Welsh-Powell")
        self.welsh_powel_window.geometry("600x500")
        self.welsh_powel_window.configure(bg='#f0f0f0')

        self.center_window(self.welsh_powel_window, 600, 500)

        input_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label = tk.Label(input_frame,
                         text="Entrez le nombre de sommets :",
                         font=('Arial', 12 ,'bold'),
                         bg='#f0f0f0',
                         fg='#008000')
        label.pack(side=tk.LEFT, padx=10)

        self.entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.entry.pack(side=tk.LEFT, padx=10)

        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=lambda: run_welsh_powel(self.entry, self.graph_frame, self.info_frame))
        execute_btn.pack(side=tk.LEFT, padx=10)

        self.graph_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

        self.info_frame = tk.Frame(self.welsh_powel_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)      
            
    def open_bellman_ford_page(self):
        self.bellman_ford_window = tk.Toplevel(self.root)
        self.bellman_ford_window.title("Bellman-Ford")
        self.bellman_ford_window.geometry("600x600")
        self.bellman_ford_window.configure(bg='#f0f0f0')
        
        self.center_window(self.bellman_ford_window, 600, 500)

    # Créer un Canvas avec une Scrollbar
        canvas = tk.Canvas(self.bellman_ford_window, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(self.bellman_ford_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

    # Configurer le Canvas et la Scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Ajouter les widgets dans le cadre défilable
        input_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_n = tk.Label(input_frame,
                       text="Nombre de sommets :",
                       font=('Arial', 12 ,'bold'),
                       bg='#f0f0f0',
                       fg='#008000')
        label_n.grid(row=0, column=0, padx=10, pady=5)

        self.entry_n = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_n.grid(row=0, column=1, padx=10, pady=5)

        label_pourcentage = tk.Label(input_frame,
                                 text="Pourcentage de liaisons (0.0 à 1.0) :",
                                 font=('Arial', 12 ,'bold'),
                                 bg='#f0f0f0',
                                 fg='#008000')
        label_pourcentage.grid(row=1, column=0, padx=10, pady=5)

        self.entry_pourcentage = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_pourcentage.grid(row=1, column=1, padx=10, pady=5)

        label_depart = tk.Label(input_frame,
                            text="Sommet de départ (x1):",
                            font=('Arial', 12 ,'bold'),
                            bg='#f0f0f0',
                            fg='#008000')
        label_depart.grid(row=2, column=0, padx=10, pady=5)

        self.entry_depart = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_depart.grid(row=2, column=1, padx=10, pady=5)

        label_arrivee = tk.Label(input_frame,
                             text="Sommet d'arrivée (x2):",
                             font=('Arial', 12 ,'bold'),
                             bg='#f0f0f0',
                             fg='#008000')
        label_arrivee.grid(row=3, column=0, padx=10, pady=5)

        self.entry_arrivee = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_arrivee.grid(row=3, column=1, padx=10, pady=5)

        execute_btn = tk.Button(input_frame,
                            text="Exécuter",
                            font=('Arial', 12),
                            bg='#008000',
                            fg='white',
                            relief='flat',
                            command=lambda: run_bellman_ford(self.entry_n, self.entry_pourcentage, self.entry_depart, self.entry_arrivee, self.graph_frame, self.info_frame))
        execute_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Ajouter le cadre pour le graphe
        self.graph_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

    # Ajouter le cadre pour les informations
        self.info_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.info_frame.pack(pady=10)

    def open_kruskal_page(self):
        self.kruskal_window = tk.Toplevel(self.root)
        self.kruskal_window.title("Kruskal")
        self.kruskal_window.geometry("600x500")
        self.kruskal_window.configure(bg='#f0f0f0')

        self.center_window(self.kruskal_window, 600, 500)

        input_frame = tk.Frame(self.kruskal_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label = tk.Label(input_frame,
                         text="Entrez le nombre de sommets :",
                         font=('Arial', 12 ,'bold'),
                         bg='#f0f0f0',
                         fg='#008000')
        label.pack(side=tk.LEFT, padx=10)

        self.entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.entry.pack(side=tk.LEFT, padx=10)

        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=lambda: run_kruskal(self.entry, self.graph_frame, self.info_frame))
        execute_btn.pack(side=tk.LEFT, padx=10)

        self.graph_frame = tk.Frame(self.kruskal_window, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

        self.info_frame = tk.Frame(self.kruskal_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)

    def open_dijkstra_page(self):
        self.dijkstra_window = tk.Toplevel(self.root)
        self.dijkstra_window.title("Dijkstra")
        self.dijkstra_window.geometry("600x600")
        self.dijkstra_window.configure(bg='#f0f0f0')

        self.center_window(self.dijkstra_window, 600, 500)

    # Créer un Canvas avec une Scrollbar
        canvas = tk.Canvas(self.dijkstra_window, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(self.dijkstra_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

    # Configurer le Canvas et la Scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ajouter les widgets dans le cadre défilable
        input_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_n = tk.Label(input_frame,
                       text="Nombre de sommets :",
                       font=('Arial', 12 ,'bold'),
                       bg='#f0f0f0',
                       fg='#008000')
        label_n.grid(row=0, column=0, padx=10, pady=5)

        self.entry_n = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_n.grid(row=0, column=1, padx=10, pady=5)

        label_pourcentage = tk.Label(input_frame,
                                 text="Pourcentage de liaisons (0-100) :",
                                 font=('Arial', 12 ,'bold'),
                                 bg='#f0f0f0',
                                 fg='#008000')
        label_pourcentage.grid(row=1, column=0, padx=10, pady=5)

        self.entry_pourcentage = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_pourcentage.grid(row=1, column=1, padx=10, pady=5)

        label_depart = tk.Label(input_frame,
                            text="Sommet de départ (x1):",
                            font=('Arial', 12 ,'bold'),
                            bg='#f0f0f0',
                            fg='#008000')
        label_depart.grid(row=2, column=0, padx=10, pady=5)

        self.entry_depart = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_depart.grid(row=2, column=1, padx=10, pady=5)

        label_arrivee = tk.Label(input_frame,
                                 text="Sommet d'arrivée (x2):",
                             font=('Arial', 12 ,'bold'),
                             bg='#f0f0f0',
                             fg='#008000')
        label_arrivee.grid(row=3, column=0, padx=10, pady=5)

        self.entry_arrivee = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_arrivee.grid(row=3, column=1, padx=10, pady=5)

        execute_btn = tk.Button(input_frame,
                            text="Exécuter",
                            font=('Arial', 12 ,'bold'),
                            bg='#008000',
                            fg='white',
                            relief='flat',
                            command=lambda: run_dijkstra(self.entry_n, self.entry_pourcentage, self.entry_depart, self.entry_arrivee, self.graph_frame, self.info_frame))
        execute_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Ajouter le cadre pour le graphe
        self.graph_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

    # Ajouter le cadre pour les informations
        self.info_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.info_frame.pack(pady=10)

    def open_north_west_page(self):
        self.north_west_window = tk.Toplevel(self.root)
        self.north_west_window.title("North-West Corner")
        self.north_west_window.geometry("600x500")
        self.north_west_window.configure(bg='#f0f0f0')

        self.center_window(self.north_west_window, 600, 500)

        input_frame = tk.Frame(self.north_west_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_factories = tk.Label(input_frame,
                                   text="Nombre d'usines :",
                                   font=('Arial', 12 ,'bold'),
                                   bg='#f0f0f0',
                                   fg='#008000')
        label_factories.grid(row=0, column=0, padx=10, pady=5)

        self.entry_factories = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_factories.grid(row=0, column=1, padx=10, pady=5)

        label_clients = tk.Label(input_frame,
                                 text="Nombre de clients :",
                                 font=('Arial', 12 ,'bold'),
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
                                command=lambda: run_north_west_corner(self.entry_factories, self.entry_clients, self.info_frame))
        execute_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.info_frame = tk.Frame(self.north_west_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)

    def open_moindre_cout_page(self):
        self.moindre_cout_window = tk.Toplevel(self.root)
        self.moindre_cout_window.title("Moindre Coût")
        self.moindre_cout_window.geometry("600x500")
        self.moindre_cout_window.configure(bg='#f0f0f0')

        self.center_window(self.moindre_cout_window, 600, 500)

        input_frame = tk.Frame(self.moindre_cout_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_factories = tk.Label(input_frame,
                                   text="Nombre d'usines :",
                                   font=('Arial', 12 ,'bold'),
                                   bg='#f0f0f0',
                                   fg='#008000')
        label_factories.grid(row=0, column=0, padx=10, pady=5)

        self.entry_factories = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_factories.grid(row=0, column=1, padx=10, pady=5)

        label_clients = tk.Label(input_frame,
                                 text="Nombre de clients :",
                                 font=('Arial', 12 ,'bold'),
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
                                command=lambda: run_moindre_cout(self.entry_factories, self.entry_clients, self.info_frame))
        execute_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.info_frame = tk.Frame(self.moindre_cout_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)
    

    def open_ford_fulkerson_page(self):
    
        self.ford_fulkerson_window = tk.Toplevel(self.root)
        self.ford_fulkerson_window.title("Ford-Fulkerson")
        self.ford_fulkerson_window.geometry("600x500")
        self.ford_fulkerson_window.configure(bg='#f0f0f0')

        self.center_window(self.ford_fulkerson_window, 600, 500)

        input_frame = tk.Frame(self.ford_fulkerson_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_n = tk.Label(input_frame,
                           text="Nombre de sommets :",
                           font=('Arial', 12 ,'bold'),
                           bg='#f0f0f0',
                           fg='#008000')
        label_n.grid(row=0, column=0, padx=10, pady=5)

        self.entry_n = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_n.grid(row=0, column=1, padx=10, pady=5)

        label_source = tk.Label(input_frame,
                                text="Sommet source (1):",
                                font=('Arial', 12 ,'bold'),
                                bg='#f0f0f0',
                                fg='#008000')
        label_source.grid(row=1, column=0, padx=10, pady=5)

        self.entry_source = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_source.grid(row=1, column=1, padx=10, pady=5)

        label_sink = tk.Label(input_frame,
                              text="Sommet puits (3):",
                              font=('Arial', 12 ,'bold'),
                              bg='#f0f0f0',
                              fg='#008000')
        label_sink.grid(row=2, column=0, padx=10, pady=5)

        self.entry_sink = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_sink.grid(row=2, column=1, padx=10, pady=5)

        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=lambda: run_ford_fulkerson(self.entry_n, self.entry_source, self.entry_sink, self.graph_frame, self.info_frame))
        execute_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.graph_frame = tk.Frame(self.ford_fulkerson_window, bg='#f0f0f0')
        self.graph_frame.pack(expand=True, fill='both', padx=20, pady=10)

        self.info_frame = tk.Frame(self.ford_fulkerson_window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)
        
    def open_potentiel_metra_page(self):
        self.potentiel_metra_window = tk.Toplevel(self.root)
        self.potentiel_metra_window.title("Potentiel Metra")
        self.potentiel_metra_window.geometry("600x500")
        self.potentiel_metra_window.configure(bg='#f0f0f0')

        self.center_window(self.potentiel_metra_window, 600, 500)

        input_frame = tk.Frame(self.potentiel_metra_window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_tasks = tk.Label(input_frame,
                               text="Nombre de tâches :",
                               font=('Arial', 12 ,'bold'),
                               bg='#f0f0f0',
                               fg='#008000')
        label_tasks.grid(row=0, column=0, padx=10, pady=5)

        self.entry_tasks = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_tasks.grid(row=0, column=1, padx=10, pady=5)

        execute_btn = tk.Button(input_frame,
                                text="Exécuter",
                                font=('Arial', 12),
                                bg='#008000',
                                fg='white',
                                relief='flat',
                                command=lambda: run_potentiel_metra(self.entry_tasks, self.info_frame))
        execute_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.info_frame = tk.Label(self.potentiel_metra_window, text="", font=('Arial', 12), bg='#f0f0f0', fg='black')
        self.info_frame.pack(pady=10)
    
    def open_stepping_stone(self):
        self.stepping_stone_window = tk.Toplevel(self.root)
        self.stepping_stone_window.title("Stepping Stone")
        self.stepping_stone_window.geometry("600x500")
        self.stepping_stone_window.configure(bg='#f0f0f0')

        self.center_window(self.stepping_stone_window, 600, 500)

    # Cadre principal avec barre de défilement
        main_frame = tk.Frame(self.stepping_stone_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

    # Canvas pour la barre de défilement
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        canvas.pack(side='left', fill='both', expand=True)

    # Barre de défilement verticale
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

    # Configurer le canvas pour la barre de défilement
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Cadre intérieur pour le contenu
        inner_frame = tk.Frame(canvas, bg='#f0f0f0')
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Cadre pour les entrées
        input_frame = tk.Frame(inner_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)

        label_factories = tk.Label(input_frame,
                               text="Nombre d'usines :",
                               font=('Arial', 12 ,'bold'),
                               bg='#f0f0f0',
                               fg='#008000')
        label_factories.grid(row=0, column=0, padx=10, pady=5)

        self.entry_factories = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_factories.grid(row=0, column=1, padx=10, pady=5)

        label_clients = tk.Label(input_frame,
                             text="Nombre de clients :",
                             font=('Arial', 12 ,'bold'),
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

    # Cadre pour afficher les résultats
        self.info_frame = tk.Frame(inner_frame, bg='#f0f0f0')
        self.info_frame.pack(fill='both', expand=True, pady=10)

    # Configurer le canvas pour mettre à jour la zone de défilement
        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
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
        

    
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AlgorithmGUI()
    app.run()