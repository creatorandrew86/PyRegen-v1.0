'''
------------------------------------------------------------------------------------------------------------------------------------------
                                                PYREGEN RUN -- INTERFACE -- RUN MODULE
    
                                                
    This is the main module of the PyRegen algorithm -- Interface and Short Output
    The main calculation algorithms are found in the Geometry Generation and PyRegen modules respectively.

    For more information about the software check the README file!!!

------------------------------------------------------------------------------------------------------------------------------------------

'''
# --------------------------------------------------------------------------------------------------------------------------------------
#   Licensing
#   The follwing is distributed in every Module:
#
#
#  PyRegen RUN.py
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
import tkinter as tk
import os
import CoolProp.CoolProp as CP
import numpy as np
from tkinter import ttk, filedialog, messagebox

#Global values declaration
global step_data, segment_data


#Import Auxiliary Modules
import ModuleProcessInputs
import ModuleGeometryGeneration
import ModulePropellants
import ModuleStepGeometry
import ModuleSegmentGeometry
import ModulePyRegen
import ModuleOutput
from ModuleDataStore import step_data, segment_data


#Global variables, booleans...
global scriptDir, nozzleType, injPsi_var, x_points, y_points, tab3
injPsi_var = 0
points_filepath, wall_k_entry = None, None
scriptDir = os.path.dirname(os.path.abspath(__file__))


nozzleType, calculate_var = None, False

''' ********************* CONICAL NOZZLE ********************* '''
def ConicalValues():
    global nozzleType
    nozzleType = 1

    #Open the nozzle angle entry and make sure the nozzle length entry is closed
    alpha_entry.config(state='normal')
    NozzleLength_entry.config(state='disabled')

    #Checkbox untick
    checkbox_parabola_var.set(0)
    upload_var.set(0)


''' ********************* BELL NOZZLE ********************* '''
def BellValues():
    global nozzleType
    nozzleType = 0

    #Open the nozzle length input
    NozzleLength_entry.config(state='normal')
    alpha_entry.config(state='disabled')

    #Checkbox untick
    checkbox_conical_var.set(0)
    upload_var.set(0)




''' ********************* UPLOAD NOZZLE ********************* '''
def UploadPoints():
    global nozzleType, points_filepath
    nozzleType = 2

    #Close the nozzle angle/length entries
    alpha_entry.config(state='disabled')
    NozzleLength_entry.config(state='disabled')

    #Ask the user to upload the points file path
    points_filepath = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    #Checkbox untick
    checkbox_parabola_var.set(0)
    checkbox_conical_var.set(0)



''' ********************* CHOOSE "Rt" OR "MFR" ********************* '''
def RtValues():
    #If "Throat Radius" selected, enable it (and unit)
    throat_radius.config(state = 'normal')
    throat_radius_units_box.config(state = 'normal')

    #Disable the "Mass Flow Rate" input (and unit) and set it to 0
    mass_flux.config(state = 'disabled')
    mass_flux_units_box.config(state = 'disabled')
    mfrValues_var.set(0)


def mfrValues():
    #If "Mass Flow Rate" is selected, enable it (and unit)
    mass_flux.config(state = 'normal')
    mass_flux_units_box.config(state = 'normal')

    #Disable the "Throat Radius" input (and unit) and set it to 0
    throat_radius.config(state = 'disabled')
    throat_radius_units_box.config(state = 'disabled')
    RtValues_var.set(0)



''' ********************* THERMAL CONDUCTIVITY INPUT ********************* '''
def Inputk(event = None):
    global wall_k_entry

    #Show interface entry for "Custom' 
    if mat_combobox.get() == 'Custom':
        ttk.Label(tab3, text='Thermal Conductivity:').grid(column=3, row=1, padx=5, pady=5, sticky='W')
        wall_k_entry = ttk.Entry(tab3)
        wall_k_entry.grid(column=4, row=1, padx=5, pady=5, sticky='W')






''' ****************************** INITIALIZE INTERFACE || CREATE TABS ****************************** '''
# Set up the Tkinter window
root = tk.Tk()
root.title('PyRegen')
root.geometry('700x370')


# Create the notebook
notebook = ttk.Notebook(root)

# Create frames
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

