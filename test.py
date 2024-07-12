import customtkinter as ctk
from tkinter import messagebox
import pygame
import os
import random
from collections import Counter

# Configuration de base de CustomTkinter
ctk.set_appearance_mode("System")  # Modes : "System" (par défaut), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Thèmes : "blue" (par défaut), "green", "dark-blue")

# Initialisation de pygame pour le son
pygame.mixer.init()

class MotusGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Jeu Motus")
        self.geometry("600x800")

        # Variables de jeu
        self.grid_size = 8
        self.words_list = ["EXAMPLE", "PYTHON", "CODING", "GAMING", "SCHOOL", "PLANET", "NATURE"]
        self.word_to_guess = random.choice(self.words_list)
        self.attempts = 0
        self.score = 0  # Initialisation du score
        print(self.word_to_guess)

        # Remplacez "C:/Chemin/Vers/Votre/Dossier/Audio" par votre chemin réel
        self.audio_folder = "C:/Users/terra/Desktop/Python"

        # Configuration de la police
        self.font = ("Helvetica", 20, "bold")
        self.text_color = "white"  # Définir la couleur du texte en blanc

        # Configuration de la grille
        self.grid = []
        self.create_grid()

        # Entrée utilisateur
        self.entry = ctk.CTkEntry(self, placeholder_text="Entrez un mot de 7 lettres", width=200, font=self.font, text_color=self.text_color)
        self.entry.grid(row=self.grid_size, column=0, columnspan=5, pady=20)
        self.entry.bind("<KeyRelease>", self.play_sound)  # Ajouter un binding pour jouer le son à chaque touche

        # Bouton de validation
        self.submit_button = ctk.CTkButton(self, text="Valider", command=self.validate_word, font=self.font, text_color=self.text_color)
        self.submit_button.grid(row=self.grid_size + 1, column=0, columnspan=7, pady=20)  # Ligne abaissée

        # Affichage du score
        self.score_label = ctk.CTkLabel(self, text=f"Score: {self.score}", font=self.font, text_color=self.text_color)
        self.score_label.grid(row=self.grid_size + 2, column=0, columnspan=7, pady=20)

        # Chargement des fichiers audio pour chaque action
        self.correct_sound = pygame.mixer.Sound(os.path.join(self.audio_folder, "ok.mp3"))
        self.incorrect_sound = pygame.mixer.Sound(os.path.join(self.audio_folder, "mauvais.mp3"))

        # Tracker pour les lettres trouvées dans les tentatives précédentes
        self.found_letters = set()

    def create_grid(self):
        for i in range(self.grid_size):
            row = []
            if i == 0:
                # Sélectionner aléatoirement certains indices pour afficher les lettres
                selected_indices = random.sample(range(len(self.word_to_guess)), k=3)  # Par exemple, afficher 3 lettres
                for j in range(len(self.word_to_guess)):
                    if j in selected_indices:
                        label_text = self.word_to_guess[j]
                    else:
                        label_text = ""
                    label = ctk.CTkLabel(self, text=label_text, width=40, height=40, corner_radius=8, fg_color="gray", font=self.font, text_color=self.text_color)
                    label.grid(row=i, column=j, padx=5, pady=5)
                    row.append(label)
            else:
                for j in range(len(self.word_to_guess)):
                    label = ctk.CTkLabel(self, text="", width=40, height=40, corner_radius=8, fg_color="gray", font=self.font, text_color=self.text_color)
                    label.grid(row=i, column=j, padx=5, pady=5)
                    row.append(label)
            self.grid.append(row)

    def play_sound(self, event):
        letter = event.char.upper()
        # Ici, vous pouvez ajouter la logique pour jouer un son à chaque touche si nécessaire

    def validate_word(self):
        guess = self.entry.get().upper()
        if len(guess) != len(self.word_to_guess):
            messagebox.showerror("Erreur", f"Le mot doit contenir {len(self.word_to_guess)} lettres.")
            return

        if self.attempts >= self.grid_size:
            messagebox.showinfo("Terminé", f"Vous avez utilisé toutes vos tentatives! La réponse correcte était: {self.word_to_guess}")
            self.show_correct_answer()  # Afficher la réponse correcte dans la ligne actuelle
            return

        word_counter = Counter(self.word_to_guess)
        guess_counter = Counter()
        
        for i, letter in enumerate(guess):
            if guess_counter[letter] < word_counter[letter]:
                if letter == self.word_to_guess[i]:
                    if letter not in self.found_letters:
                        self.grid[self.attempts][i].configure(text=letter, fg_color="green", text_color="white")
                        self.correct_sound.play()  # Jouer le son pour une lettre correcte
                        pygame.time.wait(500)  # Délai de 500 millisecondes (0.5 secondes)
                        guess_counter[letter] += 1
                        self.found_letters.add(letter)
                    else:
                        self.grid[self.attempts][i].configure(text=letter, fg_color="red", text_color="white")
                        self.incorrect_sound.play()  # Jouer le son pour une lettre incorrecte
                        pygame.time.wait(500)  # Délai de 500 millisecondes (0.5 secondes)
                elif letter in self.word_to_guess and letter not in self.found_letters:
                    self.grid[self.attempts][i].configure(text=letter, fg_color="yellow", text_color="white")
                    self.incorrect_sound.play()  # Jouer le son pour une lettre incorrecte
                    pygame.time.wait(500)  # Délai de 500 millisecondes (0.5 secondes)
                    guess_counter[letter] += 1
                else:
                    self.grid[self.attempts][i].configure(text=letter, fg_color="red", text_color="white")
                    self.incorrect_sound.play()  # Jouer le son pour une lettre incorrecte
                    pygame.time.wait(500)  # Délai de 500 millisecondes (0.5 secondes)
            else:
                self.grid[self.attempts][i].configure(text=letter, fg_color="red", text_color="white")
                self.incorrect_sound.play()  # Jouer le son pour une lettre incorrecte
                pygame.time.wait(500)  # Délai de 500 millisecondes (0.5 secondes)

        self.attempts += 1
        self.entry.delete(0, ctk.END)

        if guess == self.word_to_guess:
            self.score += 100  # Ajouter 100 points pour une réponse correcte
            self.score_label.configure(text=f"Score: {self.score}")  # Mettre à jour le label du score
            messagebox.showinfo("Gagné!", "Félicitations, vous avez trouvé le mot!")
            self.reset_game()

    def show_correct_answer(self):
        # Affiche la réponse correcte dans la ligne actuelle
        for i, letter in enumerate(self.word_to_guess):
            self.grid[self.attempts-1][i].configure(text=letter, fg_color="blue", text_color="white")

    def reset_game(self):
        self.word_to_guess = random.choice(self.words_list)  # Choisir un nouveau mot aléatoire
        self.attempts = 0
        self.grid = []
        self.found_letters = set()  # Réinitialiser les lettres trouvées
        self.create_grid()

if __name__ == "__main__":
    app = MotusGame()
    app.mainloop()
