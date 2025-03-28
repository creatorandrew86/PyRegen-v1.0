
#  ModuleOutput.py
#  Author : Andrew Toma
#  Version 1.0 "PyRegen"
#
#  Note: The following "PyRegen" mentionas refer to the v1.0, the free version
#
#  PyRegen Project Website: [https://github.com/creatorandrew86/PyRegen-v1.0]
#
#  The PyRegen project is maintained by the author
#  (https://github.com/creatorandrew86/PyRegen-v1.0)
#
#  Copyright 2025, PyRegen Contributors 
#  - Andrew Toma (https://github.com/creatorandrew86) -- Solo Developer
#
#  PyRegen is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  PyRegen is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public
#  License along with PyRegen. If not, see <http://www.gnu.org/licenses/>.

# -- Imports --
import math, tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox, filedialog, ttk


''' ***************************************************** SHOW SHORT OUTPUT ***************************************************** '''

def show_output(root, short_output_args):
    max_Twg, max_Qflux, final_P, final_T, delta_time = short_output_args

    #Initiate the output window
    results_window = tk.Toplevel(root)
    results_window.title('Main Program Output')

    #Add all the values to the window
    ttk.Label(results_window, text=f'PyRegen Run Time (s): {delta_time}').grid(column=0, row=0, padx=5, pady=5, sticky='W')
    ttk.Label(results_window, text=f'Maximum Hot Wall Temperature (K): {max_Twg}').grid(column=0, row=1, padx=5, pady=5, sticky='W')
    ttk.Label(results_window, text=f'Maximum Heat Flux (kW/m^2): {max_Qflux}').grid(column=0, row=2, padx=5, pady=5, sticky='W')
    ttk.Label(results_window, text=f'Coolant Outlet Temperature: {final_T}').grid(column=0, row=3, padx=5, pady=5, sticky='W')
    ttk.Label(results_window, text=f'Coolant Outlet Pressure (bar): {final_P}').grid(column=0, row=4, padx=5, pady=5, sticky='W')
    
    

''' ***************************************************** PLOT NOZZLE POINTS ***************************************************** '''


def plot_nozzle(calculate_var, x_points, y_points):

    #Check if the main function ran:
    if  not calculate_var:
        messagebox.showerror('Error', 'Press the "Calculate" button first, to generate the results')
        return

    #Plot the results:
    plt.figure(figsize=(7, 7))                                                              # Initiate the figure
    plt.plot(x_points, y_points, linestyle='-', color='black', label='Nozzle Contour')      # x and y axis, linestyle and color, label

    plt.title('Nozzle Contour')                                                             # Plot title
    plt.xlabel('x(cm)')                                                                     # x-axis label
    plt.ylabel('y(cm)')                                                                     # y-axis label
    plt.axis('equal')                                                                       # Set equal axis
    plt.legend()                                                                            # Set legend
    plt.grid(False)                                                                         # Set no grid

    #Show the plot
    plt.show()


''' ***************************************************** PLOT PYREGEN OUTPUT DATA ***************************************************** '''