# Add tabs
notebook.add(tab1, text='CEA/Geometry')
notebook.add(tab2, text='Coolant Inlet')
notebook.add(tab3, text='Channel Geometry/Solver')

# Pack the notebook
notebook.pack(expand=True, fill='both')


#Generate the buttons for channel geometry generation
stepped_button = ttk.Button(tab3, text='Stepped', command = lambda: func_create_step(0))
stepped_button.grid(column=0, row=1, padx=5, pady=5, sticky='W')

segmented_button = ttk.Button(tab3, text='Smoothen', command = lambda: func_create_seg(0))
segmented_button.grid(column=1, row=1, padx=5, pady=5, sticky='W')

#Initialize the 'var' values and lists for windows
stepped_channel_var, smooth_channel_var = False, False



'''
    ****************************************************************************************************************
                                            COOLING CHANNEL GEOMETRY INPUT
    ****************************************************************************************************************
'''


def func_create_step(step_number = None):
    global step_data, stepped_channel_var, smooth_channel_var, segmented_button
    
    #Set the stored information about the channel geometry
    stepped_channel_var = True
    smooth_channel_var = False

    segmented_button.config(state='disabled')

    ModuleStepGeometry.create_step(root, tab3, step_number, segmented_button)



def func_create_seg(seg_number = None):
    global segment_data, stepped_channel_var, smooth_channel_var, stepped_button

    #Set the stored information about the channel geometry
    stepped_channel_var = False
    smooth_channel_var = True

    stepped_button.config(state='disabled')

    ModuleSegmentGeometry.create_seg(root, tab3, seg_number, stepped_button)



'''
    ***********************************************************************************************************
                                                    MAIN FUNCTION
    ***********************************************************************************************************
'''



def mainFunction():
    #Global Variables/Lists for Functions
    global nozzleType, injPsi_var, wall_k_entry, calculate_var, stepped_channel_var, smooth_channel_var, points_filepath
    global x_points, y_points, step_data, segment_data, mainOutput_args


    #Set the boolean to true if the main function runs
    calculate_var = True


    '''
        ******************************************************************************************************
                                            INPUTS AND GEOMETRY GENERATION
        ******************************************************************************************************      
    '''

    #PyRegen Data Output array || Initialization
    data_array = np.empty((0, 15))

    # Create list of entries || Ttk values containing the values set by the user
    # The list is reinitialized for every iteration of the 
    entries_list = [FuelTemp_entry, OxTemp_entry, chamber_pressure, mixture_ratio, contraction_ratio, throat_radius, mass_flux, char_length, 
                    eps_entry, coolant_pressure, coolant_temp, coolant_mfr_entry, coolant_entry_point, coolant_exit_point, number_it, RtValues_var]


    #Append units to entries list:
    entries_list.extend([
        FuelTemp_units_box.get(),
        OxTemp_units_box.get(),
        chamber_pressure_units_box.get(),
        throat_radius_units_box.get(),
        mass_flux_units_box.get(),
        char_length_units_box.get(),
        coolant_pressure_units_box.get(),
        coolant_temp_units_box.get(),
        coolant_mfr_units_box.get(),
        coolant_entry_point_units_box.get(),
        coolant_exit_point_units_box.get()
    ])



    # Combobox values (Oxidizer, Fuel, Wall Material, Coolant) fetching
    coolant = coolant_combobox.get()                                                    # Coolant definiton

    # Propellants
    Ox = ox_combobox.get()                                                              # Oxidizer definition
    Fuel = 'A50' if fuel_combobox.get() == 'Aerozine 50' else fuel_combobox.get()       # Fuel definition
    wall_material = mat_combobox.get()                                                  # Chamber wall material definition


    # Inputs Fetching Function Execution
    inputs_list = ModuleProcessInputs.process_inputs(entries_list)
    FuelTemp, OxTemp, Pc, MR, CR, eps, it_number, charLength, Rt, eng_mass_flux, coolant_P, coolant_T, coolant_mfr, x_initial, x_final, input_error = inputs_list

    # Return the main function if the input processor detects an input missing
    if input_error:
        return

    #Geometry generator module arguments list
    geometry_entries_list = [NozzleLength_entry, alpha_entry, RtValues_var, mfrValues_var]

    geometry_generator_args = [CR, Pc, MR, charLength, eps, Ox, Fuel, it_number, x_initial, x_final, OxTemp, FuelTemp, Rt, eng_mass_flux,
                               geometry_entries_list, nozzleType, points_filepath]
    



    #Coolant entry enthalpy from temperature, show Coolprop error if any
    try:
        coolant_H = CP.PropsSI('H', 'T', coolant_T, 'P', coolant_P, coolant)  # Fuel Entry Enthalpy
    except Exception as e:
        print(e)
        return
    

    
    #Check the throat dimensions inputs
    if RtValues_var.get() == 0 and  mfrValues_var.get() == 0:
        messagebox.showerror('Error', 'Input throat radius or nozzle mass flux')
        return


    c, geometry_list, i_initial, i_final, CEA_Ox, CEA_Fuel, m_dot, v_exit = ModuleGeometryGeneration.geometry_generator(geometry_generator_args)


    #Unpack the geometry list
    x_points, y_points, eps_list, Rt = geometry_list


    #Define Combustion temperature (deg R to K) and the main output list
    Tc = c.get_Tcomb(Pc=Pc, MR=MR) / 1.8
    mainOutput_args = [CEA_Ox, CEA_Fuel, Pc, MR, eps, Rt, charLength, CR, coolant, coolant_mfr, Tc, v_exit, m_dot]

    #Update geometry list with "CR" and initial/final stations || List preparation for arguments of PyRegen
    #See ModulePyRegen for detail regarding inputs
    geometry_list.extend([CR, i_initial, i_final, charLength])
    coolant_init_list = [coolant_H, coolant_P, coolant, coolant_mfr] 
    cea_list = [Pc, MR, eps, wall_material]
    channel_geometry_list = [smooth_channel_var, stepped_channel_var, segment_data, step_data, wall_k_entry]
    output_list = [data_array, mainOutput_args]

    #Arrange PyRegen Args list:
    PyRegen_args = [geometry_list, coolant_init_list, cea_list, channel_geometry_list, output_list]



    ''' *************************************** PYREGEN FUNCTION EXECUTION *************************************** '''
    short_output_args, data_array, data_map, mainOutput_args = ModulePyRegen.PyRegen_func(PyRegen_args, c)

    #Main Function return
    return short_output_args, data_map


