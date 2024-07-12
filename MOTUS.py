#Import des librairies
import customtkinter as ctk
from tkinter import messagebox
import pygame
import os
import random

# Configuration de base de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Initialisation de pygame pour le son
pygame.mixer.init()

class MotusGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Paramètres de fenêtre
        self.title("Motus")
        self.geometry("700x800")

        #Initialisation des variables
        self.new_word()
        self.score = 0  #
        self.highscore = 0
        self.grid_size = 8 
        self.attempts = 0
        self.coefficient = 1
        
        # Configuration de la police
        self.font = ("Helvetica", 15, "bold")
        self.text_color = "white"
               
        # Dossier audio
        self.audio_folder = "C:/Users/terra/Desktop/Python"

        # Configuration de la grille
        self.grid = []
        self.create_grid()

        # Entrée utilisateur
        self.entry = ctk.CTkEntry(self, placeholder_text="Votre proposition", width=200)
        self.entry.grid(row=self.grid_size +1, column=23, columnspan=5, pady=20)

        # Bouton de validation
        self.submit_button = ctk.CTkButton(self, text="Valider", command=self.validate_word)
        self.submit_button.grid(row=self.grid_size +2, column=20, columnspan=5, pady=20)

        #Bouton de redémarrage
        self.reset_button = ctk.CTkButton(self, text="Recommencer", command=self.reset)
        self.reset_button.grid(row=self.grid_size +2, column=25, columnspan=5, pady=20)

        # Affichage du score
        self.score_label = ctk.CTkLabel(self, text=f"Score: {self.score}", font=self.font, text_color=self.text_color, fg_color="red")
        self.score_label.grid(row=self.grid_size +1, column=0, columnspan=5, pady=20)

        # Affichage du highscore
        self.highscore_label = ctk.CTkLabel(self, text=f"Score le plus élevé: {self.highscore}", font=self.font, text_color=self.text_color, fg_color="black")
        self.highscore_label.grid(row=self.grid_size -8, column=23, columnspan=5, pady=20)

        # Chargement des fichiers audio pour chaque action
        self.correct_sound = pygame.mixer.Sound(os.path.join(self.audio_folder, "ok.mp3"))
        self.incorrect_sound = pygame.mixer.Sound(os.path.join(self.audio_folder, "presque.mp3"))
        self.position_sound = pygame.mixer.Sound(os.path.join(self.audio_folder, "mauvais.mp3"))
    
    def create_grid(self):
            for i in range(self.grid_size):
                row = []
                if i == 0:
                    # Donne un indice de 3 lettres
                    selected_indices = random.sample(range(len(self.word_to_guess)), k=3)
                    for j in range(len(self.word_to_guess)):
                        if j in selected_indices:
                            label_text = self.word_to_guess[j]
                        else:
                            label_text = ""
                        label = ctk.CTkLabel(self, text=label_text, width=40, height=40, corner_radius=8, fg_color="blue", font=self.font, text_color=self.text_color)
                        label.grid(row=i+1, column=j+22, padx=5, pady=5)
                        row.append(label)
                else:
                    for j in range(len(self.word_to_guess)):
                        label = ctk.CTkLabel(self, text="", width=40, height=40, corner_radius=8, fg_color="blue", font=self.font, text_color=self.text_color)
                        label.grid(row=i+1, column=j+22, padx=5, pady=5)
                        row.append(label)
                self.grid.append(row)    
  
    # Variables de jeu : mots
    def new_word(self):
        self.words_list =["abeille", "accueil", "admiral", "alarmer", "amateur", "anagram", "baladin", "banquet", "bascule", "bataille", "besogne", "bouquet", "branche", "cabaret", "cahiers", "calibre", "caramel", "cascade", "catogan", "charbon", "chiffon", "colline", "cravate", "culture", "dentier", "dollars", "douleur", "drapier", "ecuries", "electre", "femelle", "fiancee", "fusible", "gambier", "garcon", "gommeux", "herbier", "houille", "jardin", "jonquille", "laitage", "laniere", "manege", "marotte", "memoire", "musique", "nectars", "nuancer", "offense", "pastels"]
        self.word_to_guess = random.choice(self.words_list).upper()
        print(self.word_to_guess)
    
    #Erreur longueur saisie
    def validate_word(self):
        guess = self.entry.get().upper()
        if len(guess) != len(self.word_to_guess):
            messagebox.showerror("Erreur", f"Le mot doit contenir {len(self.word_to_guess)} lettres.")          
            return
        
        #Position
        for i, letter in enumerate(guess):
            if letter == self.word_to_guess[i]:
                self.grid[self.attempts][i].configure(text=letter, fg_color="red", font=self.font, text_color="white")
                self.correct_sound.play()  # Jouer le son pour une lettre correcte
                pygame.time.wait(250)
            
            elif letter in self.word_to_guess:
                self.grid[self.attempts][i].configure(text=letter, fg_color="yellow", font=self.font, text_color="white")
                self.incorrect_sound.play()  # Jouer le son pour une lettre incorrecte
                pygame.time.wait(250)
                
            else:
                self.grid[self.attempts][i].configure(text=letter, fg_color="blue", font=self.font, text_color="white")
                self.position_sound.play()  # Jouer le son pour une lettre incorrecte
                pygame.time.wait(250)

        self.attempts += 1
        self.entry.delete(0, ctk.END)

        if guess == self.word_to_guess:
            messagebox.showinfo("Gagné!", "Félicitations, vous avez trouvé le mot!")
            pygame.mixer.music.load("trouve.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(2000)
            self.score += 100*self.coefficient  # Ajouter 100 points pour une réponse correcte
            self.score_label.configure(text=f"Score: {self.score}")  # Mettre à jour le label du score
            
            if self.score >= self.highscore:
                self.highscore = self.score
                self.highscore_label.configure(text=f"Score le plus élevé: {self.highscore}")  # Mettre à jour le label du score
            self.reset_game()
        elif guess != self.word_to_guess:
                self.coefficient = self.coefficient-0.10
                print(self.coefficient)
        if self.attempts == self.grid_size:
            pygame.time.wait(1000)
            pygame.mixer.music.load("fail.mp3")
            pygame.mixer.music.play()
            self.show_correct_answer()
            pygame.time.wait(2000)
            messagebox.showinfo("Terminé", f"Vous avez utilisé toutes vos tentatives! La réponse correcte était: {self.word_to_guess}")

            self.score_label.configure(text=f"Score: {self.score}")  # Mettre à jour le label du score
            self.reset()

    def show_correct_answer(self):
        # Affiche la réponse correcte dans la ligne actuelle
        for i, letter in enumerate(self.word_to_guess):
            self.grid[self.attempts-1][i].configure(text=letter, fg_color="red", text_color="white")
            
    def reset_game(self):
        self.attempts = 0
        self.grid = []
        self.new_word()
        self.create_grid()
        self.coefficient = 1
        
        
    def reset(self):
        self.coefficient = 1
        self.reset_game()
        self.score = 0  # Ajouter 100 points pour une réponse correcte
        self.score_label.configure(text=f"Score: {self.score}")  # Mettre à jour le label du score

if __name__ == "__main__":
    app = MotusGame()
    app.mainloop()