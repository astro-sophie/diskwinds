import numpy as np
from parameters import *
from radmc3dPy.natconst import *

try: # loading in data produced by master.py run
    vp_data = "wind_velocity_output.csv" 
    vp = np.loadtxt(vp_data, delimiter=",", skiprows=1).reshape(nx, ny, nz)
    rhogas_data = "wind_density_output.csv"
    rhogas = np.loadtxt(rhogas_data, delimiter=",", skiprows=1).reshape(nx, ny, nz)
    temp_data = "temp0_output.csv"
    temp0 = np.loadtxt(temp_data, delimiter=",", skiprows=1).reshape(nx, ny, nz)
    print("Data loading completed successfully.")
except Exception as e:
    print(f"Error loading data: {e}")

try: # creating 3D mesh grid, establishing parameters
    X, Y, Z = np.meshgrid(xc, yc, zc) 				# creating 3D meshgrid
    R_plane = np.sqrt(X**2 + Y**2) 				# points along the disk plane
    tan_y_x = np.arctan2(Y, X) 					# arctan(Y/X), direction of each grid cell on the disk plane
    tan_z_r = np.arctan2(Z, R_plane) 				# arctan (Z/R_plane), angle of each grid cell from the disk plane
    sqrt_GMstar_r = np.sqrt(GM_star / (R_plane + 1e-10)) 		# Keplerian orbital velocity of each grid cell

    Vx = (sqrt_GMstar_r * np.sin(tan_y_x) + vp * np.cos(tan_z_r) * np.cos(tan_y_x)) # directional orbital velocity + poloidal velocity
    Vy = (-sqrt_GMstar_r * np.cos(tan_y_x) + vp * np.cos(tan_z_r) * np.sin(tan_y_x))
    Vz = vp * np.sin(tan_z_r)

    rhod = rhogas * dusttogas 					# dust density
    tgas = temp0 						# temperature currently constant, will eventually be calculated as a function of radius
    vturb = vturb_factor * np.sqrt(tgas) 			# turbulent velocity from gas kinematics

    n_molecule = rhogas*fact 					# number density of the molecule being analyzed
    
    print("Calculations completed successfully.")
except Exception as e:
    print(f"Error in calculations: {e}")

try:
    with open('numberdens_'+str(molecule_name)+'.inp','w+') as f: # number density of molecular gas per grid cell
        f.write('1\n')                       			# format number, typically 1 at present (see RADMC documentation)
        f.write('%d\n'%(nx*ny*nz))           			# number of cells
        data = n_molecule.ravel(order='F')          		# Create a 1-D view, fortran-style indexing
        data.tofile(f, sep='\n', format="%13.6e")
        f.write('\n')
    print("numberdens_"+str(molecule_name)+".inp written successfully.")
except Exception as e:
    print(f"Error writing numberdens_"+str(molecule_name)+".inp: {e}")

try:
    with open('amr_grid.inp','w+') as f:
        f.write('1\n')                       			# iformat
        f.write('0\n')                       			# AMR grid style  (0=regular grid, no AMR)
        f.write('0\n')                      			# Coordinate system
        f.write('0\n')                       			# gridinfo
        f.write('1 1 1\n')                   			# Include x,y,z coordinate
        f.write('%d %d %d\n'%(nx,ny,nz))     			# Size of grid
        for value in xi:
            f.write('%13.6e\n'%(value))      			# X coordinates (cell walls)
        for value in yi:
            f.write('%13.6e\n'%(value))      			# Y coordinates (cell walls)
        for value in zi:
            f.write('%13.6e\n'%(value))      			# Z coordinates (cell walls)
    print("amr_grid.inp written successfully.")
except Exception as e:
    print(f"Error writing amr_grid.inp: {e}")

expected_entries = nx * ny * nz
actual_entries = len(rhod.ravel(order='F'))			

print(f"Expected Entries: {expected_entries}, Actual Entries: {actual_entries}") # check whether the number of entries matches what is expected

try:
    with open('dust_density.inp', 'w+') as f:
        f.write('1\n') 						# iformat (typically 1 at present)
        f.write(f"{expected_entries}\n")			# Number of cells
        f.write('1\n')						# Number of independent dust species densities given 
        for value in rhod.ravel(order='F'):
            f.write(f"{value:e}\n")
    print("dust_density.inp written successfully.")
except Exception as e:
    print(f"Error writing dust_density.inp: {e}")

