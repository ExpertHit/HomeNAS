from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import subprocess
import os
import sys
import requests
import psutil

# Variables Globales

ip_address = ""
i = 0
file_dir = os.path.dirname(__file__)


# Fonctions -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 

# Fonctions pour le panneau latéral et l'interface principale ***

def affichage_tableau_de_bord():
    cadre_2.pack_forget()
    cadre_1.pack(anchor=NW)
    
def affichage_page_des_fichiers():
    cadre_1.pack_forget()
    cadre_2.pack(anchor=NW)

# Fonctions pour le tableau de bord ***

def demarrage_serveur_nas():
    python_executable = sys.executable
    backend_script = os.path.join(file_dir, "BackEnd_HomeNAS.py")
    subprocess.Popen([python_executable, backend_script])

def affichage_remplissage_ip():
    global ip_address
    global i
    ip = simpledialog.askstring("Adresse IP", "Entrez l'adresse IP du serveur NAS :")
    if ip:
        ip_address = ip
        creation_cadre_ip(ip,0, i)
        messagebox.showinfo("Adresse IP", f"L'adresse IP saisie est : {ip}")
        i = i + 1
    else:
        messagebox.showwarning("Adresse IP", "Aucune adresse IP saisie")

def creation_cadre_ip(ip, start_row, start_column, nas_status=False):
    global selected_var
    
    ip_cadre = Frame(
        ip_conteneur,
        width=200,
        height=180,
        bg="#4B4949",
        bd=1
    )
    ip_cadre.pack_propagate(0)  # Empêche le cadre de redimensionner son contenu
    ip_cadre.grid(row=start_row, column=start_column, pady=20, padx=10) # Crée un cadre contenant l'adresse IP spécifiée

    ip_label = Label(ip_cadre, text=f"Serveur NAS : {ip}", bg="#4B4949", fg="white") # Texte indiquant l'adresse IP
    ip_label.pack(pady=10, anchor="center")

    statut_cadre = Frame(ip_cadre, bg="#4B4949")  # Création d'une sous-frame pour le statut et la case à cocher
    statut_cadre.pack(pady=10)

    statut_couleur = "#089016" if nas_status else "#FF0000"
    statut_point = Label(statut_cadre, text="   ", bg=statut_couleur) # Point vert ou rouge indiquant l'état du NAS
    statut_point.pack(side=LEFT, padx=10)

    statut_label = Label(statut_cadre, text="En ligne" if nas_status else "Hors ligne", bg="#4B4949", fg="white") # Texte indiquant l'état du NAS
    statut_label.pack(side=LEFT)

    verfi_var = BooleanVar()
    case_connexion = Checkbutton(ip_cadre, text="Connecté", variable=verfi_var, bg="#4B4949", fg="white",
                         selectcolor="#089016", activebackground="#089016", activeforeground="white") # Création de la case à cocher
    case_connexion.pack(anchor="center", pady=10)

    
    supprimer_bouton = Button(ip_cadre, text="Supprimer", command=lambda: supprimer_ip_cadre(ip_cadre), bg="#089016", relief="flat",
    fg="white") 
    supprimer_bouton.pack(anchor="center", pady=10) # Ajouter un bouton de suppression à la sous-frame status_frame

    def si_verfi_change():
        global ip_address
        if ip_cadre.cget("bg") != "red":
            if verfi_var.get():
                ip_address = ip
                print("Case cochée - IP mise à jour :", ip_address)
                for ip_cadre_donnees in ip_cadres_totals: # Décocher tous les autres check boutons
                    if ip_cadre_donnees["ip_frame"] is not ip_cadre:
                        ip_cadre_donnees["check_var"].set(False)

    verfi_var.trace("w", lambda *args: si_verfi_change())

    ip_cadre_donnees = {
        "ip_frame": ip_cadre,
        "check_var": verfi_var
    }
    ip_cadres_totals.append(ip_cadre_donnees) # Ajouter les références aux éléments de la ip_frame dans une liste

# Fonction pour supprimer une ip_frame
def supprimer_ip_cadre(ip_cadre):
    ip_cadre.destroy()
    for ip_cadre_donnees in ip_cadres_totals: # Supprimer l'ip_frame de la liste ip_frames
        if ip_cadre_donnees["ip_frame"] is ip_cadre:
            ip_cadres_totals.remove(ip_cadre_donnees)
            break

# Fonctions pour la page des fichiers ***

