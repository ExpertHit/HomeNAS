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
    ip_frame = Frame(
        ip_container,
        width=250,
        height=250,
        bg="#4B4949",
        bd=1
    )
    ip_frame.grid(row=start_row, column=start_column, padx=(10, 30), pady=20)
    ip_label = Label(ip_frame, text=ip, bg="#4B4949", fg="white")
    ip_label.pack(pady=80)

# Création de la fenêtre
window = Tk()
window.geometry("1000x600")
window.configure(bg="#403c3c")

# Création du canvas pour le fond
canvas = Canvas(
    window,
    bg="#403c3c",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.pack()

# Chargement de l'image de fond
background_img = PhotoImage(file="background.png")
background = canvas.create_image(0, 0, anchor=NW, image=background_img)

# Création du conteneur pour les IP frames
ip_container = Frame(window, bg="#403c3c")
ip_container.place(x=200, y=280)

# Création des boutons
img0 = PhotoImage(file="Bouton_demarrage.png")
b0 = Button(
    window,
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=start_nas_serv,
    relief="flat"
)
b0.place(x=200, y=60)

img1 = PhotoImage(file="Bouton_connexion_nas.png")
b1 = Button(
    window,
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=show_ip_entry,
    relief="flat"
)
b1.place(x=420, y=60)

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
    command=btn_clicked,
    relief="flat"
)
b2.pack(padx=0, pady=0)

img3 = PhotoImage(file="Bouton_fichiers.png")
b3 = Button(
    label_fichiers,
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=browse_for_upload(),  # Appel sans argument
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
window.resizable(False, False)
window.mainloop()
