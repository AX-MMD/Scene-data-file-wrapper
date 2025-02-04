### INSTALLATION ##############################################################
___
Unzip the archive wherever you like, but make sure `/configs`, `/resources`, `/bin` and their content stays together.

### INTRO #####################################################################
___
Author: AX-MMD    
Docs: https://github.com/AX-MMD/kk-plap-generator/tree/main?tab=readme-ov-file#intro

PLAP generator uses a Timeline interpolable as reference to generate a sequence to use with sound components. It is meant to sync with a simple movement like forward-backward, up-down, etc. 

The process is as follows:
- Export the Timeline Single File of your reference
- Configure PLAP generator
- Generate your PLAP files
- Setup your scene (import `/resources/Plap1234.png` or make your own sound components)
- Import the generated PLAP files to Timeline

### EXPORT TIMELINE SINGLE FILE ###############################################
___
> In CharaStudio
* Choose an interpolable like "GO Pos Waist", Hips, Dick, etc. Rotation is fine too. 
* Rename it with an alias, can also just Rename -> ctrl+X -> ctrl+V. 
* Make sure the owner of that interpolable is selected (green) in your Workspace.
* Timeline -> Single Files -> Save.

> In PLAP generator
* Drop the exported file into the file drop zone or use the `Select File` button.

### CONFIGURATION #############################################################
___
There are only two required info for a default generation of a sequence: The name of the interpolable (or Path if part of a group) and the Time of a reference keyframe.

> In CharaStudio
* Choose a keyframe where the interpolable is fully extended:
  -- Dick pushed in the female.
  -- Female pushed on dick (if she's the one moving).
  -- It can be whatever is the apex/movement of your interpolable.
* Copy the exact Time of that interpolable.
* Copy the exact Name of that interpolable.

> In PLAP generator
* The generator needs the Path and Time of the interpolable to use as reference.

If the interpolable is part of a group, here is an exemple:

    Your interpolable "Pos Waist" is part of a group(s), and the reference keyframe is at 00:02.454
    __________
    |  Main    |
    ------------
    |   male   |      "00:02.454"
    ------------      ⇓
      |Pos Waist|    ◆◆◆ ◆◆◆ ◆◆◆       ◆◆ ◆◆ ◆◆◆◆◆◆
      ---------

    Path = Main.male.Pos Waist
    Time = 00:02.454

If the interpolable is not part of a group, you can just use its name (`Pos Waist` in the exemple above). 
 
[-- Advanced use case ------------------------------------------------------]

You can click the ` ℹ ` icons for a full explanation of the parameters available to customize or apply corrections to your sequence:
* A time range other then 00:00.0 -> End Of Scene.
* A different sound pattern.
* A different number of sound components and names.
* Adjust the delay or the margin of error accepted to register a sound.
* (In development) Use multiple reference interpolable.

[---------------------------------------------------------------------------]

### GENERATE THE PLAP FILES ###################################################
___
Once your have exported your Single File and configured the generator, press the `▶` Play button. The program will generate a file for each name in `Sound Components`. They will be created to whatever location your exported Single File was in.

The output should be something like this:

    Generating plap for 'Plap1', 'Plap2', 'Plap3', 'Plap4' with pattern 'V'
    Plap1:: Generated 67 keyframes from time 0.2 to 36.5
    Plap2:: Generated 67 keyframes from time 0.2 to 36.5
    Plap3:: Generated 67 keyframes from time 0.2 to 36.5
    Plap4:: Generated 67 keyframes from time 0.2 to 36.5
    Generated 'path/to/your/files/Timeline/Single Files/Plap1.xml'
    Generated 'path/to/your/files/Timeline/Single Files/Plap2.xml'
    Generated 'path/to/your/files/Timeline/Single Files/Plap3.xml'
    Generated 'path/to/your/files/Timeline/Single Files/Plap4.xml'
    Press Enter to exit...

See TROUBLESHOOTING below if you have an issue.

### SETUP YOUR SCENE ##########################################################
___
> In CharaStudio

With the Plap.xml files generated, it's time to add SFX components to your scene.
You can just import `/resources/Plap1234.png` that is included with this install and skip to the next phase: IMPORT TO TIMELINE.

* Create a folder for each name "plap_names" you defined in config.toml, they need to have the exact same names.

* Fill each components with 1 or more sound items of your choice, preferably low latency single sound items like (S)Piston. There is a "delay" parameter that you can use in the config if you want to play with sounds that are not instant.

* Each folder is activated in sequence, which will produce whatever combination of sounds you put in there.

### IMPORT TO TIMELINE ########################################################
___
> In CharaStudio

(If you already have interpolables in Timeline for your sound components, delete them)

For each of your sound components in your workspace:
* Click the folder to highlight it.
* In Timeline -> Single Files, load the corresponding name.

And voilà, a simple sequence of sound keyframes is added to your scene.

### LIMITATIONS ###############################################################
___
The reference can be lost if the subject of that interpolable:
 * (A) Increase/decrease his movement by a lot.
 * (B) Moves away from his point of origin.

 Case (A) can usually be corrected in CONFIGURATION.
 Case (B) is not yet supported with the app, only with TERMINAL.

### TROUBLESHOOTING ###########################################################
___
There are keyframes for only a part of the scene, then it stop :
* Most likely the subject moved from his position to much, you can try decreasing Min Pull Out and/or Min Push In.

There is a spam of sound keyframes at one point of the scene :
* This can happen when the subject makes micro in-out moves near the contact point, you can try increasing Min Pull Out and/or Min Push In.

Missing node: `<interpolableGroup name='xxx'>`
* The path you gave for the reference interpolable contains a parent group that is not recognized, make sure the path is correct.
* Modded CharaStudio auto-translates, look at your Timeline and press Alt+T to see the real names of the groups and interpolables.

Missing node: `<interpolable alias='xxx'>`
* An interpolable with the given name was not found. Make sure it is correct and that you renamed it in your scene before you exported it to Single File.
* Modded CharaStudio auto-translates, look at your Timeline and press Alt+T to see the real names of the groups and interpolables.

Could not find the reference keyframe at ...
* Make sure you gave the correct time for the reference keyframe.

Could not find the ... file
* PLAP generator cannot access `/configs` and `/resources`, or `config.toml` and `template.xml` that is supposed to be there.