# Fonction interne pour parcourir et téléverser un fichier
def parcourir_pour_envoi():
    def interne_parcourir_pour_envoi():
        fichier_chemin = filedialog.askopenfilename()
        if fichier_chemin:
            fichiers = {'file': open(fichier_chemin, 'rb')}
            url = f"http://{ip_address}:8000/upload"  # Utilisez ip_address dans l'URL
            response = requests.post(url, files=fichiers)
            if response.status_code == 200:
                print("Fichier téléversé avec succès")
            else:
                print("Erreur lors du téléversement du fichier")

    return interne_parcourir_pour_envoi

def obtenir_fichiers_du_nas():
    url = f"http://{ip_address}:8000/files"  # URL de votre endpoint dans le backend Flask
    response = requests.get(url)
    
    if response.status_code == 200:
        fichiers = response.json()
        vider_liste_fichier()
        for fichier in fichiers:
            creation_cadre_fichier(fichier)
    else:
        vider_liste_fichier()
        fichier_cadre = Frame(fichier_liste, bg="#4B4949", bd=1)
        fichier_cadre.pack(fill=X)
        file_label = Label(fichier_cadre, text="Erreur lors de la récupération des fichiers du NAS", bg="#4B4949", fg="white")
        file_label.pack(pady=5)

def creation_cadre_fichier(file):
    fichier_cadre = Frame(fichier_liste, bg="#4B4949", bd=1, pady=10, padx=100)
    fichier_cadre.pack(fill=X)
    fichier_label = Label(fichier_cadre, text=file, bg="#4B4949", fg="white", highlightbackground="#089016")
    fichier_label.pack(side=LEFT, pady=5)
    fichier_bouton = Button(fichier_cadre, text="Télécharger", bg="#089016", fg="white", bd=0, relief="flat")
    fichier_bouton.pack(side=RIGHT, pady=5, padx=(20, 0))
    fichier_cadre.file_label = fichier_label  # Ajouter une référence au label dans la frame
    fichier_cadre.bind("<Button-1>", si_fichier_cadre_clic)

def vider_liste_fichier():
    for widget in fichier_liste.winfo_children():
        widget.destroy()

def si_fichier_cadre_clic(event):
    fichier_cadre = event.widget
    if fichier_cadre.cget("bg") == "#089016":
        fichier_cadre.config(bg="#4B4949")  # Réinitialiser la couleur de fond
    else:
        fichier_cadre.config(bg="#089016")  # Mettre en évidence la frame sélectionnée

# Fonctions pour le test *

def bouton_clic():
    print("Button Clicked")

def fermer_port():
    for proc in psutil.process_iter():
        try:
            for conn in proc.connections():
                if conn.laddr.port == 8000:
                    proc.kill()
                    print("Port fermé avec succès")
                    return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("Erreur lors de la fermeture du port")

def fermeture_app():
    subprocess.run(["lsof", "-ti", ":8000", "-sTCP:LISTEN", "-n", "-P", "-Fp"]) # Fermer le processus utilisant le port 8000

def on_closing():
    fermeture_app() # Appelé lorsque la fenêtre est fermée
    window.destroy()


# Interface -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Interface principale ***

window = Tk() # Création de la fenêtre
window.title("HomeNas")
window.geometry("1000x600")
window.configure(bg="#403c3c")

cadre_1 = Frame(window, bg="#403c3c",padx=200, pady=70)
cadre_1.place()
cadre_1.pack(anchor=NW)

cadre_2 = Frame(window, bg="#403c3c",padx=200, pady=70)

