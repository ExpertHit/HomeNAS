from tkinter import *
import subprocess
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
# Création des boutons
import os
import sys
import requests
import tkinter as tk
import psutil
print(tk.TkVersion)

def close_port():
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

ip_address = ""
i = 0
file_dir = os.path.dirname(__file__)

def btn_clicked():
    print("Button Clicked")

def shutdown_app():
    # Fermer le processus utilisant le port 8000
    subprocess.run(["lsof", "-ti", ":8000", "-sTCP:LISTEN", "-n", "-P", "-Fp"]) 

def on_closing():
    # Appelé lorsque la fenêtre est fermée
    shutdown_app()
    window.destroy()

def start_nas_serv():
    python_executable = sys.executable
    backend_script = os.path.join(file_dir, "BackEnd_HomeNAS.py")
    subprocess.Popen([python_executable, backend_script])

def browse_for_upload():
    # Fonction interne pour parcourir et téléverser un fichier
    def inner_browse_for_upload():
        file_path = filedialog.askopenfilename()
        if file_path:
            files = {'file': open(file_path, 'rb')}
            url = f"http://{ip_address}:8000/upload"  # Utilisez ip_address dans l'URL
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print("Fichier téléversé avec succès")
            else:
                print("Erreur lors du téléversement du fichier")
    
    return inner_browse_for_upload


def show_ip_entry():
    global ip_address
    global i
    ip = simpledialog.askstring("Adresse IP", "Entrez l'adresse IP du serveur NAS :")
    if ip:
        ip_address = ip
        create_ip_frame(ip,0, i)
        messagebox.showinfo("Adresse IP", f"L'adresse IP saisie est : {ip}")
        i = i + 1
    else:
        messagebox.showwarning("Adresse IP", "Aucune adresse IP saisie")


def create_ip_frame(ip, start_row, start_column, nas_status=False):
    global selected_var
    
    # Crée un cadre contenant l'adresse IP spécifiée
    ip_frame = Frame(
        ip_container,
        width=200,
        height=180,
        bg="#4B4949",
        bd=1
    )
    ip_frame.pack_propagate(0)  # Empêche le cadre de redimensionner son contenu
    ip_frame.grid(row=start_row, column=start_column, pady=20, padx=10)

    # Texte indiquant l'adresse IP
    ip_label = Label(ip_frame, text=f"Serveur NAS : {ip}", bg="#4B4949", fg="white")
    ip_label.pack(pady=10, anchor="center")

    # Création d'une sous-frame pour le statut et la case à cocher
    status_frame = Frame(ip_frame, bg="#4B4949")
    status_frame.pack(pady=10)

    # Point vert ou rouge indiquant l'état du NAS
    status_color = "#089016" if nas_status else "#FF0000"
    status_point = Label(status_frame, text="   ", bg=status_color)
    status_point.pack(side=LEFT, padx=10)

    # Texte indiquant l'état du NAS
    status_label = Label(status_frame, text="En ligne" if nas_status else "Hors ligne", bg="#4B4949", fg="white")
    status_label.pack(side=LEFT)

    # Création de la case à cocher
    check_var = BooleanVar()
    switch = Checkbutton(ip_frame, text="Connecté", variable=check_var, bg="#4B4949", fg="white",
                         selectcolor="#089016", activebackground="#089016", activeforeground="white")
    switch.pack(anchor="center", pady=10)

    # Ajouter un bouton de suppression à la sous-frame status_frame
    delete_button = Button(ip_frame, text="Supprimer", command=lambda: delete_ip_frame(ip_frame), bg="#089016", relief="flat",
    fg="white")
    delete_button.pack(anchor="center", pady=10)

    def on_check_changed():
        global ip_address
        if ip_frame.cget("bg") != "red":
            if check_var.get():
                ip_address = ip
                print("Case cochée - IP mise à jour :", ip_address)
                # Décocher tous les autres check boutons
                for ip_frame_data in ip_frames:
                    if ip_frame_data["ip_frame"] is not ip_frame:
                        ip_frame_data["check_var"].set(False)
            else:
                ip_address = ""
                print("Case décochée")

    check_var.trace("w", lambda *args: on_check_changed())

    # Ajouter les références aux éléments de la ip_frame dans une liste
    ip_frame_data = {
        "ip_frame": ip_frame,
        "check_var": check_var
    }
    ip_frames.append(ip_frame_data)

# Fonction pour supprimer une ip_frame
def delete_ip_frame(ip_frame):
    ip_frame.destroy()
    # Supprimer l'ip_frame de la liste ip_frames
    for ip_frame_data in ip_frames:
        if ip_frame_data["ip_frame"] is ip_frame:
            ip_frames.remove(ip_frame_data)
            break

def show_frame1():
    frame2.pack_forget()
    frame1.pack(anchor=NW)
    
def show_frame2():
    frame1.pack_forget()
    frame2.pack(anchor=NW)

def get_files_from_nas():
    url = "http://localhost:8000/files"  # URL de votre endpoint dans le backend Flask
    response = requests.get(url)
    
    if response.status_code == 200:
        files = response.json()
        clear_file_list()
        for file in files:
            create_file_frame(file)
    else:
        clear_file_list()
        file_frame = Frame(file_list, bg="#4B4949", bd=1)
        file_frame.pack(fill=X)
        file_label = Label(file_frame, text="Erreur lors de la récupération des fichiers du NAS", bg="#4B4949", fg="white")
        file_label.pack(pady=5)

def clear_file_list():
    for widget in file_list.winfo_children():
        widget.destroy()

