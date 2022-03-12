# BitsAndChisels-Blueprint
Schem (sponge) file conversion to blueprint nbt file, and allowing paste / load / saving it for bits and chisels

# How to use?
First you need to install python 3.8+ and nbtlib via pip.
go to CMD, and run /pip install nbtlib... or do it yourself.
Then you need .schem format file, its not litematic file. It can be obtained in various ways, but I will take one from https://github.com/Pangamma/PixelStacker.

You also need Fabric-Carpet https://github.com/gnembon/fabric-carpet to import nbt file, or manage, or set in world.

# Schem -> Nbt conversion for 'blueprints'
If you're ready, then run something like this:
`#a = Schem(nbtlib.load('mumeibig.schem'))
#a.saveAll('birb')`

It will save all the parts of the file as 'blueprint', so that you can load it from following script.
# Fabric Carpet Script(Scarpet) and Pasting

Sp or Mp, if you run minecraft with carpet, then scripts folder will be generated under worlds/worldname folder. Put blueprint.sc in /scripts/folder.
Then you can load it via /script load blueprint.

Zip all the results and put inside /scripts/blueprint.data/, then you can run following script to 'paste':
If you saved as mumei.zip and it starts with birb, then
`/script in blueprint run pasteFrom('mumei.zip','birb',[0,128,0])`

if you want it to start from [0,128,0], toward +x +y +z.

It will paste blocks automatically : but remember, it can be laggy or there could be some visual glitch, so rejoin minecraft to see it properly.
![2022-03-12_23 46 00](https://user-images.githubusercontent.com/35677394/158023245-b75214ef-9b1f-4ac8-8c2e-d231ce551e90.png)

Yes cute birb with bits and chisels!

It means, you can generate any mini-structures using this!

# Script usage for survival
now there's no zip support, but there's save / load / info command.

`/blueprint info`

It shows how many bits you need for current 'holding' blueprint.

`/blueprint save <name>`

It saves current holded blueprint into prefixes + name.

`/blueprint load <name>`

It loads blueprint from <name>.Overrides current data of blueprint item.
  
`/blueprint loadZip mumei2 a0b0b0`
 
 It loads a0b0b0.nbt from mumei2.zip.
  
