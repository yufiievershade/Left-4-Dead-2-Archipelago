# Left 4 Dead 2 Archipelago WIP

The Current Build is expected to have many bugs. Just in case I don't get the things I want down with traps, how weapons spawn, etc. Know that I probably know if a trap doesn't send at the moment. Weapon spawns are also high priority right now. They work, but can be varied with how they decide to spawn. Everything else should work(in theory). I've done thorough testing with each build with friends. More will be done before I feel satisfied with the state of the apworld. For now, opening it up to more eyes is giving me more access to potential problems that I might not know about.

Finally, I recommend testing it by itself without other games until Filler is added. Most of the filler right now is just duplicates of guns. It might not generate with other games because of the limited item amount

# Installing Left 4 Dead 2 Archipelago

Please have the latest build of sourcemod and metamod installed for Left 4 Dead 2.
You can find them here: (Also, don't know if linux works, so try and let me know how that goes. I don't use linux myself)

Sourcemod: https://www.sourcemod.net/downloads.php?branch=stable (Grab the latest windows build.)

Metamod: https://www.sourcemm.net/downloads.php?branch=stable

Zombie Spawn(for traps): https://forums.alliedmods.net/showthread.php?p=2745733 

Left4dHooks(also for traps.): https://forums.alliedmods.net/showthread.php?t=321696 

# All things related to traps are not currently implemented fully. So for now, skip the steps with Zombie Spawn and Left4dhooks.

After you have installed Sourcemod and Metamod into your Left 4 Dead 2 installation, be sure to download everything from the releases page and sort them into the following locations.
1. All sp files go into your SteamLibrary\steamapps\common\Left 4 Dead 2\left4dead2\addons\sourcemod\scripting folder

2. All smx files go into your SteamLibrary\steamapps\common\Left 4 Dead 2\left4dead2\addons\sourcemod\plugins folder

3. The Archipelago folder goes into your SteamLibrary\steamapps\common\Left 4 Dead 2\left4dead2\addons\sourcemod\data folder

4. The json file goes into your SteamLibrary\steamapps\common\Left 4 Dead 2\left4dead2\addons\sourcemod\data folder

5. The apworld goes into your custom apworlds inside of your archipelago installation.

6. The Vpk file goes here SteamLibrary\steamapps\common\Left 4 Dead 2\left4dead2\addons 

7. Your Zombie Spawner is a smx file, so it goes to the same place as your other smx files.

8. Your Left4dhooks zip contains a sourcemod folder inside of it. Drag and drop this folder into your addons folder and it will just overwrite your sourcemod folder with the new files only) 

9. Finally, you can put your client file wherever. Just make sure you know your slot name and your archipelago.gg:(numbers) before you use it.

# For testing the Public Build, be aware that you are required to play in the Archipelago mutation, otherwise, scripts will not run and you will be playing Vanilla. Not only this, but be sure to run your launch options on -insecure if you want to test this