'''
    **************************************************************************************************************************
                                                            SHORT PROGRAM OUTPUT
    **************************************************************************************************************************
'''

#Number of times the main function has run
global run_counter, run_outputs, data_map
run_counter, run_outputs = 0, []

def execute_PyRegen():
    global run_counter, tab3, data_map, new_data_map
    run_counter += 1

    import time

    #Get the results and time the function execution
    start_time = time.time()
    short_output_args, data_map = mainFunction()
    end_time = time.time()
    
    #Calculate the time difference and append it to the output arguments list
    delta_time = round(end_time - start_time, 2)
    short_output_args.append(delta_time)


    #Run the function to show the outputs
    ModuleOutput.show_output(root, short_output_args)


    #Add the current (> 1) run to the values for plotting and the short output lists to the data map
    run_outputs.append(data_map)
    new_data_map = data_map
    if run_counter > 1:
        y2_options.append(f'Run {run_counter - 1}')
        new_data_map[f'Run {run_counter - 1}'] = run_outputs[run_counter - 2]

        y2_combobox['values'] = y2_options




'''
    ************************************************************************************************************************
                                                             USER INTERFACE
    ************************************************************************************************************************
'''

#Lists for the Oxidizer, Fuel and Coolant

coolant_list = ['Water', 'Methane', 'Ammonia', 'Ethane', 'Ethanol', 'R134a', 'Hydrogen', 'Methanol', 'n-Butane', 'Ethanol', 'Ethylene', 
                'Fluorine', 'n-Decane', 'n-Hexane', 'n-Nonane', 'n-Octane', 'n-Pentane', 'n-Propane', 'n-Undecane']

ox_list = ['LOX', 'Peroxide90', 'Peroxide 98', 'O2', 'AIR', 'F2', 'H2O2', 'HNO3', 'IRFNA', 'MON25','MON3', 'N2O', 'N2O4']

fuel_list = ['CH4', 'RP1', 'H2', 'C2H6', 'C4H10', 'C3H8', 'Aerozine 50', 'B2H6', 'C2H2', 'Gasoline', 
             'Kerosene90_H2O10', 'LH2', 'MMH', 'UDMH', 'NITROMETHANE', 'Methanol', 'N2H4', 'NH3']


