import os
import platform
from colorama import Fore, Style
import shutil

current_directory = os.getcwd()
mods_path = os.path.join(current_directory, "mods")

def print_color(string, color):
    color_code = getattr(Fore, color, Fore.RESET)
    reset_code = Style.RESET_ALL
    print(color_code + string + reset_code)


def copy_mod(mod_path):
    try:
        shutil.copy(mod_path, destination_path)
        print_color(f"\tSuccessfully copied {mod} to {destination_path} ✓", "GREEN")
    except Exception as e:
        print_color(f"Error: {e}", "RED")


def get_destination_path():
    # Get the default mods folder for Mac or Windows
    os_name = platform.system()
    if os_name == "Darwin":
        destination_path = os.path.expanduser("~\Library\Application Support\minecraft\mods")
    else:
        destination_path = os.path.expanduser("~\AppData\Roaming\.minecraft\mods")

    correct_path = False
    count = 0

    while(not correct_path):
        if count == 0:
            print_color(f"\n[WARNING]: Default mod location is {destination_path}","YELLOW")
        else:
            print_color(f"New mod location is {destination_path}", "YELLOW")
        
        # Prompt user to confirm if the current path is correct
        user_input = input(Fore.YELLOW + "Press 'Y' if this is correct or enter the correct path: " + Style.RESET_ALL)
        
        # If path is correct, return
        if user_input.upper() == 'Y':
            correct_path = True
            return destination_path
        
        # If path is incorrect, try again
        else:
            destination_path = os.path.expanduser(user_input)
            count += 1


if __name__ == "__main__":
    mods = os.listdir(mods_path)

    # List files in the mods folder
    print_color("Here's what's in this mods folder:", "GREEN")
    for mod in mods:
        print_color(f"\t • {mod}", "GREEN")

    destination_path = get_destination_path()

    # Prompt user to continue
    print_color(f"\n[WARNING]: This script will move the mods folder into {destination_path}", "YELLOW")
    user_input = input(Fore.YELLOW + "Press 'Y' to continue or any other key to abort: " + Style.RESET_ALL)

    # Exit the script if the user did not enter Y
    if user_input.upper() != 'Y':
        print_color("\nOperation aborted by user. Exiting...", "RED")
        exit()

    # 'Y' was pressed -- continue script
    print_color("\nStarting copying process...", "GREEN")
    for mod in mods:
        mod_path = os.path.join(mods_path, mod)
        copy_mod(mod_path)