try:
    with open('gas_velocity.inp','w+') as f:
        f.write('1\n')						# iformat (typically 1 at present)
        f.write('%d\n' % (nx * ny * nz))			# Number of cells
        for ix in range(nx):
            for iy in range(ny):
                for iz in range(nz):
                    f.write('%13.6e %13.6e %13.6e\n' % (Vx[ix, iy, iz], Vy[ix, iy, iz], Vz[ix, iy, iz])) # Writes velocity in x, y, z
    print("gas_velocity.inp written successfully.")
except Exception as e:
    print(f"Error writing gas_velocity.inp: {e}")

try:
    with open('microturbulence.inp','w+') as f:
        f.write('1\n')                      	 		# Format number
        f.write('%d\n'%(nx*ny*nz))           			# Nr of cells
        data = vturb.ravel(order='F')        			# Create a 1-D view, fortran-style indexing
        data.tofile(f, sep='\n', format="%13.6e") 		# Writes turbulent velocities to file
        f.write('\n')
    print("microturbulence.inp written successfully.")
except Exception as e:
    print(f"Error writing microturbulence.inp: {e}")

try:
    with open('gas_temperature.inp','w+') as f:
        f.write('1\n')                       			# Format number
        f.write('%d\n'%(nx*ny*nz))           			# Nr of cells
        data = tgas.ravel(order='F')         			# Create a 1-D view, fortran-style indexing
        data.tofile(f, sep='\n', format="%13.6e")		# Write gas temperatures to file
        f.write('\n')
    print("gas_temperature.inp written successfully.")
except Exception as e:
    print(f"Error writing gas_temperature.inp: {e}")

try:
    with open('wavelength_micron.inp','w+') as f: 		# sets discrete wavelength points for the continuum radiative transfer calculations (not the same as wavelength grid used for line radiative transfer)
        f.write('%d\n'%(nlam))					# number of wavelengths
        for value in lam:
            f.write('%13.6e\n'%(value))				# write wavelength values (specified in parameters) to file
    print("wavelength_micron.inp written successfully.")
except Exception as e:
    print(f"Error writing wavelength_micron.inp: {e}")

try:
    with open('stars.inp','w+') as f:				# specifies number of stars, positions, radii, and spectra
        f.write('2\n')						# iformat (put to 2!)
        f.write('1 %d\n\n'%(nlam))				# number of stars, number of wavelengths
        f.write('%13.6e %13.6e %13.6e %13.6e %13.6e\n\n'%(rstar,mstar,pstar[0],pstar[1],pstar[2]))	# lists out star radius, star mass, x position, y position, z position
        for value in lam:
            f.write('%13.6e\n'%(value))				# creates list of all wavelengths
        f.write('\n%13.6e\n'%(-tstar))				# creates a list of the fluxes
    print("stars.inp written successfully.")
except Exception as e:
    print(f"Error writing stars.inp: {e}")

try:
    with open('dustopac.inp','w+') as f:
        f.write('2\n')  					# iformat (put to 2)
        f.write('1\n') 						# Number of dust species that will be loaded
        f.write('============================================================================\n')
        f.write('1\n') 						# Indicates what form to read dust opacity in--when set to 1, the dustkappa_*.inp file style is used
        f.write('0\n')						# 0 for normal thermal grains (non-zero if quantum-heated grain)
        f.write('silicate\n') 					# Name of dust species
        f.write('----------------------------------------------------------------------------\n')
    print("dustopac.inp written successfully.")
except Exception as e:
    print(f"Error writing dustopac.inp: {e}")

try:
    with open('lines.inp','w') as f:
        f.write('2\n') 						# iformat (put to 2)
        f.write('1\n') 						# number of molecules/atoms to be modeled
        f.write(str(molecule_name)+'    leiden    0    0    0\n') # molecule name, input style, dummy column, dummy column, which collision partner particle the rate tables are associated with (not needed here)
    print("lines.inp written successfully.")
except Exception as e:
    print(f"Error writing lines.inp: {e}")

try:
    with open('radmc3d.inp','w+') as f:				# see section 16.1 of the RADMC documentation for more information
        f.write('nphot = %d\n'%(nphot))				# number of photon packages for the scattering Monte Carlo simulations
        f.write('scattering_mode_max = '+str(scattering_mode_max)+'\n')   # Put this to 1 for isotropic scattering
        f.write('tgas_eq_tdust   = '+str(tgas_eq_tdust))	# tells radmc whether or not to read the dust_temperature.inp file and equate it to the gas temperature
    print("radmc3d.inp written successfully.")
except Exception as e:
    print(f"Error writing radmc3d.inp: {e}")

print("All files written successfully.")
