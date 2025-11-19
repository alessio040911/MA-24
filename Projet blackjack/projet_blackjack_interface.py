import tkinter as tk
import random

# ---------------------------
# Logique des cartes
# ---------------------------
class Carte:
    couleurs = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}
    valeurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, rang, couleur):
        self.rang = rang
        self.couleur = couleur

    @property
    def valeur(self):
        if self.rang in ["J", "Q", "K"]:
            return 10
        if self.rang == "A":
            return 11
        return int(self.rang)


class Paquet:
    def __init__(self):
        self.cartes = [Carte(r, c) for c in ["♠", "♥", "♦", "♣"] for r in Carte.valeurs]
        random.shuffle(self.cartes)

    def tirer(self):
        if not self.cartes:
            self.__init__()
        return self.cartes.pop()


class Main:
    def __init__(self):
        self.cartes = []

    def ajouter(self, carte):
        self.cartes.append(carte)

    def valeur(self):
        total = sum(c.valeur for c in self.cartes)
        nb_as = sum(1 for c in self.cartes if c.rang == "A")
        while total > 21 and nb_as > 0:
            total -= 10
            nb_as -= 1
        return total


# ---------------------------
# Tkinter : interface et jeu
# ---------------------------
class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack 🃏 - Mode local & mise")
        self.root.configure(bg="darkgreen")

        # Mode de jeu : 1 joueur ou local
        self.mode_local = tk.BooleanVar(value=False)

        # Variables de mise et argent
        self.argent = 500
        self.mise = 50

        # Paquet et mains
        self.paquet = Paquet()
        self.joueur1 = Main()
        self.joueur2 = Main()
        self.croupier = Main()

        # Gestion du tour
        self.tour = 1  # 1 = joueur1, 2 = joueur2, 3 = croupier

        # Titre
        tk.Label(root, text="Blackjack 🃏", font=("Arial", 26, "bold"), bg="darkgreen", fg="white").pack(pady=10)

        # Frames
        self.dealer_frame = tk.Frame(root, bg="darkgreen")
        self.dealer_frame.pack(pady=10)
        self.player_frame = tk.Frame(root, bg="darkgreen")
        self.player_frame.pack(pady=10)

        # Info
        self.info_label = tk.Label(root, text="", bg="darkgreen", fg="yellow", font=("Arial", 18, "bold"))
        self.info_label.pack(pady=10)

        # Zone mise et mode
        self.options_frame = tk.Frame(root, bg="darkgreen")
        self.options_frame.pack(pady=5)

        tk.Label(self.options_frame, text="💰 Mise :", bg="darkgreen", fg="white", font=("Arial", 14)).grid(row=0, column=0)
        self.mise_entry = tk.Entry(self.options_frame, width=6, font=("Arial", 14))
        self.mise_entry.insert(0, "50")
        self.mise_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.options_frame, text=f"Argent : {self.argent}$", bg="darkgreen", fg="white", font=("Arial", 14),
                 name="moneylabel").grid(row=0, column=2, padx=20)

        tk.Checkbutton(self.options_frame, text="Mode local (2 joueurs)", variable=self.mode_local, bg="darkgreen",
                       fg="white", font=("Arial", 14)).grid(row=0, column=3, padx=10)

        # Boutons
        self.button_frame = tk.Frame(root, bg="darkgreen")
        self.button_frame.pack(pady=15)
        tk.Button(self.button_frame, text="Tirer", command=self.hit, width=12, height=2,
                  font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(self.button_frame, text="Rester", command=self.stand, width=12, height=2,
                  font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
        tk.Button(self.button_frame, text="Rejouer", command=self.play_again, width=12, height=2,
                  font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)

        self.play_again()

    # Dessin d'une carte
    def dessiner_carte(self, frame, carte):
        card_frame = tk.Frame(frame, width=100, height=150, bg="white", bd=3, relief="raised")
        card_frame.pack(side="left", padx=8)
        card_frame.pack_propagate(False)
        couleur = Carte.couleurs[carte.couleur]
        tk.Label(card_frame, text=carte.rang, fg=couleur, bg="white", font=("Arial", 18, "bold")).pack(anchor="nw")
        tk.Label(card_frame, text=carte.couleur, fg=couleur, bg="white", font=("Arial", 32)).pack(expand=True)
        tk.Label(card_frame, text=carte.rang, fg=couleur, bg="white", font=("Arial", 18, "bold")).pack(anchor="se")

    def update_display(self, hide_dealer_card=True):
        for w in self.dealer_frame.winfo_children():
            w.destroy()
        for w in self.player_frame.winfo_children():
            w.destroy()

        # Croupier
        for i, c in enumerate(self.croupier.cartes):
            if i == 1 and hide_dealer_card and self.tour != 3:
                back = tk.Frame(self.dealer_frame, width=100, height=150, bg="blue", bd=3, relief="raised")
                back.pack(side="left", padx=8)
            else:
                self.dessiner_carte(self.dealer_frame, c)

        # Joueur actuel
        joueur = self.joueur1 if self.tour == 1 else self.joueur2
        for c in joueur.cartes:
            self.dessiner_carte(self.player_frame, c)

        txt = f"Tour : Joueur {self.tour}" if self.mode_local.get() else "Votre main"
        txt += f" | Valeur : {joueur.valeur()}"
        if joueur.valeur() > 21:
            txt += " (Dépasse 21 😢)"
        self.info_label.config(text=txt)

    def hit(self):
        joueur = self.joueur1 if self.tour == 1 else self.joueur2
        joueur.ajouter(self.paquet.tirer())
        self.update_display()
        if joueur.valeur() > 21:
            self.stand()

    def stand(self):
        if self.mode_local.get():
            if self.tour == 1:
                self.tour = 2
                self.update_display()
                self.info_label.config(text="🎮 Joueur 2, à toi de jouer !")
            elif self.tour == 2:
                self.tour = 3
                self.jouer_croupier()
        else:
            self.tour = 3
            self.jouer_croupier()

    def jouer_croupier(self):
        while self.croupier.valeur() < 17:
            self.croupier.ajouter(self.paquet.tirer())
        self.fin_tour()

    def fin_tour(self):
        self.update_display(hide_dealer_card=False)
        if not self.mode_local.get():
            pv = self.joueur1.valeur()
            dv = self.croupier.valeur()
            if pv > 21:
                result = "Perdu 😢"
                self.argent -= self.mise
            elif dv > 21 or pv > dv:
                result = "Gagné 🎉"
                self.argent += self.mise
            elif dv == pv:
                result = "Égalité 🤝"
            else:
                result = "Perdu 😢"
                self.argent -= self.mise
            self.info_label.config(text=f"{result} ({pv} vs {dv})")
        else:
            p1 = self.joueur1.valeur()
            p2 = self.joueur2.valeur()
            self.info_label.config(text=f"Résultats : J1={p1}, J2={p2}")
        self.update_money()

    def update_money(self):
        money_label = self.options_frame.nametowidget("moneylabel")
        money_label.config(text=f"Argent : {self.argent}$")

    def play_again(self):
        try:
            self.mise = int(self.mise_entry.get())
        except ValueError:
            self.mise = 50
        if self.mise <= 0:
            self.mise = 50
        if self.mise > self.argent:
            self.mise = self.argent
            self.mise_entry.delete(0, tk.END)
            self.mise_entry.insert(0, str(self.argent))

        self.paquet = Paquet()
        self.joueur1 = Main()
        self.joueur2 = Main()
        self.croupier = Main()

        self.tour = 1

        self.joueur1.ajouter(self.paquet.tirer())
        self.joueur1.ajouter(self.paquet.tirer())
        self.croupier.ajouter(self.paquet.tirer())
        self.croupier.ajouter(self.paquet.tirer())

        self.update_display()


# ---------------------------
# Lancement
# ---------------------------
root = tk.Tk()
app = BlackjackApp(root)
root.mainloop()
