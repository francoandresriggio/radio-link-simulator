from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from file_manipulation import *
from Scripts.calculations import *

def browse_file():
    file = filedialog.askopenfilename(title="Open coordinate file")
    directory.set(file)

def activate_simulation():
    k = factorK.get()
    n = fresnelN.get()
    percentage = fresnel_percentage.get()
    lambda_sim = lambda_simulation.get()
    gain = antenna_gain.get()
    eirp = eirp_antenna.get()

    latitude, longitude, altitude = extract_info(directory.get())

    # Get the distance between two points (ignoring heights). This applies to both link ends and intermediate points:
    dist = calculate_distance(latitude, longitude)

    # Calculate the slope between the two points where the antennas will be placed:
    slope = slope_between_points(altitude, dist[-1])

    # Calculate the distance between the radio link endpoints and intermediate points, considering the calculated slope:
    radio_distance = radio_link_distance(slope, dist)

    # Calculate the apparent height of obstacles, the upper Fresnel radius (using distance and slope between antennas),
    # and the line connecting the antennas:
    upper_radius, line, apparent_height = line_height_fresnel_radius(n, lambda_sim, k, slope, radio_distance, altitude, dist)

    # Rotate the Fresnel radius and calculate the upper and lower Fresnel radii:
    lower_radius, upper_radius = rotate_calculate_radii(radio_distance, slope, upper_radius, line, len(altitude))

    # Calculate antenna heights. To do this, raise the antenna until it is above the apparent height of the obstacle:
    line, upper_radius, lower_radius = antenna_heights(line, upper_radius, lower_radius, len(altitude), percentage, apparent_height)

    # Power calculations:
    received_power = calculate_power(eirp, gain, dist[-1], lambda_sim)

    # Plot the final result:
    ax.clear()
    ax.plot(dist, line, color='green', label="Link")
    ax.plot(dist, upper_radius, '--', color='red', label="Fresnel Radius")
    ax.plot(dist, lower_radius, '--', color='red')
    ax.plot(dist, altitude, color='black', label="Terrain Height")
    ax.plot(dist, apparent_height, '--', color='orange', label="Apparent Terrain Height")
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    ax.grid(True)
    ax.set_xlabel('$Distance(meters)$')
    ax.set_ylabel('$Height(meters)$')
    graph.draw()
    antenna_height_label.config(text="The antenna height will be " + str(int(float(line[0]) - float(altitude[0]))) + " meters")
    received_power_label.config(text="The received power will be " + str(round(received_power, 3)) + " dBm")

# ---------------------------------------DEFINE ROOT-----------------------------------------#

root = Tk()
root.resizable(0, 0)
root.geometry("610x800")
root.title("Link Simulation")

# ------------------------------DECLARE GUI VARIABLES---------------------------------#

directory = StringVar()
fresnelN = IntVar()
fresnel_percentage = DoubleVar()
lambda_simulation = DoubleVar()
factorK = DoubleVar()
antenna_gain = DoubleVar()
eirp_antenna = DoubleVar()

# -----------------------DECLARE FRAME ----------------#

simulation_frame = Frame(root, width=400, height=300)
simulation_frame.pack(side="top", fill="x")

# ---------------------FILE SELECTION GUI------------------#

title_selection = Label(simulation_frame, text="SIMULATION")
title_selection.grid(row=0, column=0, padx=5, pady=5, columnspan=5)
title_selection.config(font=("MS PMincho", 15), justify="center")

file_path_label = Label(simulation_frame, text="Path: ").grid(row=1, column=0, sticky="e", padx=5, pady=10)
file_path_entry = Entry(simulation_frame, width=50, textvariable=directory).grid(row=1, column=1, padx=5, pady=5, columnspan=3)
file_button = Button(simulation_frame, text="Select", width=10, command=browse_file).grid(row=1, column=4, padx=5, pady=5, columnspan=4)

# --------------------PARAMETER INPUT GUI-----------------#

fresnel_radius_label = Label(simulation_frame, text="Fresnel Radius (n):").grid(row=2, column=0, sticky="e", pady=5)
fresnel_radius_entry = Entry(simulation_frame, textvariable=fresnelN).grid(row=2, column=1, pady=5)

lambda_label = Label(simulation_frame, text="Lambda (mm):").grid(row=2, column=3, sticky="e", pady=5)
lambda_entry = Entry(simulation_frame, textvariable=lambda_simulation).grid(row=2, column=4, pady=5)

percentage_radius_label = Label(simulation_frame, text="Percentage of Radius (%):").grid(row=3, column=0, sticky="e", pady=5)
percentage_radius_entry = Entry(simulation_frame, textvariable=fresnel_percentage).grid(row=3, column=1, pady=5)

factorK_label = Label(simulation_frame, text="Correction Factor K:").grid(row=3, column=3, sticky="e", pady=5)
factorK_entry = Entry(simulation_frame, textvariable=factorK).grid(row=3, column=4, pady=5)

antenna_gain_label = Label(simulation_frame, text="Antenna Gain (dBi):").grid(row=4, column=0, sticky="e", pady=5)
antenna_gain_entry = Entry(simulation_frame, textvariable=antenna_gain).grid(row=4, column=1, pady=5)

EIRP_label = Label(simulation_frame, text="EIRP (dBm):").grid(row=4, column=3, sticky="e", pady=5)
EIRP_entry = Entry(simulation_frame, textvariable=eirp_antenna).grid(row=4, column=4, pady=5)

calculate_button = Button(simulation_frame, text="Calculate Simulation", width=30, command=activate_simulation).grid(row=5, column=0, padx=5, pady=5, columnspan=5)

# ----------------------ADD GRAPH TO GUI----------------------------#

figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
ax.grid(True)
ax.set_xlabel('$Distance(m)$')
ax.set_ylabel('$Height(m)$')
graph = FigureCanvasTkAgg(figure, simulation_frame)
graph.get_tk_widget().grid(row=6, column=0, padx=5, columnspan=5)

# ----------------------DISPLAY GRAPH DATA IN GUI----------------------------#

antenna_height_label = Label(simulation_frame, text="The antenna height will be 0 meters")
antenna_height_label.config(font="Verdana 8 bold")
antenna_height_label.grid(row=7, column=0, columnspan=2)

received_power_label = Label(simulation_frame, text="The received power will be 0 dBm")
received_power_label.config(font="Verdana 8 bold")
received_power_label.grid(row=7, column=3, columnspan=2)

root.mainloop()