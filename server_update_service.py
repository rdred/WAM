"""Check github for new commits on main & apply them to the server"""
import subprocess
import time
import git


def git_fetch():
    """git fetch"""
    repo = git.Repo('.')
    origin = repo.remotes.origin
    origin.fetch()


def get_current_commit_hash():
    """git rev-parse HEAD"""
    repo = git.Repo('.')
    return repo.head.commit.hexsha


def git_pull():
    """git pull"""
    repo = git.Repo('.')
    origin = repo.remotes.origin
    origin.pull()


def run_move_mods_script():
    """Move mods into correct folder"""
    subprocess.run(['python', 'move_mods.py'])


def restart_server():
    """Restart the server"""
    # Replace this command with the actual command to restart your server
    subprocess.run(['your_restart_command_here'])


if __name__ == "__main__":
    while True:
        git_fetch()
        current_commit = get_current_commit_hash()

        main_commit = git.Repo('.').commit('main').hexsha

        if current_commit != main_commit:
            git_pull()
            run_move_mods_script()
            restart_server()

        time.sleep(1_800)  # Sleep for 30 minutes
