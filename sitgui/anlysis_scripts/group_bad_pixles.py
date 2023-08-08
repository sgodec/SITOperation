import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read chip names from file
with open('chips.txt', 'r') as f:
    chip_names = [line.strip() for line in f.readlines()]

# Use latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Create a larger figure
fig, ax = plt.subplots(figsize=(10, 8))

# Initialize lists to hold the data
value1 = []
value2 = []

# Loop over chip names and gather data
for chip in chip_names:
    # Read specific lines for the chip
    with open(f'../SiT_testing/{chip}_ANLYSIS/stats_{chip}.txt', 'r') as f:
        lines = f.readlines()
        value1.append(float(lines[4].split(":")[1].strip()))  # Assuming that "line 4" means index 3 in Python
        value2.append(float(lines[9].split(":")[1].strip()))  # Assuming that "line 8" means index 7 in Python

# Define bar width
bar_width = 0.35
index = np.arange(len(chip_names))

# Add bars for value 1 and value 2
bar1 = ax.bar(index, value1, bar_width, label='Number of Badpixels Threshold')
bar2 = ax.bar(index + bar_width, value2, bar_width, label='Number of Badpixels ToT')

# Add labels and title
ax.set_xlabel('Modules', fontsize=14)
ax.set_ylabel('Number of pixels', fontsize=14)
ax.set_title('Badpixels for each module', fontsize=16)

# Set Y-axis limit
ax.set_ylim([0, 80])  # adjust as necessary

# Add xticks - on the 'index' position, we place the corresponding chip name
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(chip_names, rotation=45)

# Add legend
ax.legend(fontsize=12)

# Increase tick label size
ax.tick_params(axis='both', which='major', labelsize=12)

# Save figure
plt.savefig('../SiT_testing/all_modules_anlysis/sensor_badpixels_values.png', dpi=300)

