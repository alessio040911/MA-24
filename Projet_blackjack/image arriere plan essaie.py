from tkinter import *

# Création de la fenêtre principale
root = Tk()
root.title("Affichage d'une Image")
root.geometry("400x300")
# Chargement de l'image
photo = PhotoImage(file="test.png")
lbl = Label(root, image=photo)
lbl.pack()
root.mainloop()
