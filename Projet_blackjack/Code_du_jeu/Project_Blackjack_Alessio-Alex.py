#Author: Alessio-Alex , CHATGPT-4
#Date: 05.01.2026
#Name : Project_Blackjack_Alessio-Alex.py
# Description: A complete Blackjack game with a launch window using Tkinter.

import tkinter as tk
import random
import os
import sys

# ------------------------------
# Launch Window
# ------------------------------
class LaunchWindow:
    def __init__(self, master):  
        self.master = master
        self.master.title("Bienvenue au Casino Blackjack")
        self.master.geometry("1024x768")
        self.master.configure(bg="#003300")

        title = tk.Label(master, text="🎰 Bienvenue au Casino Blackjack 🎰",
                         font=("Playfair Display", 40, "bold"), fg="#FFD700", bg="#003300")
        title.pack(pady=80)

        subtitle = tk.Label(master, text="Cliquez sur 'Lancer' pour commencer le jeu",
                            font=("Georgia", 24, "italic"), fg="#FFD700", bg="#003300")
        subtitle.pack(pady=10)

        launch_btn = tk.Button(master, text="Lancer", font=("Georgia", 20, "bold"),
                               bg="#d2232a", fg="white", activebackground="#ff4c51", activeforeground="white",
                               width=15, height=2, relief="raised", bd=5, cursor="hand2",
                               command=self.launch_game)
        launch_btn.pack(pady=30)

        quit_btn = tk.Button(master, text="Quitter", font=("Georgia", 20, "bold"),
                             bg="#555555", fg="white", activebackground="#777777", activeforeground="white",
                             width=10, height=2, relief="raised", bd=5, cursor="hand2",
                             command=self.master.destroy)
        quit_btn.pack(pady=10)

    def launch_game(self):
        self.master.destroy()
        root = tk.Tk()
        game = BlackjackGame(root)
        root.mainloop()

