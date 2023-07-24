import numpy as np
import matplotlib.pyplot as plt

# Load the data from the text file
data = np.loadtxt('iv_data.txt')

# Extract the columns
x_values = np.abs(data[:, 0])
y_values = np.abs(data[:, 1])

# Plot the data
plt.semilogy(x_values, y_values)
plt.xlabel('$V[V]$')
plt.ylabel('$I[mI]$')
plt.title('IV Scan for module B2-M37')
plt.show()