def plot_data(calculate_var, data_map, new_data_map, run_counter, y1_combobox, y2_combobox):

    #Get "show_X" from data_map
    show_x = data_map['x']

    #Check if the main function ran
    if not calculate_var:
        messagebox.showerror('Error', 'Press the "Calculate" button first, to generate the results')
        return
    

    option_1 = y1_combobox.get()                        # Get the first option
    y_val1 = data_map[option_1]                         # Assign a value from 'data_map'
    
    option_2 = y2_combobox.get()                        # Get the second option
    fig, ax1 = plt.subplots(figsize=(10, 5))            # Create a figure and the first axis (left y-axis)


    # Plot the first y-axis data on the left
    ax1.plot(show_x, y_val1, linestyle='-', color='b', label=option_1)
    ax1.set_xlabel('x (cm)')
    ax1.set_ylabel(f'{option_1}', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Second axis definition if the second option is validated
    if option_2 != '-':
        ax2 = ax1.twinx()

    # If the second option is not 'Nothing', create a second axis (right y-axis)
    if option_2 in ['Tl', 'P', 'Twl', 'Twg', 'hg', 'hl', 'u', 'y']:
        y_val2 = data_map[option_2]         # Assign a value from 'data_map'


        # Plot the second y-axis data on the right
        ax2.plot(show_x, y_val2, linestyle='-', color='r')
        ax2.set_ylabel(f'{option_2}', color='r')
        ax2.tick_params(axis='y', labelcolor='r')



    if run_counter > 1:
        for i in range(1, run_counter):
            if option_2 == f'Run {i}':
                y_val2 = new_data_map[option_2][option_1]

                # Make the plot of the second axis
                ax2.set_ylabel(f'Run {i} {option_1}', color='r')
                ax2.tick_params(axis='y', labelcolor='r')
                ax2.plot(show_x, y_val2, linestyle='-', color='r')

                # Equally size the plots
                ax1.set_ylim(0.9 * min(min(y_val1), min(y_val2)), 1.1 * max(max(y_val1), max(y_val2)))
                ax2.set_ylim(0.9 * min(min(y_val1), min(y_val2)), 1.1 * max(max(y_val1), max(y_val2)))


    # Set the title, grid, and legend
    if option_2 == '-':
        title = f'Plot of {option_1} vs x'
    else:
        title = f'Plot of {option_1} and {option_2} vs x'
        
    plt.title(title)
    ax1.grid(True)  # Apply grid to the first axis

    # Show the plot
    plt.show()


''' ***************************************************** SAVE NOZZLE POINTS FILE ***************************************************** '''


def save_nozzle_file(calculate_var, x_points, y_points):

    #Check if the main function ran
    if not calculate_var:
        messagebox.showerror('Error', 'Press the "Calculate" button first, to generate the results')
        return
    
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".dat", filetypes=[("DAT files", "*.dat")])
        if not file_path:
            return  # User cancelled the save dialog
        
        # Open the file and write x_points and y_points
        with open(file_path, 'w') as file:
            for x, y in zip(x_points, y_points):
                file.write(f"{x} {y}\n")
        
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: \n {e}")



''' ***************************************************** SAVE MAIN OUTPUT FILE ***************************************************** '''


