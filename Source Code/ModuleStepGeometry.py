
#  ModuleStepGeometry.py
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
import math
import os
import tkinter as tk
from tkinter import messagebox, ttk
from ModuleDataStore import step_data

scriptDir = os.path.dirname(os.path.abspath(__file__))
global step_windows
current_steps, buttons, step_windows = [], [], []


def _show_step_error(message):
    messagebox.showerror('Step Geometry Error', message)


def _validate_step_entries(step_widgets, step_number):
    raw_values = [entry.get().strip() for entry in step_widgets]

    if any(value == '' for value in raw_values):
        _show_step_error(f'Step {step_number}: fill all fields.')
        return None

    try:
        values = [float(value) for value in raw_values]
    except ValueError:
        _show_step_error(f'Step {step_number}: use numbers only.')
        return None

    if any(not math.isfinite(value) for value in values):
        _show_step_error(f'Step {step_number}: invalid number.')
        return None

    cw, ch, step_loc, channels, thickness = values

    if cw <= 0 or ch <= 0 or thickness <= 0:
        _show_step_error(f'Step {step_number}: width, height, thickness > 0.')
        return None

    if channels <= 0 or not channels.is_integer():
        _show_step_error(f'Step {step_number}: channels must be a whole number > 0.')
        return None

    if step_loc < 0:
        _show_step_error(f'Step {step_number}: end location must be >= 0.')
        return None

    return values

def create_step(root, tab3, step_number, segmented_button):
    #Placeholder for finish/reset functions
    def placeholder():
        pass
    
    global scriptDir, step_list, step_windows



    #Location of the step window along the width of the user's screen
    window_width = 300*(step_number + 1)

    
    #Generate the step window
    step_window = tk.Toplevel(root)
    step_window.title(f' Segment {step_number + 1}')
    step_window.geometry(f'330x240+{window_width}+300')


    #Join the window in the windows list
    step_windows.append(step_window)

    ''' ***************** LABELS FOR ENTRIES **************** '''


    #Channel width
    ttk.Label(step_window, text='Channel Width (mm):').grid(column=0, row=0, padx=5, pady=5, sticky='W')
    cw_entry = ttk.Entry(step_window)
    cw_entry.grid(column=1, row=0, padx=5, pady=5, sticky='W')

    #Channel height
    ttk.Label(step_window, text='Channel Height (mm):').grid(column=0, row=1, padx=5, pady=5, sticky='W')
    ch_entry = ttk.Entry(step_window)
    ch_entry.grid(column=1, row=1, padx=5, pady=5, sticky='W')

    #Channel segment location along the nozzle
    ttk.Label(step_window, text='Step end (Distance from IP, m):').grid(column=0, row=2, padx=5, pady=5, sticky='W')
    step_loc = ttk.Entry(step_window)
    step_loc.grid(column=1, row=2, padx=5, pady=5, sticky='W')

    #Number of cooling channels
    ttk.Label(step_window, text='Number of Channels').grid(column=0, row=3, padx=5, pady=5, sticky='W')
    Ni = ttk.Entry(step_window)
    Ni.grid(column=1, row=3, padx=5, pady=5,  sticky='W')

    #Cooling channel thickness
    ttk.Label(step_window, text='Wall thickness (mm)').grid(column=0, row=4, padx=5, pady=5, sticky='W')
    tInput = ttk.Entry(step_window)
    tInput.grid(column=1, row=4, padx=2, pady=0, sticky='W')


    #Ip definition and documentation
    IP_def = ttk.Label(step_window, text='IP = Injector Plate').grid(column=0, row=10, padx=5, pady=5, sticky='W')
    
    

    #Append data to preliminary list
    current_steps.append((cw_entry, ch_entry, step_loc, Ni, tInput))

    
    #Another step function 'Add':
    def another_step():
        for index, step_widgets in enumerate(current_steps, start=1):
            validated_values = _validate_step_entries(step_widgets, index)
            if validated_values is None:
                return

        #Create button for the current step
        step_button = ttk.Button(tab3, text=f'Step {step_number + 1}', command = lambda: step_window.deiconify())
        step_button.grid(row=step_number + 5, column=0, padx=5, pady=5, sticky='W')

        buttons.append(step_button)


        #Create step 'i + 1':
        create_step(root, tab3, step_number + 1, segmented_button)



    # 'Add' button
    add_button = ttk.Button(step_window, text='Add', command=another_step)
    add_button.grid(column=0, row=5, padx=5, pady=5, sticky='W')

    def hide_windows():
        for window in step_windows:
            window.withdraw()


    #Finish button
    def finish():
        global step_list, step_windows
        global step_data



        #Disable entries and buttons for the step windows
        for i in range(0, len(current_steps)):
            for entry in current_steps[i]:
                entry.config(state='disabled')
                
        for index, step_widgets in enumerate(current_steps, start=1):
            validated_values = _validate_step_entries(step_widgets, index)
            if validated_values is None:
                return

        #Append the entries to the main list, fed to the main function
        for cw_entry, ch_entry, step_loc, Ni, tInput in current_steps:
            step_data.append((cw_entry.get(), ch_entry.get(), step_loc.get(), Ni.get(), tInput.get()))




        
        finish_button.config(state='disabled')


        #Button at the end of the sections list
        
        last_step_button = ttk.Button(tab3, text=f'Step {step_number + 1}', command=lambda: step_window.deiconify())
        last_step_button.grid(row=step_number + 5, column=0, padx=5, pady=5, sticky='W')


        buttons.append(last_step_button)

        #The buttons list refers to the list inside the "create_step" function, hold the buttons order, and number for
        #showing in the interface and deletion


        #Hide the step windows
        hide_windows()



    #Finish geometry creation button:
    finish_button = ttk.Button(tab3, text='Finish', command=finish)
    finish_button.grid(column=0, row=2, padx=5, pady=2, sticky='W')

    #"Segment list" label
    step_list = ttk.Label(tab3, text='Step list:')
    step_list.grid(column=0, row=4, padx=5, pady=0, sticky='W')


    #Button to reset the window
    reset_button = ttk.Button(tab3, text='Reset', command=placeholder)
    reset_button.grid(column=0, row=3, padx=5, pady=0, sticky='W')

    buttons.append(step_list)
    buttons.append(finish_button)
    buttons.append(reset_button)





    ''' **** RESET FUNCTION **** '''
    def reset():
        global current_steps, step_data, step_list

        #Empty the values lists
        current_steps.clear()
        step_data.clear()

        #Update the state of the finish/smooth channels button and and the windows 
        finish_button.config(state='normal')
        segmented_button.config(state='normal')

        step_window.destroy()

        #Destroy the existing buttons
        for button in buttons:
            button.destroy()

        step_list.destroy()
        buttons.clear()


    # Reconfig the reset button to activate the 'reset' function
    reset_button.config(command = reset)

    return


