''' Application Main Class

'''

import sys
import os
import MOTUS

class Application:

    def __init__ (self):
        pass


    def launch_app (self):
        os.system('cls')
        print("Demarrage...")

    def display_menu (self):
        print("Menu principal \n1) Commencer une nouvelle partie ! \n2) Quitter le jeu")

        user_choice = input("")

        #Condition Or Switch case (Match Case)

        match(user_choice):
            case "1":
                new_app_instance = MOTUS.MotusGame()
                new_app_instance.mainloop()
            case "2":
                self.quit_app()
            case _:
                print("Veuillez faire un choix :")

    def app_new_adventure (self):
        pass
    def quit_app (self):
        sys.exit()