# ------------------------------
# Blackjack Game
# ------------------------------
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        root.title("Blackjack Édition Casino - Option 3 (Corrigé)")
        root.geometry("1024x768")
        root.configure(bg="#004225")  # Deep emerald green

        # Player money and betting
        self.balance = 1000
        self.current_bet = 100
        self.game_over = True  # True when no round in progress

        # Load cards
        self.deck = self.load_cards()
        self.card_deck = self.deck.copy()
        random.shuffle(self.card_deck)

        self.player_hand = []
        self.dealer_hand = []

        # Variables
        self.player_score_var = tk.StringVar(value="Score Joueur: 0")
        self.dealer_score_var = tk.StringVar(value="Score Croupier: ?")
        self.result_var = tk.StringVar(value="Placez votre mise pour commencer!")
        self.balance_var = tk.StringVar(value=f"Solde: {self.balance}$")
        self.bet_var = tk.StringVar(value=f"Mise Actuelle: {self.current_bet}$")

        # Load chip images (if missing, still works)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chip_folder = os.path.join(script_dir, "blackjack_cards", "chips")

        def safe_img(path):
            try:
                return tk.PhotoImage(file=path)
            except:
                return None

        self.chip_images = {
            50: safe_img(os.path.join(chip_folder, "chip_50.png")),
            100: safe_img(os.path.join(chip_folder, "chip_100.png")),
            500: safe_img(os.path.join(chip_folder, "chip_500.png")),
            -50: safe_img(os.path.join(chip_folder, "chip_neg_50.png")),
            -100: safe_img(os.path.join(chip_folder, "chip_neg_100.png")),
            -500: safe_img(os.path.join(chip_folder, "chip_neg_500.png")),
        }

        # Back card image
        try:
            self.back_img = tk.PhotoImage(file=os.path.join(script_dir, "blackjack_cards", "back.png"))
        except:
            self.back_img = None

        self.setup_ui()

    def load_cards(self):
        # Adjust ranks to match your folder naming convention where ace is '1'
        suits = ['club', 'diamond', 'heart', 'spade']
        ranks = ['1'] + [str(i) for i in range(2, 11)] + ['jack', 'queen', 'king']
        cards = []
        script_dir = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', False) else sys._MEIPASS

        for suit in suits:
            for rank in ranks:
                filename = os.path.join(script_dir, "blackjack_cards", f"{rank}_{suit}.png")
                try:
                    img = tk.PhotoImage(file=filename)
                except:
                    img = None
                if rank == '1':  # Ace
                    value = 11
                elif rank in ('jack', 'queen', 'king'):
                    value = 10
                else:
                    value = int(rank)
                cards.append({'rank': rank, 'value': value, 'image': img})
        return cards

    def deal_card(self):
        if len(self.card_deck) == 0:
            self.card_deck = self.deck.copy()
            random.shuffle(self.card_deck)
        return self.card_deck.pop(0)

    def calculate_score(self, hand):
        total = 0
        aces = 0
        for card in hand:
            total += card['value']
            if card['rank'] == '1':  # Ace
                aces += 1
        # Reduce aces from 11 to 1 as needed
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    # ------------------------------
    # UI Setup
    # ------------------------------
    def setup_ui(self):
        # Fonts
        self.title_font = ("Playfair Display", 24, "bold")
        self.score_font = ("Georgia", 18, "bold")
        self.result_font = ("Georgia", 20, "italic")
        self.button_font = ("Georgia", 14, "bold")

        # Result Label
        self.result_label = tk.Label(self.root, textvariable=self.result_var,
                                     font=self.result_font, fg="#ffd700", bg="#004225")
        self.result_label.pack(pady=12)

        # Dealer
        dealer_label = tk.Label(self.root, text="Croupier", font=self.score_font, fg="#ffe600", bg="#004225")
        dealer_label.pack()
        self.dealer_frame = tk.Frame(self.root, bg="#003315", bd=3, relief="ridge", width=360, height=160)
        self.dealer_frame.pack(pady=6)
        self.dealer_frame.pack_propagate(0)
        self.dealer_score_label = tk.Label(self.root, textvariable=self.dealer_score_var,
                                           font=self.score_font, fg="#ffd700", bg="#004225")
        self.dealer_score_label.pack()

        # Player
        player_label = tk.Label(self.root, text="Joueur", font=self.score_font, fg="#ffd700", bg="#004225")
        player_label.pack(pady=(10, 0))
        self.player_frame = tk.Frame(self.root, bg="#003315", bd=3, relief="ridge", width=360, height=160)
        self.player_frame.pack(pady=6)
        self.player_frame.pack_propagate(0)
        self.player_score_label = tk.Label(self.root, textvariable=self.player_score_var,
                                           font=self.score_font, fg="#ffd700", bg="#004225")
        self.player_score_label.pack()

        # Balance and Bet
        balance_frame = tk.Frame(self.root, bg="#004225")
        balance_frame.pack(pady=10)
        tk.Label(balance_frame, textvariable=self.balance_var, font=self.score_font, fg="#00FF00", bg="#004225").pack(side="left", padx=30)
        tk.Label(balance_frame, textvariable=self.bet_var, font=self.score_font, fg="#FFD700", bg="#004225").pack(side="left", padx=30)

        # Betting Chips
        chip_frame = tk.Frame(self.root, bg="#004225")
        chip_frame.pack(pady=12)

        bet_amounts = [50, 100, 500]
        for i, amt in enumerate(bet_amounts):
            img = self.chip_images.get(amt)
            if img:
                btn = tk.Button(chip_frame, image=img, command=lambda a=amt: self.change_bet(a), bd=0, cursor="hand2")
            else:
                btn = tk.Button(chip_frame, text=f"+{amt}$", command=lambda a=amt: self.change_bet(a), bd=0, cursor="hand2",
                                bg="#ffffff", fg="#000000", width=8)
            btn.grid(row=0, column=i, padx=10)
        for i, amt in enumerate(bet_amounts):
            img = self.chip_images.get(-amt)
            if img:
                btn = tk.Button(chip_frame, image=img, command=lambda a=-amt: self.change_bet(a), bd=0, cursor="hand2")
            else:
                btn = tk.Button(chip_frame, text=f"-{amt}$", command=lambda a=-amt: self.change_bet(a), bd=0, cursor="hand2",
                                bg="#ffffff", fg="#000000", width=8)
            btn.grid(row=1, column=i, padx=10, pady=6)

        # Game Buttons
        button_frame = tk.Frame(self.root, bg="#004225")
        button_frame.pack(pady=12)

        style_btn_opts = {"font": self.button_font, "width": 10, "bg": "#d2232a",
                          "fg": "white", "activebackground": "#ff4c51", "activeforeground": "white",
                          "bd": 4, "relief": "raised", "cursor": "hand2"}

        self.hit_button = tk.Button(button_frame, text="Tirer", command=self.player_hit, **style_btn_opts)
        self.hit_button.grid(row=0, column=0, padx=12)
        self.stand_button = tk.Button(button_frame, text="Rester", command=self.player_stand, **style_btn_opts)
        self.stand_button.grid(row=0, column=1, padx=12)
        self.new_game_button = tk.Button(button_frame, text="Nouvelle Partie", command=self.new_game, **style_btn_opts)
        self.new_game_button.grid(row=0, column=2, padx=12)
        quit_btn = tk.Button(button_frame, text="Quitter", command=self.root.destroy, **style_btn_opts)
        quit_btn.grid(row=0, column=3, padx=12)

        # Disable Hit/Stand until a bet is placed
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    # ------------------------------
    # Betting Functions
    # ------------------------------
    def change_bet(self, amount):
        # Prevent bet changes when a round is active
        if not self.game_over:
            self.result_var.set("Terminez la partie en cours avant de changer la mise.")
            return

        # Prevent negative total bet
        if self.current_bet + amount < 0:
            return
        if amount > 0 and self.current_bet + amount > self.balance:
            self.result_var.set("Vous ne pouvez pas miser plus que votre solde!")
            return

        self.current_bet += amount
        self.bet_var.set(f"Mise Actuelle: {self.current_bet}$")
        self.result_var.set("Mise mise à jour. Cliquez sur 'Nouvelle Partie' pour distribuer.")

    # ------------------------------
    # Card Display and Gameplay
    # ------------------------------
    def display_hand(self, frame, hand, hide_first=False):
        # Clear
        for widget in frame.winfo_children():
            widget.destroy()

        # Basic geometry values
        offset_x = 40  # horizontal offset between cards
        card_w = 72    # approximate card width used for centering (depends on images)
        hand_len = len(hand)
        total_width = offset_x * (hand_len - 1) + card_w if hand_len > 0 else card_w
        # ensure frame width at least as big as configured (frame is fixed width), we center within that
        frame_width = int(frame.cget('width'))
        start_x = max(8, (frame_width - total_width) // 2)

        for idx, card in enumerate(hand):
            x = start_x + idx * offset_x
            if idx == 0 and hide_first:
                if self.back_img:
                    label = tk.Label(frame, image=self.back_img, bd=2, relief="raised", bg="#003315")
                    label.image = self.back_img
                else:
                    label = tk.Label(frame, text="?", font=("Georgia", 20), fg="white", bg="#003315", width=4, height=6, relief="raised", bd=2)
                label.place(x=x, y=8)
            else:
                card_obj = hand[idx]
                if card_obj['image']:
                    label = tk.Label(frame, image=card_obj['image'], bd=2, relief="raised", bg="#003315")
                    label.image = card_obj['image']
                    label.place(x=x, y=8)
                else:
                    # Show human friendly rank if no image
                    rank_display = card_obj['rank']
                    if rank_display == '1':
                        text = "A"
                    elif rank_display in ('jack', 'queen', 'king'):
                        text = rank_display[0].upper()
                    else:
                        text = rank_display
                    label = tk.Label(frame, text=text, font=("Georgia", 20, "bold"), fg="white", bg="#003315", width=4, height=6, relief="raised", bd=2)
                    label.place(x=x, y=8)

    def update_scores_display(self, hide_dealer_card=True):
        player_score = self.calculate_score(self.player_hand)
        self.player_score_var.set(f"Score Joueur: {player_score}")
        if hide_dealer_card:
            self.dealer_score_var.set("Score Croupier: ?")
        else:
            dealer_score = self.calculate_score(self.dealer_hand)
            self.dealer_score_var.set(f"Score Croupier: {dealer_score}")

    # ------------------------------
    # Game Logic
    # ------------------------------
    def new_game(self):
        if self.current_bet == 0:
            self.result_var.set("Placez d'abord une mise!")
            return

        if not self.game_over:
            self.result_var.set("Partie en cours! Terminez-la d'abord.")
            return

        # Start a round
        self.game_over = False
        self.result_var.set("Distribution des cartes...")
        self.player_hand.clear()
        self.dealer_hand.clear()

        # Deal
        self.player_hand.append(self.deal_card())
        self.dealer_hand.append(self.deal_card())
        self.player_hand.append(self.deal_card())
        self.dealer_hand.append(self.deal_card())

        # Display
        self.display_hand(self.player_frame, self.player_hand)
        self.display_hand(self.dealer_frame, self.dealer_hand, hide_first=True)
        self.update_scores_display(hide_dealer_card=True)

        # Enable hit/stand and disable new_game & changing bet
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.DISABLED)

    def player_hit(self):
        if self.game_over:
            return
        self.player_hand.append(self.deal_card())
        self.display_hand(self.player_frame, self.player_hand)
        score = self.calculate_score(self.player_hand)
        self.player_score_var.set(f"Score Joueur: {score}")
        if score > 21:
            # Immediately resolve as bust
            self.player_stand()

    def player_stand(self):
        if self.game_over:
            return
        # Disable hit/stand to avoid double actions
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        # Reveal dealer card and play
        self.display_hand(self.dealer_frame, self.dealer_hand, hide_first=False)
        self.update_scores_display(hide_dealer_card=False)
        self.root.update()

        dealer_score = self.calculate_score(self.dealer_hand)
        while dealer_score < 17:
            self.dealer_hand.append(self.deal_card())
            self.display_hand(self.dealer_frame, self.dealer_hand, hide_first=False)
            dealer_score = self.calculate_score(self.dealer_hand)
            self.update_scores_display(hide_dealer_card=False)
            self.root.update()
            # short pause for realism
            self.root.after(600)

        player_score = self.calculate_score(self.player_hand)
        self.resolve_game(player_score, dealer_score)

    def resolve_game(self, player_score, dealer_score):
        # Mark round over and update balances, re-enable new_game button
        self.game_over = True
        if player_score > 21:
            self.result_var.set("Éliminé! Le croupier gagne!")
            self.balance -= self.current_bet
        elif dealer_score > 21:
            self.result_var.set("Le croupier est éliminé! Le joueur gagne!")
            self.balance += self.current_bet
        elif dealer_score > player_score:
            self.result_var.set("Le croupier gagne!")
            self.balance -= self.current_bet
        elif dealer_score < player_score:
            self.result_var.set("Le joueur gagne!")
            self.balance += self.current_bet
        else:
            self.result_var.set("Égalité! C'est un match nul!")

        # Update UI state
        self.balance_var.set(f"Solde: {self.balance}$")
        self.bet_var.set(f"Mise Actuelle: 0$")
        self.current_bet = 0

        # Re-enable New Game & disable Hit/Stand (already disabled)
        self.new_game_button.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

# ------------------------------
# Start App
# ------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = LaunchWindow(root)
    root.mainloop()