## How Much D-de-dedotat-tated wam do you need for a minecraft servwer?

[Let's find out...](https://www.youtube.com/watch?v=LP0HYIkHs2Q&ab_channel=CyberKross)

## Versions:

Minecraft: v1.20.4
Forge: v1.20.4-forge-49.0.19

## Script Dependencies:

[Python 3.X+](https://www.python.org/downloads/)
[Colorama](https://pypi.org/project/colorama/) (_Just run `pip install colorama`_)
[GitPython](https://pypi.org/project/GitPython/) (_Just run `pip install GitPython`_)

## Scripts:

`move_mods.py`: This script will automatically move mods from this repository's `/mods` folder into the correct location on your computer. Don't remember the correct path to where mods go? No worries. Me either. The script will always remember, though.

`server_update_service.py`: This script is only to be used on the minecraft server machine. This script assumes `main` is checked out. Once here, the script will check if the server's current commit hash is different than `main`'s commit hash. If different, the script will perform a `git pull` and use the `move_mods` script to update the server automatically. Once updated, the server will be restarted. If no new changes, the service will wait **30 minutes** before trying again.
