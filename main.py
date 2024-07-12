#PSL Modules

#exeternal module
import customtkinter

#Costum module
import app

# Main Function (entry-point)
def main():

    #application new instance
    new_app_instance = app.Application()

    new_app_instance.launch_app()
    new_app_instance.display_menu()

# Main Guard
if __name__ == "__main__":
    main()