#Units lists || Entries list initialization

pressure_units = ['bar', 'atm', 'kPa', 'psi']
temperature_units = ['K', 'C', 'F', 'R']
length_units = ['m', 'cm', 'in', 'ft']
mass_flow_units = ['kg/s', 'lb/s', 'oz/s']


#Checkboxes variables
checkbox_conical_var = tk.IntVar()
checkbox_parabola_var = tk.IntVar()
upload_var = tk.IntVar()
RtValues_var = tk.IntVar()
mfrValues_var = tk.IntVar()
injPsi_v = tk.IntVar()

#Nozzle options: 1-Conical 2-Bell 3-Upload points
checkbox_conical = ttk.Checkbutton(tab1, text='Conical Nozzle', variable=checkbox_conical_var, command = ConicalValues)
checkbox_conical.grid(column=3, row=6, padx=5, pady=5, sticky='W')


checkbox_parabola = ttk.Checkbutton(tab1, text='Bell Nozzle', variable=checkbox_parabola_var, command = BellValues)
checkbox_parabola.grid(column=3, row=7, padx=5, pady=5, sticky='W')


checkbox_upload = ttk.Checkbutton(tab1, text='Upload points file', variable=upload_var, command = UploadPoints)
checkbox_upload.grid(column=3, row=8, padx=5, pady=5, sticky='W')
                 


''' ************************************ CEA INPUTS || TAB 1 ************************************ '''



#Fuel Entry
fuel_options = fuel_list
fuel_combobox = ttk.Combobox(tab1, values=fuel_options)
fuel_combobox.grid(column=0, row=2, padx=5, pady=5)
fuel_combobox.set('CH4')

#Fuel Temperature Entry
ttk.Label(tab1, text='*T:').grid(column=1, row=2, padx=1, pady=1, sticky='W')
FuelTemp_entry = ttk.Entry(tab1, width=5)
FuelTemp_entry.grid(column=1, row=2, padx=20, pady=1, sticky='W')

#Fuel Temperature Unit
FuelTemp_units_box = ttk.Combobox(tab1, values=temperature_units, width=3)
FuelTemp_units_box.grid(column=1, row=2, padx=70, pady=5, sticky='W')
FuelTemp_units_box.set('K')


#Oxidizer Entry
ox_options = ox_list
ox_combobox = ttk.Combobox(tab1, values=ox_options)
ox_combobox.grid(column=0, row=1, padx=5, pady=5)
ox_combobox.set('LOX')

#Oxidizer Temperature Entry
ttk.Label(tab1, text='*T:').grid(column=1, row=1, padx=1, pady=1, sticky='W')
OxTemp_entry = ttk.Entry(tab1, width=5)
OxTemp_entry.grid(column=1, row=1, padx=20, pady=1, sticky='W')

#Fuel Temperature Unit
OxTemp_units_box = ttk.Combobox(tab1, values=temperature_units, width=3)
OxTemp_units_box.grid(column=1, row=1, padx=70, pady=5, sticky='W')
OxTemp_units_box.set('K')



#CEA card oxidizer/fuel buttons
CustomOxidizer_button = ttk.Button(tab1, text='Custom Oxidizer', command = lambda: ModulePropellants.CustomOxidizer(root))
CustomOxidizer_button.grid(column=0, row=6, padx=5, pady=5, sticky='W')

CustomFuel_button= ttk.Button(tab1, text='Custom Fuel', command = lambda: ModulePropellants.CustomFuel(root))
CustomFuel_button.grid(column=0, row=5, padx=5, pady=5, sticky='W')


#Chamber Pressure Entry
ttk.Label(tab1, text='Chamber Pressure (bar):').grid(column=0, row=3, padx=5, pady=5, sticky='W')
chamber_pressure = ttk.Entry(tab1, width=10)
chamber_pressure.insert(0, '100')
chamber_pressure.grid(column=1, row=3, padx=5, pady=5, sticky='W')

#Chamber Pressure Unit Entry
chamber_pressure_units_box = ttk.Combobox(tab1, values=pressure_units, width=5)
chamber_pressure_units_box.grid(column=1, row=3, padx=80, pady=5, sticky='W')
chamber_pressure_units_box.set('bar')



