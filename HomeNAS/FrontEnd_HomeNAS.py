from tkinter import *
import subprocess
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import requests

ip_address = ""

def btn_clicked():
    print("Button Clicked")

def start_nas_serv():
    subprocess.Popen(["python", "BackEnd_HomeNAS.py"])

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
    ip = simpledialog.askstring("Adresse IP", "Entrez l'adresse IP du serveur NAS :")
    if ip:
        ip_address = ip
        create_ip_frame(ip)
        messagebox.showinfo("Adresse IP", f"L'adresse IP saisie est : {ip}")
    else:
        messagebox.showwarning("Adresse IP", "Aucune adresse IP saisie")


def create_ip_frame(ip, start_row=0, start_column=0):
    # Crée un cadre contenant l'adresse IP spécifiée
    ip_frame = Frame(
        ip_container,
        width=250,
        height=250,
        bg="#4B4949",
        bd=1
    )
    ip_frame.pack_propagate(0)  # Empêche le cadre de redimensionner son contenu
    ip_frame.grid(row=start_row, column=start_column, padx=(10, 30), pady=20)
    ip_label = Label(ip_frame, text=ip, bg="#4B4949", fg="white")
    ip_label.pack(pady=80)

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
window.geometry("1000x600")
window.configure(bg="#403c3c")

# Création des frames pour les boutons b0 et b1
frame1 = Frame(window, bg="#403c3c",padx=200, pady=70)
frame1.place()
frame1.pack(anchor=NW)

frame2 = Frame(window, bg="#403c3c",padx=200, pady=70)

file_frames = []

# Création d'une zone de scroll pour la liste des fichiers
scrollbar = Scrollbar(frame2)
scrollbar.pack(side=RIGHT, fill=Y)

# Création d'un bouton pour mettre à jour la liste des fichiers
update_button = Button(frame2, text="Mettre à jour", command=get_files_from_nas)

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

# Création du conteneur pour les IP frames
ip_container = Frame(window, bg="#403c3c")
ip_container.place(x=200, y=280)

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

# Création des boutons
img0 = PhotoImage(file="Bouton_demarrage.png")
b0 = Button(
    frame1,
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=start_nas_serv,
    relief="flat"
)
b0.grid(row=0,column=0,padx=10)

img1 = PhotoImage(file="Bouton_connexion_nas.png")
b1 = Button(
    frame1,
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=show_ip_entry,
    relief="flat"
)
b1.grid(row=0,column=1,padx=10)

# Création des Labels pour les boutons gauche
label_tableau = Label(window, bg="#403c3c")
label_tableau.place(x=-2, y=170)
label_fichiers = Label(window, bg="#403c3c")
label_fichiers.place(x=-2, y=230)
label_parametres = Label(window, bg="#403c3c")
label_parametres.place(x=-2, y=290)

img2 = PhotoImage(file="Bouton_tableau.png")
b2 = Button(
    label_tableau,
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=show_frame1,
    relief="flat"
)
b2.pack(padx=0, pady=0)

img3 = PhotoImage(file="Bouton_fichiers.png")
b3 = Button(
    label_fichiers,
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=show_frame2,  # Appel sans argument
    relief="flat"
)
b3.pack(padx=0, pady=0)

img4 = PhotoImage(file="Bouton_parametres.png")
b4 = Button(
    label_parametres,
    image=img4,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
b4.pack(padx=0, pady=0)

img5 = PhotoImage(file="bouton_rafraichir.png")
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
