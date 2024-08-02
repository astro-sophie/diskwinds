# diskwinds

This repository contains an adaptation of the [Disk-Wind-Density-Program](https://github.com/K1zum1/Disc-Wind-Density-Program)

It is recommended to make a new folder for each model you run, first copying the base files folder and modifying from there. Unless you are looking to change how the disk wind characteristics are calculated (or the imaging settings in imaging.sh), you should not need to change anything other than parameters.py. 

To use, follow these steps:
1. Make a copy of the base_files directory and rename it to your desired model name 
2. Navigate to the model directory and make any desired modifications to the parameters.py input file (and possibly the imaging.sh file to modify the RADMC imaging commands)
3. Execute imaging.sh (run ./imaging.sh in the command line) to run RADMC and generate an image from your provided parameters and the settings in imaging.sh

