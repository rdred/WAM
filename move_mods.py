"""Move .jar files into the correct mod location."""
import sys
import os
import platform
import shutil
from datetime import datetime, timezone, timedelta
import git
from utils import print_color, input_color

current_directory = os.getcwd()
mods_path = os.path.join(current_directory, "mods")


def get_local_timestamp(timestamp):
    """Receives a timestamp and returns EST timestamp"""
    local_timezone = timezone(timedelta(hours=-5))
    timestamp_utc = datetime.utcfromtimestamp(timestamp)
    return timestamp_utc.replace(
        tzinfo=timezone.utc).astimezone(local_timezone)


def get_up_to_date():
    """Run git checkout [branch] && git fetch && git pull"""
    branch = "main"

    # Define the repo
    repo = git.Repo('.')
    origin = repo.remotes.origin
    origin.fetch()

    # Fetch current commit & origin commit details
    current_commit_hash = repo.head.commit.hexsha
    current_commit_timestamp = repo.head.commit.committed_date
    origin_commit_hash = repo.commit(branch).hexsha

    # Compare current commit to origin commit
    print_color("Checking for repo updates...", "YELLOW")
    if current_commit_hash != origin_commit_hash:
        # Show the user the current commit details
        print_color(f"You're currently on: {current_commit_hash}", "YELLOW")
        print_color(
            f"This was committed on: {get_local_timestamp(current_commit_timestamp)}\n", "YELLOW")

        # Checkout the branch
        print_color("Updating to latest...\n", "YELLOW")
        repo.git.checkout(branch)
        origin.pull()

        # Show the user the new current commit details
        current_commit_hash = repo.head.commit.hexsha
        current_commit_timestamp = repo.head.commit.committed_date
        print_color(f"You're now on: {current_commit_hash}", "GREEN")
        print_color(
            f"This was committed on: {get_local_timestamp(current_commit_timestamp)}\n", "GREEN")
    else:
        print_color("Your local repo is already up to date! ✓\n", "GREEN")


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

    # If the user passed an arg, use that arg path
    if len(sys.argv) > 1:
        destination_path = os.path.expanduser(sys.argv[1])
        return destination_path

    # If the user is on a Mac, use this path
    elif os_name == "Darwin":
        destination_path = os.path.expanduser(
            "~/Library/Application Support/minecraft/mods")

    # If the user is on Windows, use this path
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
        path_input = input_color(
            "Press 'Y' if this is correct or enter the correct path (Enter 1 for server path): ", "YELLOW")

        # If path is correct, return
        if path_input.upper() == 'Y':
            correct_path = True
            return destination_path
        elif path_input == '1':
            destination_path = os.path.expanduser(
                "~\Desktop\mcss_win-x86-64_v13.7.0\servers\WAM\mods")

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
    get_up_to_date()
    mods = os.listdir(mods_path)

    # List files in the mods folder
    print_color("Here's what's in this mods folder:", "GREEN")
    for mod in mods:
        print_color(f"\t • {mod}", "GREEN")

    destination_path = get_destination_path()

    # If passed a Y arg, skip the user input check
    if len(sys.argv) > 2 and sys.argv[2].upper() == 'Y':
        user_input = "Y"

    # Prompt the user to enter Y to confirm the changes
    else:
        print_color(
            f"\n[WARNING]: This script will move the mods folder into {destination_path}", "YELLOW")
        user_input = input_color(
            "Press 'Y' to continue or any other key to abort: ", "YELLOW")

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
