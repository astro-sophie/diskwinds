import os
import matplotlib
from radmc3dPy.image import *
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.pylab as plb
from generateimage import *
 
os.system('make cleanall') 
os.system('python3 master.py')
os.system('python3 problem_setup.py')
os.system('radmc3d mctherm setthreads 12')

os.system(f'radmc3d image lambda {wavelength} incl {inclination} phi {phi} zoomau {low_x} {up_x} {low_y} {up_y} npixx {npixx} npixy {npixy}')
img_online = readImage()
image_data_online = img_online.image.flatten()  # units of ergs/s/cm^2/Hz/ster

os.system(f'radmc3d image lambda {offline_wavelength} incl {inclination} phi {phi} zoomau {low_x} {up_x} {low_y} {up_y} npixx {npixx} npixy {npixy}')
img_offline = readImage()
image_data_offline = img_offline.image.flatten()  # units of ergs/s/cm^2/Hz/ster

image_data = (image_data_online) - (image_data_offline)

dist_pc = distance #from parameters.py, in pc
c = 3e10 #cm/s
line_peak = wavelength # from parameters.py, in um
conversion_factor = (img_online.sizepix_x*img_online.sizepix_y)/((dist_pc*pc)**2) # ergs/s/cm^2/Hz/ster to ergs/s/cm^2/Hz/pixel
total_flux = np.sum(image_data_online)*conversion_factor # ergs/s/cm^2
total_flux = f"{total_flux:.2e}"

result = plotImage2(img_online, flux=total_flux, log=True, maxlog=max_log, cmap=cm.hot, bunit='snu', dpc=dist_pc, arcsec=True)

plt.savefig('output.png')
plt.close()

file_path = "/home/reu24/hh30_data.py"
