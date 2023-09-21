import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read chip names from file
with open('chips.txt', 'r') as f:
    chip_names = [line.strip() for line in f.readlines()]

# Use latex font
#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

# Create a larger figure
fig, ax = plt.subplots(figsize=(14, 12))

# Generate a unique color for each chip
num_colors = len(chip_names)
colors = plt.cm.viridis(np.linspace(0, 1, num_colors))

for i, chip in enumerate(chip_names):
    data = pd.read_csv(f'../SiT_testing//{chip}/iv_data.txt', sep='\s+', header=None, names=['Voltage', 'Current'])
    ax.plot(data['Voltage'], data['Current'], label=chip, color=colors[i], linewidth=2.0)
    ax.scatter(data['Voltage'], data['Current'], color=colors[i], alpha=0.3)

    # Add scatter plot
    ax.scatter(data['Voltage'], data['Current'],color=colors[i], alpha=0.3)

# Add complementary level line
ax.axhline(y=0.5, color='r', linestyle=':', label='cmpl level batch1')
ax.axhline(y=0.25, color='r', linestyle=':', label='cmpl level batch2')

# Set labels and title
ax.set_xlabel('Voltage [V]', fontsize=14)
ax.set_ylabel('Current [mA]', fontsize=14)
ax.set_title('Compare IV curve', fontsize=24)

# Add legend
#ax.legend(fontsize=12)
# Place the legend to the right of the plot
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Adjust the layout so that the plot is fit inside its area
plt.tight_layout()

# Increase tick label size
ax.tick_params(axis='both', which='major', labelsize=12)

# Save figure
plt.savefig('../SiT_testing/all_modules_anlysis/iv_combined.png',dpi = 400)

