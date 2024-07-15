# diskwinds

This repository contains an adaptation of the Disk-Wind-Density-Program by Jae Chong.

It is recommended to make a new folder for each model you run, first copying the base files folder and modifying from there. Unless you are looking to change how the disk wind characteristics are calculated, you should not need to change anything other then parameters.py. 

Currently, this program is only capable of modeling a single molecule/atom at a time. 

To use, follow these steps:
1. Navigate to the model directory
2. Make any desired modifications to the parameters.py input file
3. Run master.py
4. Run problem_setup.py
5. Use the command radmc3d mctherm setthreads [desired number of threads]
6. After the Monte Carlo simulation has completed, run radmc3d image lambda [desired wavelength] incl [desired inclination] phi [desired viewing angle]
7. Run generate_image.py to see the result image in the given wavelength, as well as the calculated flux in ergs/s/cm^2
