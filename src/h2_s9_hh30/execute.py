import os
import matplotlib
from radmc3dPy.image import *
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.pylab as plb
 
#subprocess.Popen('python3 master.py', shell=True)
#subprocess.Popen('python3 problem_setup.py', shell=True)
#subprocess.Popen('radmc3d mctherm setthreads 4', shell=True)
#subprocess.Popen('radmc3d image lambda 4.69125225 incl 85 phi 0 zoomau -210 210 14 252 npixx 30 npixy 17', shell=True)
#subprocess.Popen('python3 generateimage.py', shell=True)

os.system('python3 master.py')
os.system('python3 problem_setup.py')
os.system('radmc3d mctherm setthreads 4')
os.system('radmc3d image lambda 4.69125225 incl 85 phi 0 zoomau -210 210 14 252 npixx 30 npixy 17')
os.system('python3 generateimage.py')
