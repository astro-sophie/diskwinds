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
#os.system(f'radmc3d mctherm setthreads {n_threads}')

#os.system('radmc3d spectrum incl 0 iline 10 widthkms 50 linenlam 100')
#os.system('python3 flux_estimator.py')

dist_pc = distance #from parameters.py, in pc
c = 3e10 #cm/s
line_peak = wavelength # from parameters.py, in um

#os.system(f'radmc3d image iline {iline} incl {inclination} phi {phi} zoomau {low_x} {up_x} {low_y} {up_y} npixx {npixx} npixy {npixy}')
wavelengths = np.linspace(4.69105, 4.69145, 10)
center_wavelengths = [(wavelengths[i]+(wavelengths[i+1]-wavelengths[i])/2) for i in range(0, len(wavelengths)-1)]
dlambda = np.diff(wavelengths)
flux = 0
for i in range(0, len(center_wavelengths)):
     os.system(f'radmc3d image lambda {center_wavelengths[i]} incl {inclination} phi {phi} zoomau {low_x} {up_x} {low_y} {up_y} npixx {npixx} npixy {npixy}')
     img = readImage()
     image_data = img.image.flatten()
     image_flux = np.sum(image_data)*((dlambda[i]))
     flux += image_flux
     if i ==0:
          data = image_data
     else:
          data += image_data
conversion_factor = (img.sizepix_x*img.sizepix_y)/((dist_pc*pc)**2) # ergs/s/cm^2/Hz/ster to ergs/s/cm^2/Hz/pixel
total_flux = flux*conversion_factor*(c/(line_peak)) # ergs/s/cm^2
image_data = image_data.reshape((17,30), order='F')

#os.system(f'radmc3d image iline {iline} incl {inclination} phi {phi} zoomau {low_x} {up_x} {low_y} {up_y} npixx {npixx} npixy {npixy}')
#img = readImage()
#result = plotImage2(img, flux=total_flux, log=True, maxlog=max_log, cmap=cm.hot, bunit='snu', dpc=dist_pc, arcsec=True)
plt.imshow(image_data, cmap='Greens', vmin=0, vmax=1)
plt.title(f'Flux={total_flux}')
plt.show()
plt.savefig('output.png')
plt.close()
