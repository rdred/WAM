"""Move .jar files into the correct mod location."""
import sys
import os
import platform
import shutil
from colorama import Fore, Style

current_directory = os.getcwd()
mods_path = os.path.join(current_directory, "mods")


def print_color(string, color):
    """Determine the Fore.color and print the string in that color."""
    color_code = getattr(Fore, color, Fore.RESET)
    reset_code = Style.RESET_ALL
    print(color_code + string + reset_code)


def copy_mod(m, m_path, d_path):
    """Copy the mod from the repo directory to the specified directory"""
    try:
        shutil.copy(m_path, d_path)
        print_color(
            f"\tSuccessfully copied {m} to {d_path} ✓", "GREEN")
    except Exception as e:
        print_color(f"Error: {e}", "RED")


def get_destination_path():
    """Determine the default destination path from OS or allow user to enter their own"""
    os_name = platform.system()
    if os_name == "Darwin":
        destination_path = os.path.expanduser(
            "~/Library/Application Support/minecraft/mods")
    else:
        destination_path = os.path.expanduser(
            "~\AppData\Roaming\.minecraft\mods")

    correct_path = False
    count = 0

    while not correct_path:
        if count == 0:
            print_color(
                f"\n[WARNING]: Default mod location is {destination_path}", "YELLOW")
        else:
            print_color(f"New mod location is {destination_path}", "YELLOW")

        # Prompt user to confirm if the current path is correct
        path_input = input(
            Fore.YELLOW +
            "Press 'Y' if this is correct or enter the correct path: " +
            Style.RESET_ALL)

        # If path is correct, return
        if path_input.upper() == 'Y':
            correct_path = True
            return destination_path

        # If path is incorrect, try again
        else:
            destination_path = os.path.expanduser(path_input)
            count += 1


def cleanup_destination(mods_in_repo, destination_path):
    """Remove mods in the destination path that don't appear in the repo's mod folder"""
    mods_in_destination = os.listdir(destination_path)

    for mod in mods_in_destination:
        if mod not in mods_in_repo:
            mod_path = os.path.join(destination_path, mod)
            try:
                os.remove(mod_path)
                print_color(
                    f"\tRemoved {mod} from {destination_path} ✓", "RED")
            except Exception as e:
                print_color(f"Error removing {mod}: {e}", "RED")


if __name__ == "__main__":
    mods = os.listdir(mods_path)

    # List files in the mods folder
    print_color("Here's what's in this mods folder:", "GREEN")
    for mod in mods:
        print_color(f"\t • {mod}", "GREEN")

    destination_path = get_destination_path()

    # Prompt user to continue
    print_color(
        f"\n[WARNING]: This script will move the mods folder into {destination_path}", "YELLOW")
    user_input = input(
        Fore.YELLOW +
        "Press 'Y' to continue or any other key to abort: "
        + Style.RESET_ALL)

    # Exit the script if the user did not enter Y
    if user_input.upper() != 'Y':
        print_color("\nOperation aborted by user. Exiting...", "RED")
        sys.exit(0)

    # 'Y' was pressed -- continue script
    print_color("\nStarting copying process...", "GREEN")
    for mod in mods:
        mod_path = os.path.join(mods_path, mod)
        copy_mod(mod, mod_path, destination_path)

    # Clean up destination path
    cleanup_destination(mods, destination_path)