barre_lateral = Canvas(
    window,
    bg="#4B4949",
    width=183,
    height=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
barre_lateral.place(x=0, y=0) # Création du fond de la barre latéral


barre_superieur = Canvas(
    window,
    bg="#089016",
    width=3000,
    height=49,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
barre_superieur.place(x=0, y=0) # Création du fond de la barre en haut de la page

tableau_label = Label(window, bg="#403c3c")
tableau_label.place(x=-2, y=170)

Bouton_tableau_chemin = os.path.join(file_dir, "Bouton_tableau.png")
Bouton_tableau_img = PhotoImage(file=Bouton_tableau_chemin)
Bouton_tableau = Button(
    tableau_label,
    image=Bouton_tableau_img,
    borderwidth=0,
    highlightthickness=0,
    command=affichage_tableau_de_bord,
    relief="flat"
)
Bouton_tableau.pack(padx=0, pady=0)

page_fichiers_label = Label(window, bg="#403c3c")
page_fichiers_label.place(x=-2, y=230)

Bouton_fichiers_chemin = os.path.join(file_dir, "Bouton_fichiers.png")
Bouton_fichiers_img = PhotoImage(file=Bouton_fichiers_chemin)
Bouton_fichiers = Button(
    page_fichiers_label,
    image=Bouton_fichiers_img,
    borderwidth=0,
    highlightthickness=0,
    command=affichage_page_des_fichiers,
    relief="flat"
)
Bouton_fichiers.pack(padx=0, pady=0)

parametres_label = Label(window, bg="#403c3c")
parametres_label.place(x=-2, y=290)

Bouton_parametres_chemin = os.path.join(file_dir, "Bouton_parametres.png")
Bouton_parametres_img = PhotoImage(file=Bouton_parametres_chemin)
Bouton_parametres = Button(
    parametres_label,
    image=Bouton_parametres_img,
    borderwidth=0,
    highlightthickness=0,
    command=bouton_clic,
    relief="flat"
)
Bouton_parametres.pack(padx=0, pady=0)

Bouton_rafraichir_chemin = os.path.join(file_dir, "bouton_rafraichir.png")
Bouton_rafraichir_img = PhotoImage(file=Bouton_rafraichir_chemin)
Bouton_rafraichir = Button(
    window,
    image=Bouton_rafraichir_img,
    borderwidth=0,
    highlightthickness=0,
    command=bouton_clic,
    relief="flat"
)
Bouton_rafraichir.place(x=950, y=5)


# Interface du tableau de bord ***

ip_cadres_totals = []

boutons_conteneur = Frame(cadre_1, bg="#403c3c") # Création d'un conteneur pour les boutons b0 et b1
boutons_conteneur.grid(row=0, column=0, sticky="ew")

ip_conteneur = Frame(cadre_1, bg="#403c3c") # Création d'un conteneur pour les IP frames
ip_conteneur.grid(row=1, column=0, sticky="n")


Bouton_demarrage_chemin = os.path.join(file_dir, "Bouton_demarrage.png")
Bouton_demarrage_img = PhotoImage(file=Bouton_demarrage_chemin)
Bouton_demarrage = Button(
    boutons_conteneur,
    image=Bouton_demarrage_img,
    borderwidth=0,
    highlightthickness=0,
    command=demarrage_serveur_nas,
    relief="flat"
)
Bouton_demarrage.grid(row=0, column=0, padx=10)

Bouton_connexion_nas_chemin = os.path.join(file_dir, "Bouton_connexion_nas.png")
Bouton_connexion_nas_img = PhotoImage(file=Bouton_connexion_nas_chemin)
Bouton_connexion_nas = Button(
    boutons_conteneur,
    image=Bouton_connexion_nas_img,
    borderwidth=0,
    highlightthickness=0,
    command=affichage_remplissage_ip,
    relief="flat"
)
Bouton_connexion_nas.grid(row=0, column=1, padx=10)


# Interface de la page des fichiers ***

fichiers_cadres_totals = []

scrollbar = Scrollbar(cadre_2)
scrollbar.pack(side=RIGHT, fill=Y)

fermeture_bouton = Button(cadre_2, text="Fermer le port", command=fermer_port) # Création du bouton pour fermer le port
fermeture_bouton.pack()

Bouton_envoi_fichier = Button(
    cadre_2,
    borderwidth=0,
    highlightthickness=0,
    command=parcourir_pour_envoi(),
    text="Envoyer un fichier dans le serveur NAS",
    width=100,
    height=2,
    bg="#089016",
    fg="white",
    relief="flat"
)
Bouton_envoi_fichier.pack(pady=5) # Création d'un bouton b6

fichier_liste = Listbox(cadre_2, bg="#403c3c", fg="white") # Création d'une zone de liste pour afficher les fichiers
fichier_liste.configure(width=100, height=20)

scrollbar.config(command=fichier_liste.yview)
fichier_liste.config(yscrollcommand=scrollbar.set)

fichier_liste.pack(pady=10, padx=20, fill=BOTH, expand=True) # Placement des éléments dans le cadre frame2
scrollbar.pack(side=RIGHT, fill=Y)

Bouton_actualiser = Button(cadre_2, text="Mettre à jour", command=obtenir_fichiers_du_nas) # Création d'un bouton pour mettre à jour la liste des fichiers
Bouton_actualiser.pack(pady=5)

# Lancement de l'interface ***

window.grid_rowconfigure(0, weight=1)  # Permet à la fenêtre de redimensionner le cadre des IP frames
window.grid_columnconfigure(0, weight=1)  # Permet à la fenêtre de redimensionner le cadre des IP frames
window.resizable(True, True)
window.mainloop() # Exécution de la boucle principale
