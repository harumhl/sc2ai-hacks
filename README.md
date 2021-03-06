# sc2ai-hacks
A StarCraft 2 AI which uses Google's pysc2 library to send commands to a StarCraft 2 client.

[An introduction to Starcraft 2 and Google's Bot Library.](https://deepmind.com/blog/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment/)

### Easy Install
Download and install the following binaries:

- [Anaconda](https://www.anaconda.com/download/) - an optimized python library with common science tools preinstalled
- [StarCraft 2](https://www.battle.net/download/getInstallerForGame?gameProgram=STARCRAFT_2) - a futuristic real time strategy game where players command armies in epic battles
* [Ladder 2017 Season 1](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season1.zip)
* [Ladder 2017 Season 2](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season2.zip)
* [Ladder 2017 Season 3](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season3.zip)
* [Melee](http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip)
* [Mini-games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip)

The map files are password protected with the password 'iagreetotheeula'.

*By typing in the password ‘iagreetotheeula’ you agree to be bound by the terms of the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)*


Install:
- Create a folder named "Maps" in your StarCraft 2 program files directory. Then, extract the map files into the Maps folder. Do not move them from their extracted folders. 
The default StarCraft program file directories are:
  * Windows: C:\Program Files (x86)\StarCraft II\
  * Mac: /Applications/StarCraft II/
- Open Anaconda Prompt, which is installed in `"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)"` by default for Windows
- Inside of Anaconda Prompt, type
 `pip install pysc2`

### Run
- Update StarCraft
- Enter `python -m pysc2.bin.agent --map Simple64` into Anaconda Prompt

### Additional Information

 [Googles SC Python Github](https://github.com/deepmind/pysc2)
 
 [Blizzard's API Github](https://github.com/Blizzard/s2client-proto)
