### INSTALLATION ##############################################################

Unzip the archive wherever you like, make sure config.toml, generate_plaps, and 
template.xml are always together.

### LIMITATIONS ###############################################################

This program uses a Timeline interpolable as reference to generate a sequence 
to use with sound folders. It is meant to sync with a simple movement like 
forward-backward, up-down, etc. 

If the subject of that interpolable moves away from his point of origin, or 
change his movement to much, the reference will be lost.

 [-- Advanced use case ------------------------------------------------------]
  
  That being said you can define multiple reference as well as the margin of 
  error allowed, so if your subject moves to much you can adjust the margin or
  define a time range for which each reference is valid.

  see reference.toml for available customization.
  see multi_ref.toml for an exemple of multiple references.

 [---------------------------------------------------------------------------]

### EXPORT TIMELINE SINGLE FILE ###############################################

This program uses a Timeline interpolable as reference to generate a sequence.
* Choose an interpolable like "GO Pos Waist", Hips, Dick. Rotation is fine too.
* Rename it with an alias, can also just Rename -> ctrl+X -> ctrl+V.
* Click the owner of that interpolable in your Workspace then
  Timeline -> Single Files -> Save.

### CONFIG.TOML ###############################################################

There are only two required info for a default generation of a sequence: The 
name of the interpolable (or path if part of a group) and the time of a 
reference keyframe.

* Choose a keyframe where the interpolable is fully extended:
-- Dick pushed in the female.
-- Female pushed on dick (if she's the one moving).
-- It can be whatever is the apex/movement of your interpolable.
* Copy the exact Time of that interpolable.
* Copy the exact Name of that interpolable.

Exemple: Your interpolable "Pos Waist" is part of a group(s), and the reference
	 keyframe is at 00:02.454
 __________
|  Main    |
------------
 |   male   |      "00:02.454"
 ------------      ⇓
  |Pos Waist|    ◆◆◆ ◆◆◆ ◆◆◆       ◆◆ ◆◆ ◆◆◆◆◆◆
   ---------

your config.toml would look like this:

[[plap_group]]
interpolable_path = "Main.male.Pos Waist"
ref_keyframe_time = "00:02.454"
### You can redefine the number of sound folders and their names ##
plap_names = ["Plap1", "Plap2", "Plap3", "Plap4"]

 [-- Advanced use case ------------------------------------------------------]

  You can check reference.toml for a full explanation of the parameters 
  available to customize your sequence, such as:
  * A time range other then 00:00.0 -> End Of Scene.
  * A different sound pattern.
  * Use multiple reference interpolable.
  * Adjust the delay or the margin of error accepted to register a sound.
  * ...

 [---------------------------------------------------------------------------]

### GENERATE THE PLAP FILES ###################################################

Once your have exported your Single File and setup your config.toml, just take
your Single File and drop it on generate_plaps. The program will generate a
file for each name in "plap_names" of your config.toml file. They will be 
created to whatever location your Single File was in.

The output should be something like this:

Generating plap for ['Plap1', 'Plap2', 'Plap3', 'Plap4'] with pattern 'V'
Plap1:: Generated 67 keyframes from time 0.2 to 36.5
Plap2:: Generated 67 keyframes from time 0.2 to 36.5
Plap3:: Generated 67 keyframes from time 0.2 to 36.5
Plap4:: Generated 67 keyframes from time 0.2 to 36.5
Generated 'path\to\your\files\Timeline\Single Files\Plap1.xml'
Generated 'path\to\your\files\Timeline\Single Files\Plap2.xml'
Generated 'path\to\your\files\Timeline\Single Files\Plap3.xml'
Generated 'path\to\your\files\Timeline\Single Files\Plap4.xml'
Press Enter to exit...

See TROUBLESHOOTING below if you have an issue.

### SETUP YOUR SCENE ##########################################################

With the Plap.xml files generated, it's time to add SFX folders to your scene.
You can just import into your scene Plap1234.png that is included with this 
install and skip to the next phase: IMPORT TO TIMELINE.

*
 Create a folder for each name "plap_names" you defined in config.toml, they 
 need to have the exact same names.
* 
 Fill each folders with 1 or more sound items of your choice, preferably low 
 latency single sound items like (S)Piston. There is a "delay" parameter that 
 you can use in the config if you want to play with sounds that are not instant.
*
 Each folder is activated in sequence, which will produce whatever combination
 of sounds you put in there.

### IMPORT TO TIMELINE ########################################################

Open Timeline -> Single Files, and for each of your sound folders:
* Click the folder to highlight it.
* Click on the corresponding name in the Single Files.
* Click Load

And voilà, a simple sequence of sound keyframes is added to your scene.



### TROUBLESHOOTING ###########################################################

NodeNotFoundError: Node not found: interpolableGroup[@name='Whatever']
* The path to your interpolable contains a group that is not recognized make 
  sure it is the correct group.

NodeNotFoundError: Node not found: interpolable[@alias='My Interpolable']
* An interpolable with the given name was not found. Make sure it is correct 
  and that you renamed it in your scene before you exported it to Single File.

NodeNotFoundError: The reference keyframe was not found
* Make sure you gave the correct time for the reference keyfram