#Mixture Ratio Entry
ttk.Label(tab1, text='Mixture Ratio:').grid(column=0, row=4, padx=5, pady=5, sticky='W')
mixture_ratio = ttk.Entry(tab1)
mixture_ratio.insert(0, '3.6')
mixture_ratio.grid(column=1, row=4, padx=5, pady=6, sticky='W')

ttk.Label(tab1, text = 'CEA Inputs').grid(column=0, row=0, padx=5, pady=5, sticky='W')
ttk.Label(tab1, text = 'Note: * means optional value.').grid(column=0, row=7, padx=5, pady=5, sticky='W')





''' ************************************ NOZZLE GEOMETRY INPUTS || TAB 1 ************************************ '''





ttk.Label(tab1, text='Geometric Parameters').grid(column=3, row=0, padx=5, pady=5, sticky='W')


# Contraction Ratio Entry
ttk.Label(tab1, text='Contraction Ratio(Ac/At):').grid(column=3, row=1, padx=5, pady=5, sticky='W')
contraction_ratio = ttk.Entry(tab1)
contraction_ratio.insert(0, '3')
contraction_ratio.grid(column=4, row=1, padx=5, pady=5, sticky='W')


# Throat Radius Entry
ThroatRadius = ttk.Checkbutton(tab1, text='Throat Radius (cm): ', variable=RtValues_var, command=RtValues)
ThroatRadius.grid(column=3, row=3, padx=5, pady=5, sticky='W')

throat_radius = ttk.Entry(tab1, width=10)
throat_radius.insert(0, '4.5')
throat_radius.config(state='disabled')
throat_radius.grid(column=4, row=3, padx=5, pady=5, sticky='W')

# Throat Radius Units
throat_radius_units_box = ttk.Combobox(tab1, values=length_units, width=5) 
throat_radius_units_box.grid(column=4, row=3, padx=80, pady=5, sticky='W')
throat_radius_units_box.set('cm')
throat_radius_units_box.config(state='disabled')




# Mass Flow Rate Entry
MassFlux = ttk.Checkbutton(tab1, text='Design Mass Flux (kg/s):', variable=mfrValues_var, command=mfrValues)
MassFlux.grid(column=3, row=4, padx=5, pady=5, sticky='W')

mass_flux = ttk.Entry(tab1, width=10)
mass_flux.insert(0, '0')
mass_flux.config(state='disabled')
mass_flux.grid(column=4, row=4, padx=5, pady=5, sticky='W')


# Mass Flow Rate Unit
mass_flux_units_box = ttk.Combobox(tab1, values=mass_flow_units, width=5)  
mass_flux_units_box.grid(column=4, row=4, padx=80, pady=5, sticky='W')
mass_flux_units_box.set('kg/s')
mass_flux_units_box.config(state='disabled')



# Characteristic Length Entry
ttk.Label(tab1, text='Characteristic Length (cm):').grid(column=3, row=5, padx=5, pady=3, sticky='W')
char_length = ttk.Entry(tab1, width=10)
char_length.insert(0, '80')
char_length.grid(column=4, row=5, padx=5, pady=5, sticky='W')


# Characteristic Length Unit
char_length_units_box = ttk.Combobox(tab1, values=length_units, width=5) 
char_length_units_box.grid(column=4, row=5, padx=80, pady=5, sticky='W')
char_length_units_box.set('cm')


# Nozzle Area Ratio Entry
ttk.Label(tab1, text='Nozzle Area Ratio(Ae/At):').grid(column=3, row=2, padx=5, pady=5, sticky='W')
eps_entry = ttk.Entry(tab1)
eps_entry.insert(0, '10')
eps_entry.grid(column=4, row=2, padx=5, pady=5, sticky='W')



# Nozzle Angle Entry | Conical Nozzle
ttk.Label(tab1, text='Nozzle Angle:').grid(column=4, row=6, padx=1, pady=1, sticky='W')
alpha_entry = ttk.Entry(tab1, width=5)
alpha_entry.insert(0,  '15')
alpha_entry.config(state='disabled')
alpha_entry.grid(column=4, row=6, padx=80, pady=1, sticky='W')