def print_file(calculate_var, mainOutput_args):

    #Check if the main function ran
    if not calculate_var:
        messagebox.showerror('Error', 'Press the "Calculate" button first, to generate the results')
        return
    
    #Unpack main output list
    Ox, Fuel, Pc, MR, eps, Rt, charLength, CR, coolant, mfr, Tc, v_exit, m_dot, maxTwg, maxQflux, maxhg, data_array = mainOutput_args

    ''' Extract the output data from "data_array" '''
    output_lines = []

    # Column headers
    col_headers = [
        "Station", "cw(mm)", "ch(mm)", "A/At", "T_l(K)", "P_coolant(bar)", 
        "T_wl(K)", "T_wg(K)", "velocity(m/s)", "hg(kW/m^2*K)", "Q_flux(kW/m^2)"
    ]

    # Add headers if output_lines is empty
    if not output_lines:
        header_line = '    '.join(f'{header:<10}' for header in col_headers)
        output_lines.append(header_line)
        output_lines.append('-' * len(header_line))

    # Data Appending
    for i in range(len(data_array)):
        # Extract values directly from data_array and eps_i_list
        cw = data_array[i, 11]          # cw (m)
        ch = data_array[i, 10]          # ch (m)
        eps_i = data_array[i, 13]       # A/A*
        T_l = data_array[i, 0]          # T_l (K)
        coolant_P = data_array[i, 2]    # P_coolant (bar)
        T_wl = data_array[i, 9]         # T_wl (K)
        T_wg = data_array[i, 8]         # T_wg (K)
        coolant_u = data_array[i, 3]    # velocity (m/s)
        hg = data_array[i, 6]           # hg (W/m^2*K)
        Q_flux = data_array[i, 7]       # Q_flux (W/m^2)

        # Prepare the values for output
        values = [
            i + 1,                  # Iteration (1-based index)
            cw * 1000,              # Channel width (m to mm)
            ch * 1000,              # Channel height (m to mm)
            eps_i,                  # A/A*
            T_l,                    # Coolant temperature (K)
            coolant_P,              # Coolant pressure (bar)
            T_wl,                   # Cold wall temperature (K)
            T_wg,                   # Hot wall temperature (K)
            coolant_u,              # Coolant velocity (m/s)
            hg / 1000,              # Heat transfer coefficient (gas side) (W/m^2*K to kW/m^2*K)
            Q_flux / 1000           # Heat flux (W/m^2 to kW/m^2)
        ]

        # Format the line
        line = '    '.join(f'{float(value):<10.2f}' for value in values)
        output_lines.append(line)

        # Combine output lines into a single string
        output_str = '\n'.join(output_lines)



    #Unpack lists from data array
    filename = filedialog.asksaveasfilename(defaultextension='.txt',
                                            filetypes=[('Text files', '*.txt'), ("All files", "*.*")])
    
    if filename:
        with open(filename, 'w') as file:
            file.write(" PyRegen Analysis Result\n")
            file.write("\n")
            file.write(" ***************************************************************************************************************************\n")

            #Engine Definition
            file.write("\n")
            file.write(" Engine Definition\n")
            file.write("\n")
            file.write("\n")

            file.write(f" Oxidizer : {Ox}\n")
            file.write(f" Fuel : {Fuel}\n")
            file.write(f" Chamber Pressure = {Pc/14.7} bar\n")
            file.write(f" Mixture Ratio = {MR}\n")
            file.write(f" Ae/A* = {eps}\n")
            file.write(f" Throat Radius = {Rt} cm\n")
            file.write(f" Characteristic Length = {charLength * CR} cm\n")
            file.write("\n")
            file.write(f" Coolant : {coolant}\n")
            file.write(f" Coolant Mass Flow Rate = {mfr} kg/s\n")
            file.write(f" Coolant Inlet Temperature = {round(float(data_array[0, 0]), 1)} K\n")
            file.write(f" Coolant Inlet Temperature = {data_array[0, 2]} bar\n")

            #CEA Short Output
            file.write("\n")
            file.write("\n")
            file.write(" Short CEA Output\n")
            file.write("\n")
            file.write(f" Combustion Temperature = {round(Tc, 1)} K\n")
            file.write(f" Specific Impulse = {round(v_exit/9.81, 1)} s\n")
            file.write(f" Engine Mass Flow Rate = {round(m_dot, 2)} kg/s")
            file.write(f" Engine Thrust = {round(m_dot * v_exit/1000, 2)} kN \n")

            #PyRegen Short Output
            file.write("\n")
            file.write("\n")
            file.write(" Short PyRegen Output\n")
            file.write("\n")
            file.write(f" Max Hot Wall Temperature = {round(maxTwg, 2)} K\n")
            file.write(f" Coolant Outlet Temperature = {round(float(data_array[-1, 0]), 2)} K\n")
            file.write(f" Coolant Outlet Pressure = {round(data_array[-1, 2], 2)} bar\n")
            file.write(f" Maximum Wall Heat Flux = {round(maxQflux/1000, 2)} kW\n")
            file.write(f" Maximum Gas Side Heat Transfer Coefficient = {round(maxhg/1000, 2)} kW/m^2K\n")
            file.write("\n")
            file.write(f" Temperature Rise in The Channels = {round(float(data_array[-1, 0]) - float(data_array[0,  0]), 2)} K\n")
            file.write(f" Coolant Pressure Drop Through The Channels  = {round(math.fabs(data_array[-1, 2] - data_array[0, 2]), 2)} bar\n")


            #PyRegen Long Output
            file.write("\n")
            file.write(" ***************************************************************************************************************************\n")
            file.write("\n")
            file.write("\n")
            file.write("PyRegen Main Output \n")
                       
            #Write lists from the PyRegen Output          
            file.write(output_str)

            file.write("\n")



''' ***************************************************** SAVE FULL CEA OUTPUT AS FILE ***************************************************** '''


def full_cea(calculate_var, mainOutput_args):
    from rocketcea.cea_obj import CEA_Obj

    #Check if the main function ran
    if not calculate_var:
        messagebox.showerror('Error', 'Press the "Calculate" button first, to generate the results')
        return

    #Local list "args" and values fetching
    args = mainOutput_args
    Ox, Fuel, Pc, MR, eps, CR = args[0], args[1], args[2], args[3], args[4], args[7]

    #Get Full Output
    fullOutput = CEA_Obj(oxName = Ox, fuelName = Fuel, fac_CR = CR)
    full_cea = fullOutput.get_full_cea_output(Pc = Pc, MR = MR, eps = eps, pc_units = 'bar', output = 'si_units')

    #Initialize the files
    filename = filedialog.asksaveasfilename(defaultextension='.txt',
                                            filetypes=[('Text files', '*.txt'), ("All files", "*.*")])
    if filename:
        with open(filename, 'w') as file:
            file.write(full_cea)