def on_file_frame_clicked(event):
    file_frame = event.widget
    if file_frame.cget("bg") == "#089016":
        file_frame.config(bg="#4B4949")  # Réinitialiser la couleur de fond
    else:
        file_frame.config(bg="#089016")  # Mettre en évidence la frame sélectionnée

def create_file_frame(file):
    file_frame = Frame(file_list, bg="#4B4949", bd=1, pady=10, padx=100)
    file_frame.pack(fill=X)
    file_label = Label(file_frame, text=file, bg="#4B4949", fg="white", highlightbackground="#089016")
    file_label.pack(side=LEFT, pady=5)
    file_button = Button(file_frame, text="Télécharger", bg="#089016", fg="white", bd=0, relief="flat")
    file_button.pack(side=RIGHT, pady=5, padx=(20, 0))
    file_frame.file_label = file_label  # Ajouter une référence au label dans la frame
    file_frame.bind("<Button-1>", on_file_frame_clicked)

# Création de la fenêtre
window = Tk()
window.title("HomeNas")
window.geometry("1000x600")
window.configure(bg="#403c3c")

# Création des frames pour les boutons b0 et b1
frame1 = Frame(window, bg="#403c3c",padx=200, pady=70)
frame1.place()
frame1.pack(anchor=NW)

frame2 = Frame(window, bg="#403c3c",padx=200, pady=70)

file_frames = []
ip_frames = []


# Création d'une zone de scroll pour la liste des fichiers
scrollbar = Scrollbar(frame2)
scrollbar.pack(side=RIGHT, fill=Y)

# Création d'un bouton pour mettre à jour la liste des fichiers
update_button = Button(frame2, text="Mettre à jour", command=get_files_from_nas)

# Création du bouton pour fermer le port
close_button = Button(frame2, text="Fermer le port", command=close_port)
close_button.pack()

# Création d'un bouton b6
b6 = Button(
    frame2,
    borderwidth=0,
    highlightthickness=0,
    command=browse_for_upload(),
    text="Envoyer un fichier dans le serveur NAS",
    width=100,
    height=2,
    bg="#089016",
    fg="white",
    relief="flat"
)

# Création d'une zone de liste pour afficher les fichiers
file_list = Listbox(frame2, bg="#403c3c", fg="white")
file_list.configure(width=100, height=20)

# Configuration de la barre de défilement
scrollbar.config(command=file_list.yview)
file_list.config(yscrollcommand=scrollbar.set)

# Placement des éléments dans le cadre frame2
b6.pack(pady=5)
file_list.pack(pady=10, padx=20, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Création d'un bouton pour mettre à jour la liste des fichiers
update_button = Button(frame2, text="Mettre à jour", command=get_files_from_nas)
update_button.pack(pady=5)

# Création du conteneur pour les boutons b0 et b1
buttons_container = Frame(frame1, bg="#403c3c")
buttons_container.grid(row=0, column=0, sticky="ew")

# Création du conteneur pour les IP frames
ip_container = Frame(frame1, bg="#403c3c")
ip_container.grid(row=1, column=0, sticky="n")

rectangle = Canvas(
    window,
    bg="#4B4949",
    width=183,
    height=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
rectangle.place(x=0, y=0)

# Création du rectangle en haut de la page
rectangle2 = Canvas(
    window,
    bg="#089016",
    width=3000,
    height=49,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
rectangle2.place(x=0, y=0)


# Chemin vers les fichiers d'image
img0_path = os.path.join(file_dir, "Bouton_demarrage.png")
img1_path = os.path.join(file_dir, "Bouton_connexion_nas.png")
img2_path = os.path.join(file_dir, "Bouton_tableau.png")
img3_path = os.path.join(file_dir, "Bouton_fichiers.png")
img4_path = os.path.join(file_dir, "Bouton_parametres.png")
img5_path = os.path.join(file_dir, "bouton_rafraichir.png")

img0 = PhotoImage(file=img0_path)
b0 = Button(
    buttons_container,
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=start_nas_serv,
    relief="flat"
)
b0.grid(row=0, column=0, padx=10)

img1 = PhotoImage(file=img1_path)
b1 = Button(
    buttons_container,
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=show_ip_entry,
    relief="flat"
)
b1.grid(row=0, column=1, padx=10)

# Création des Labels pour les boutons gauche
label_tableau = Label(window, bg="#403c3c")
label_tableau.place(x=-2, y=170)
label_fichiers = Label(window, bg="#403c3c")
label_fichiers.place(x=-2, y=230)
label_parametres = Label(window, bg="#403c3c")
label_parametres.place(x=-2, y=290)

img2 = PhotoImage(file=img2_path)
b2 = Button(
    label_tableau,
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=show_frame1,
    relief="flat"
)
b2.pack(padx=0, pady=0)

img3 = PhotoImage(file=img3_path)
b3 = Button(
    label_fichiers,
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=show_frame2,
    relief="flat"
)
b3.pack(padx=0, pady=0)

img4 = PhotoImage(file=img4_path)
b4 = Button(
    label_parametres,
    image=img4,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
b4.pack(padx=0, pady=0)

img5 = PhotoImage(file=img5_path)
b5 = Button(
    window,
    image=img5,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
b5.place(x=950, y=5)

# Exécution de la boucle principale
window.grid_rowconfigure(0, weight=1)  # Permet à la fenêtre de redimensionner le cadre des IP frames
window.grid_columnconfigure(0, weight=1)  # Permet à la fenêtre de redimensionner le cadre des IP frames
window.resizable(True, True)
window.mainloop()
