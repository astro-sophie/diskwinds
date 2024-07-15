# diskwinds

This repository contains an adaptation of the [Disk-Wind-Density-Program](https://github.com/K1zum1/Disc-Wind-Density-Program)

It is recommended to make a new folder for each model you run, first copying the base files folder and modifying from there. Unless you are looking to change how the disk wind characteristics are calculated (or the imaging settings in imaging.sh, as this portion of the program is still in development), you should not need to change anything other than parameters.py. 

To use, follow these steps:
1. Navigate to the model directory
2. Make any desired modifications to the parameters.py input file
3. Execute imaging.sh to run RADMC and generate an image from your provided parameters and the settings in imaging.sh

Currently, this program is only capable of modeling a single molecule/atom at a time. 
