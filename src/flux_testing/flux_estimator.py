import numpy as np
import matplotlib.pyplot as plt

# Constants
AU = 1.496e13 #cm
c = 2.998e10 #cm/s
pc = 3.08e18 #cm
dist = 140.0 #pc

# Line particulars for H2 S(9)
Aval = 4.991e-7 #Einstein coefficient
T_upper = 10261.792 #Kelvin
nu_line = 6.390457e4 *1e9
g_upper = 79.0
dE = 6.626e-27*nu_line

# Files
def import_lines_from_file(file_path, start_line, end_line):
    extracted_lines = []
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if start_line <= current_line_number <= end_line:
                extracted_lines.append(line.rstrip()) 
            elif current_line_number > end_line:
                break
    vals = []
    for line in extracted_lines:
        parts = line.strip().split()
        vals.append([float(part) for part in parts])
    return vals
levels = np.array(import_lines_from_file('molecule_h2.inp', 8, 325))

grid = np.loadtxt('amr_grid.inp', skiprows=6)
nx, ny, nz = int((len(grid)-3)/3), int((len(grid)-3)/3), int((len(grid)-3)/3)

temp = np.loadtxt('gas_temperature.inp',skiprows=2)
temp = temp.reshape((nx,ny,nz), order='F')

numberdens = np.loadtxt('numberdens_h2.inp', skiprows=2)
numberdens = numberdens.reshape((nx,ny,nz), order='F')
print("All files loaded in")

# Partition function
def partitionfcn(mol_levels, t):
    n = mol_levels[:,0]
    e = mol_levels[:,1]
    g = mol_levels[:,2]
    nl = np.size(n)
    zt = 0
    for i in range(0,nl):
        zt += g[i]*np.exp(-e[i]*1.43873/t)
    return zt

# Grid definition
x = grid[0:nx+1]
y = grid[nx+1:nx+ny+2]
z = grid[nx+ny+2:nx+ny+nz+3]

# Flux calculation
flux = 0
num = 0
for i in range(0, nx):
    for j in range(0, ny):
        for k in range(0, nz):
            Z = partitionfcn(levels, temp[i,j,k])
            n_upper = numberdens[i,j,k]*(g_upper/Z)*np.exp(-T_upper/temp[i,j,k])
            dV = (x[i+1]-x[i])*(y[j+1]-y[j])*(z[k+1]-z[k])
            flux += n_upper*Aval*dE*dV/(4*np.pi*(dist*pc)**2)
            num += 1
            if (num%10000==0):
            	print(f'{num}/{nx*ny*nz}')
print(flux,'from theoretical expression')


f=np.loadtxt('spectrum.out',skiprows=3)
#lam is in microns and flux is in erg/cm2/s/Hz at 1pc distance
lam=f[:,0]*1e-4
flux=f[:,1]/dist**2
plt.plot(lam,flux)
# dnu = dlam * c/lam^2
dlam=np.diff(lam)
dlam=np.insert(dlam,0,dlam[0])
dnu = dlam * c/(lam**2)
print(np.sum(dnu*flux),' From RADMC model')
plt.savefig('spec.png')
plt.close()
