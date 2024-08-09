import numpy as np
from parameters import *

# Function to create a coordinate system
def coord(x_values, y_values, z_values):
    X, Y, Z = np.meshgrid(x_values, y_values, z_values, indexing="ij")
    R_plane = np.sqrt(X**2 + Y**2)
    R_values = np.sqrt(X**2 + Y**2 + Z**2)
    r_base = R_plane * np.abs(d) / (np.abs(d) + np.abs(z_values))
    return R_values, R_plane, r_base, X, Y, Z

# Function to calculate the angle
def calculate_angle(R_plane, z_values):
    delta = (np.pi / 2) - np.arctan(z_values / R_plane)				# Calculate angle from vertical
    return delta
    
# Function to calculate the temperature (preliminary, based only on r and z)
def calculate_temperature(r_base, z_values):
    T = 1000*(0.1*AU/abs(r_base))*((abs(r_base)/abs(z_values))**0.5)
    return T

# Function to calculate the mass loss rate
def calculate_mass_loss_rate(r_base, M_dot_w, p, r_in, r_out, R_plane, k):
    mass_loss_rate = np.zeros_like(r_base) 					# Initialize mass loss rate array
    mask = (r_base >= r_in) & (r_base <= r_out)					# Create a mask for values within the range [r_in, r_out]
    if np.any(mask):								# If any values in the mask, calculate the mass loss rate
        mass_loss_rate[mask] = k * (R_plane[mask] ** p)
    return mass_loss_rate
    
def get_source_point(R_plane, z_values, d):
    D = np.sqrt(R_plane**2 + (np.abs(z_values) + np.abs(d)) ** 2)		# Calculate D, the distance from the source point to any point in the space
    return D
    
# Function to calculate the poloidal velocity
def calculate_vp(d, GM_star, lmbda, r_base):
    factor = (2 * lmbda - 3)							# Calculate the factor used in the velocity equation
    if factor < 0:								# Check if the factor is less than 0, which would cause a math error
        raise ValueError("Invalid value of lambda causing sqrt of negative number")
    vp = (np.sqrt(factor) * np.sqrt(GM_star)) / np.sqrt(r_base)			# Calculate the poloidal velocity
    return vp

def wind_density(m_dot_wi, vp_wi_l, delta, d, D_wi_l):
    abs_cos_delta = np.abs(np.cos(delta))					# Calculate the absolute value of the cosine of the angle
    wind_density = (m_dot_wi / (vp_wi_l * abs_cos_delta)) * (np.abs(d) / (D_wi_l * abs_cos_delta)) ** 2		# Calculate the wind density
    vals = np.full((nx,ny,nz),0)
    n_filled = 0
    for i in range(0,nx):
    	for j in range(0,ny):
    		for k in range(0,nz):
    			if wind_density[i,j,k] != 0:
    				vals[i,j,k] = (1e8)/(abs(Z[i,j,k]/AU)**2)
    			else:
    				vals[i,j,k] = 0
    vals = vals*(10**-20)*(4*1e6)
    return wind_density

# Main Execution
try:
    # Call all the functions to calculate the wind density
    expected_entries = nx * ny * nz
    
    R_values, R_plane, r_base, X, Y, Z = coord(xc, yc, zc)
    vp_wi_l = calculate_vp(d, GM_star, lmbda, r_base)
    m_dot_wi = calculate_mass_loss_rate(r_base, M_dot_w, p, r_in, r_out, R_plane, k)
    delta = calculate_angle(R_plane, zc)
    D_wi_l = get_source_point(R_plane, zc, d)
    # temp0_array = calculate_temperature(r_base, z_values)
    temp0_array = np.full((expected_entries,), temp0)
    density = wind_density(m_dot_wi, vp_wi_l, delta, d, D_wi_l)

    for i in range(0, nx):
        for j in range(0, ny):
            if density[i,j,30]>0:
                print(density[i,j,30])

    # Save the results to CSV files
    density_flattened = density.flatten()
    np.savetxt("wind_density_output.csv", density_flattened, delimiter=",", header="Density", comments="")
    print("Wind density has been computed and saved to wind_density_output.csv")
    
    vp_flat = vp_wi_l.flatten()
    np.savetxt("wind_velocity_output.csv", vp_flat, delimiter=",", header="Velocity", comments="")
    print("Wind velocity has been computed and saved to  wind_output.csv")
    
    np.savetxt("temp0_output.csv", temp0_array, delimiter=",", header="Temp0", comments="")
    print("Wind temperature has been computed and saved to  temp0_output.csv")
    
    print("The simulation has been successfully executed and the results have been saved.")    
except Exception as e:
    print("An error occurred during the simulation:", str(e))
