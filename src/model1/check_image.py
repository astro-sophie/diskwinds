import pandas as pd
file = pd.read_csv("wind_density_output.csv")
for i in range(0, len(file['Density'])):
	if file['Density'][i] > 0:
		print(file['Density'][i])