# Nozzle Length Entry | Bell Nozzle
ttk.Label(tab1, text='Nozzle Length(%):').grid(column=4, row=7, padx=1, pady=1, sticky='W')
NozzleLength_entry = ttk.Entry(tab1, width=5)
NozzleLength_entry.insert(0, '80')
NozzleLength_entry.config(state='disabled')
NozzleLength_entry.grid(column=4, row=7, padx=100, pady=1, sticky='W')





''' *************************************** COOLANT INLET CONDITION || TAB 2 *************************************** '''





ttk.Label(tab2, text='Coolant Definition').grid(column=0, row=0, padx=5, pady=10,  sticky='W')


#Coolant
ttk.Label(tab2, text='Coolant:').grid(column=0, row=1, padx=5, pady=5, sticky='W')
coolant_combobox = ttk.Combobox(tab2, values=coolant_list)
coolant_combobox.grid(column=1, row=1, padx=20, pady=5)
coolant_combobox.set('Methane')


# Coolant Inlet Pressure
ttk.Label(tab2, text='Coolant Pressure:').grid(column=0, row=2, padx=5, pady=5, sticky='W')
coolant_pressure = ttk.Entry(tab2, width=10)
coolant_pressure.insert(0, '150')
coolant_pressure.grid(column=1, row=2, padx=5, pady=5, sticky='W')

# Coolant Inlet Pressure Unit
coolant_pressure_units_box = ttk.Combobox(tab2, values=pressure_units, width=5)  
coolant_pressure_units_box.grid(column=1, row=2, padx=80, pady=5, sticky='W')
coolant_pressure_units_box.set('bar')



# Coolant Temperature
ttk.Label(tab2, text='Coolant Temperature:').grid(column=0, row=3, padx=5, pady=5, sticky='W')
coolant_temp = ttk.Entry(tab2, width=10)
coolant_temp.insert(0, '120')
coolant_temp.grid(column=1, row=3, padx=5, pady=5, sticky='W')

# Coolant Temperature Unit
coolant_temp_units_box = ttk.Combobox(tab2, values=temperature_units, width=5) 
coolant_temp_units_box.grid(column=1, row=3, padx=80, pady=5, sticky='W')
coolant_temp_units_box.set('K')



# Coolant Mass Flow Rate
ttk.Label(tab2, text='Coolant Mass Flow Rate:').grid(column=0, row=4, padx=5, pady=5, sticky='W')
coolant_mfr_entry = ttk.Entry(tab2, width=10)
coolant_mfr_entry.insert(0, '7')
coolant_mfr_entry.grid(column=1, row=4, padx=5, pady=5, sticky='W')

# Coolant Mass Flow Rate Unit
coolant_mfr_units_box = ttk.Combobox(tab2, values=mass_flow_units, width=5)  
coolant_mfr_units_box.grid(column=1, row=4, padx=80, pady=5, sticky='W')
coolant_mfr_units_box.set('kg/s')



ttk.Label(tab2, text='Cooling Jacket Definition:').grid(column=0, row=6, padx=5, pady=10, sticky='W')



# Inlet Location
ttk.Label(tab2, text='Coolant Entry (Distance from IP):').grid(column=0, row=7, padx=5, pady=5, sticky='W')
coolant_entry_point = ttk.Entry(tab2, width=10)
coolant_entry_point.insert(0, '0.5')
coolant_entry_point.grid(column=1, row=7, padx=5, pady=5, sticky='W')

# Inlet Location Unit
coolant_entry_point_units_box = ttk.Combobox(tab2, values=length_units, width=5)  
coolant_entry_point_units_box.grid(column=1, row=7, padx=80, pady=5, sticky='W')
coolant_entry_point_units_box.set('m')



# Outlet Location
ttk.Label(tab2, text='Coolant Exit (Distance from IP):').grid(column=0, row=8, padx=5, pady=5, sticky='W')
coolant_exit_point = ttk.Entry(tab2, width=10)
coolant_exit_point.insert(0, '0.2')
coolant_exit_point.grid(column=1, row=8, padx=5, pady=5, sticky='W')

# Outlet Location Unit
coolant_exit_point_units_box = ttk.Combobox(tab2, values=length_units, width=5)  
coolant_exit_point_units_box.grid(column=1, row=8, padx=80, pady=5, sticky='W')
coolant_exit_point_units_box.set('m')



