import subprocess
import numpy as np
from radmc3dPy.natconst import *

constant_density = 1e-17

# Constants
AU = 1.493e13  									# AU in cm
MS = 1.99e+33   								# Solar mass in grams
RS = 6.96e10   									# Solar radius in cm
MU = 2.3e-24    								# Mean molecular weight in grams

# Star Parameters
GM_star = 6.674e25  								# Gravitational parameter for the star
distance = 140									# Distance in parsecs

# Wind Parameters
M_dot_w = 1e20  								# Wind mass loss rate in grams/second
lmbda = 1.6     								# Alfven lever parameter
d = -25 * AU     								# Distance of wind source point below the origin
p = 3.4959999999999996  							# Exponent in mass loss rate calculation
temp0 = 1500									# Wind temperature (constant for now)

# Line parameters 
molecule_name = "h2"
abun = 1e-4									# Abundance of given molecule

# Radial Boundaries for Mass Loss Calculation
r_in = 3 * AU  								# Inner boundary radius
r_out = 6 * AU  								# Outer boundary radius
k = ((p + 2) * M_dot_w) / (2 * np.pi * (r_out**(p + 2) - r_in**(p + 2))) 	# proportionality constant for mass loss rate

# Grid parameters
nx, ny, nz = 64, 64, 64							# Number of cells in each direction
sizex = 420 * AU								# Size across the x direction
sizey = 420 * AU								# Size across the y direction
sizez = 420 * AU								# Size across the z direction

# Model parameters
dusttogas = 1e-5								# Ratio of dust to gas (for calculating dust density from gas density)
vturb_factor = 6427.0								# Factor by which sqrt(tgas) is multiplied to determine gas turbulence velocities

# RADMC3D settings (don't change without reading the documentation)
incl_dust = 0									# Include dust in calculations
incl_lines = 1									# Include lines in calculations
nphot = 1e7									# Number of photon packages to split luminosity into
scattering_mode_max = 0                                                         # Gives scattering information; if 0, isotropic scattering
lines_mode = 1									# 1 = LTE
tgas_eq_tdust = 0                                                               # Tells RADMC whether to interpret gas and dust temperatures as equal
lines_widthmargin = 24								# Tolerance for line contribution
n_threads = 4                                                                  # Defines number of parallel threads, larger = shorter runtime

# Imaging settings
max_log = 1                                                                   # Defines maximum for colorbar in logscale
iline = 10
wavelength = 4.69125225                                                         # Wavelength of desired transition for imaging, in micrometers
offline_wavelength = 4.6                                                        # Wavelength for continuum subtraction
inclination = 85                                                                # Viewing inclination from vertical, in degrees
phi = 0                                                                         # Observing angle on disk plane, in degrees
low_x, up_x = -210, 210                                                         # Limits for plotting on x-axis, in AU (from center at specified distance)
low_y, up_y = 14, 252                                                         # Limits for plotting on y-axis, in AU (from center at specified distance)
npixx, npixy = 30, 17

# Star parameters from constants file
mstar = MS									# Stellar mass
rstar = 2 * RS									# Stellar radius
tstar = 5500									# Stellar temperature
pstar = np.array([0., 0., 0.])							# Star position (lies at the origin if all zeros)

# Wavelength settings
# Sets discrete wavelength points for the continuum radiative transfer calculations
lam1, lam2, lam3, lam4, lam5 = 0.1, 4.5, 4.8, 25.0, 10000.0 				# This and the next line create a staggered wavelength list, with more values at lower wavelengths
n12, n23, n34, n45 = 3000, 10000, 3000, 3000							# Number of values between lam1 & lam2, between lam2 & lam3, between lam3 & lam4
lam12 = np.logspace(np.log10(lam1), np.log10(lam2), n12, endpoint=False)
lam23 = np.logspace(np.log10(lam2), np.log10(lam3), n23, endpoint=False)
lam34 = np.logspace(np.log10(lam3), np.log10(lam4), n34, endpoint=False)
lam45 = np.logspace(np.log10(lam4), np.log10(lam5), n45, endpoint=True)
lam = np.concatenate([lam12, lam23, lam34, lam45])					# Creates a single array of all provided wavelengths
nlam = lam.size

# Grid setup
xi = np.linspace(-sizex, sizex, nx + 1)						# Grid cell wall positions from the size and number of points
yi = np.linspace(-sizey, sizey, ny + 1)
zi = np.linspace(-sizez, sizez, nz + 1)
xc = 0.5 * (xi[0:nx] + xi[1:nx + 1])						# Grid cell center positions
yc = 0.5 * (yi[0:ny] + yi[1:ny + 1])
zc = 0.5 * (zi[0:nz] + zi[1:nz + 1])
