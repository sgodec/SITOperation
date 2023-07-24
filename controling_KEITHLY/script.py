import pyvisa
import time
import matplotlib.pyplot as plt
import os

chip = str(input('ChipName'))
# Resource string for the Keithley instrument (e.g., "GPIB0::22::INSTR")
resource_string = "GPIB0::24::INSTR"

# Open the connection to the instrument
rm = pyvisa.ResourceManager()
keithley = rm.open_resource(resource_string)

# Set the voltage range and compliance level
voltage_range = 50.0  # Set the appropriate voltage range in volts
compliance_level = 0.0005  # Set the compliance level in amperes (0.5 mA)
breakdown_current = 0.48  # Set the breakdown current threshold

# Configure the Keithley instrument
keithley.write("SOUR:VOLT:RANG {}".format(voltage_range))
keithley.write("SENS:CURR:PROT {}".format(compliance_level))
keithley.write("SENS:FUNC:CONC OFF")  # Disable concurrent functions

# Prepare the plot
fig, ax = plt.subplots()
line, = ax.semilogy([], [], 'r-')
ax.set_xlim(0, 2*voltage_range)
ax.set_ylim(0, 2*compliance_level)
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('Current (mA)')
ax.set_title('IV Curve Measurement')

curr = []
vol = []

data_file = open("/home/simonsdell/Desktop/CERN/SiT_testing/" + chip + "/iv_data.txt", "w")  # Open the file for writing


def update_plot(frame):
    global curr, vol
    ax.clear()
    ax.semilogy(vol, curr, 'r-')
    ax.set_xlim(0, voltage_range)
    ax.set_ylim(0, compliance_level)
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (mA)')
    ax.set_title('IV Curve Measurement')

# Perform the IV curve measurement
start_voltage = 0.0
voltage_step = 1.0

for voltage in range(int(start_voltage), -int(voltage_range), -int(voltage_step)):
    keithley.write("SOUR:VOLT {}".format(voltage))
    data = keithley.query("MEAS:CURR?").split(",")
    current = abs(float(data[1])) * 1000
    volt = abs(float(data[0]))
    print("Voltage: {:.2f} V, Current: {:.3f} mA".format(volt, current))
    if current >= breakdown_current:
        # Break the loop if breakdown current occurs
        break
    time.sleep(30)  # Delay for 30 seconds between voltage steps
    data = keithley.query("MEAS:CURR?").split(",")
    current = abs(float(data[1])) * 1000
    volt = abs(float(data[0]))
    
    curr.append(current)
    vol.append(volt)

    # Update the plot
    #update_plot(0)
    #plt.pause(0.5)
    # Write voltage and current to the file
    data_file.write("{:.2f}\t{:.3f}\n".format(volt, current))

    # Process and store the measurement (e.g., save to a file or plot the data)
    print("Voltage: {:.2f} V, Current: {:.3f} mA".format(volt, current))
    
data_file.close()  # Close the file

# Decrease the voltage slowly to 0
while voltage < 0:
    print("CMPL reached")
    time.sleep(5)  
    voltage += voltage_step
    keithley.write("SOUR:VOLT {}".format(voltage))
    data = keithley.query("MEAS:CURR?").split(",")
    current = abs(float(data[1]))
    volt = abs(float(data[0]))
    print("Voltage: {:.2f} V, Current: {:.7f} A".format(volt, current))
keithley.close()  # Close the connection, i have worte this script now i want to use matplotib to draw data intime

os.chmod("/home/simonsdell/Desktop/CERN/SiT_testing/" + chip + "/iv_data.txt", 0o644)

plt.show()  # Show the final plot

