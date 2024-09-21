import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Load the datasets
dataset = xr.open_dataset('NSIDC0081_SEAICE_PS_S25km_20240820_v2.0.nc')
concentration_data = xr.open_dataset('NSIDC0081_SEAICE_PS_N25km_20240820_v2.0.nc')
thickness_data = xr.open_dataset('RDEFT4_20240515.nc')

# Print out the dimensions to understand the structure
print("Dataset dimensions:")
print(dataset.dims)

print("Concentration data dimensions:")
print(concentration_data.dims)

print("Thickness data dimensions:")
print(thickness_data.dims)

# Resample or reproject the concentration and thickness data to match the main dataset
# For simplicity, let's use a basic resampling approach. Ensure you adjust the method to fit your needs.

def resample_data(data, target_grid):
    return data.interp(x=target_grid.x, y=target_grid.y, method='linear')

# Perform resampling
concentration_data_resampled = resample_data(concentration_data, dataset)
thickness_data_resampled = resample_data(thickness_data, dataset)

# Print resampled data to verify
print("Concentration data resampled:")
print(concentration_data_resampled)

print("Thickness data resampled:")
print(thickness_data_resampled)

# Merge datasets if alignment is successful
# Merge datasets with compat='override'
try:
    combined_data = xr.merge([dataset, concentration_data_resampled, thickness_data_resampled], compat='override')
    print("Combined dataset:")
    print(combined_data)
except Exception as e:
    print(f"Error during merging: {e}")

# Check available variables
print("Variables in combined dataset:")
print(combined_data.variables)

# Plot available variables
if 'F16_ICECON' in combined_data:
    combined_data['F16_ICECON'].plot()
else:
    print("Variable 'F16_ICECON' not found in the dataset.")

if 'sea_ice_thickness' in combined_data:
    combined_data['sea_ice_thickness'].plot()
else:
    print("Variable 'sea_ice_thickness' not found in the dataset.")

if 'ice_con' in combined_data:
    combined_data['ice_con'].plot()
else:
    print("Variable 'ice_con' not found in the dataset.")



plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Sea Ice Concentration')
plt.imshow(combined_data.F16_ICECON[0, :, :], cmap='Blues')
plt.colorbar(label='Concentration')
plt.xlabel('X')
plt.ylabel('Y')

# Plot Sea Ice Thickness
plt.subplot(1, 2, 2)
plt.title('Sea Ice Thickness')
plt.imshow(combined_data.sea_ice_thickness[:, :], cmap='Greens')
plt.colorbar(label='Thickness (m)')
plt.xlabel('X')
plt.ylabel('Y')

plt.tight_layout()
plt.show()