#Number of stations along the nozzle
ttk.Label(tab2, text='Number of Stations:').grid(column=0, row=9, padx=5, pady=5, sticky='W')
number_it = ttk.Entry(tab2)
number_it.insert(0, '140')
number_it.grid(column=1, row=9, padx=2, pady=5, sticky='W')

#Warning
warning = ttk.Label(tab2, text='IP = Injector Plate').grid(column=0, row=10, padx=5, pady=5, sticky='W')




#Button to get the nozzle length
ttk.Button




#Separators
ttk.Separator(tab3, orient='horizontal').grid(column=3, row=4, columnspan=3, pady=5, sticky='ew')
ttk.Separator(tab3, orient='vertical').grid(column=2, row=0, rowspan=7, padx=5, sticky='ns')
ttk.Separator(tab2, orient='horizontal').grid(column=0, row=5, columnspan=2, pady=7, sticky='ew')






''' ************************************* SOLVER || TAB 3 ************************************* '''


#Tab 3 Labels/Spacer
ttk.Label(tab3, text=' ').grid(column=3, row=1, sticky='W')
ttk.Label(tab3, text='Cooling Channel Geometry').grid(column=0, row=0, padx=5, pady=5, sticky='W')
ttk.Label(tab3, text='Solver Control:').grid(column=3, row=3, padx=5, pady=5, sticky='W')
ttk.Label(tab3, text='Select Values/Solver Runs to Plot:').grid(column=3, row=5, padx=5, pady=5, sticky='W')
ttk.Label(tab3, text='PyRegen Output').grid(column=3, row=7, padx=5, pady=5, sticky='W')
ttk.Label(tab3, text='Nozzle Geometry/CEA').grid(column=4, row=7, padx=5, pady=5, sticky='W')

# Note to check the README file
ttk.Label(tab3, text='Check the README file in the Github repository on how to fill the Channel Geometry entries!').grid(
    column=0, columnspan=5, row=10, padx=5, pady=25, sticky='sw'
)


#Options for graph plotting
y1_options = ['Tl', 'Twl', 'Twg', 'hg', 'hl', 'u']
y1_combobox = ttk.Combobox(tab3, values=y1_options)
y1_combobox.grid(column=3, row=6, padx=5, pady=5)
y1_combobox.set('Twg')


y2_options = ['-', 'Tl', 'P', 'Twl', 'Twg', 'hg', 'hl', 'u', 'y']
y2_combobox = ttk.Combobox(tab3, values=y2_options)
y2_combobox.grid(column=4, row=6, padx=5, pady=5)
y2_combobox.set('-')


#Wall material and thermal conductivity
ttk.Label(tab3, text='Wall Material:').grid(column=3, row=0, padx=5, pady=5, sticky='W')
mat_options = ['Copper', 'GRCop 42', 'GRCop 84', 'NARloy Z', 'Custom']
mat_combobox = ttk.Combobox(tab3, values=mat_options)
mat_combobox.grid(column=4, row=0, padx=5, pady=5)
mat_combobox.set('Wall Material')

mat_combobox.bind('<<ComboboxSelected>>', Inputk)



#Button for Short Output
short_output = ttk.Button(tab3, text = 'PyRegen Run', command = execute_PyRegen)
short_output.grid(column=3, row=8, padx=5, pady=5, sticky='W')

#Button for saving output
save_output = ttk.Button(tab3, text = 'Save Output File', command = lambda: ModuleOutput.print_file(calculate_var, mainOutput_args))
save_output.grid(column=3, row=9, padx=5, pady=5, sticky='W')

#Button to plot graph
plotdata_button = ttk.Button(tab3, text = 'Plot Graph', command = lambda: ModuleOutput.plot_data(calculate_var, data_map, new_data_map, run_counter, y1_combobox, y2_combobox))
plotdata_button.grid(column=4, row=9, padx=5, pady=5, sticky='W')

#Button to plot the nozzle points
plot_button = ttk.Button(tab3, text = 'Plot Nozzle',command = lambda: ModuleOutput.plot_nozzle(calculate_var, x_points, y_points))
plot_button.grid(column=4, row=8, padx=5, pady=5, sticky='W')

# Run the Tkinter event loop
root.mainloop()
