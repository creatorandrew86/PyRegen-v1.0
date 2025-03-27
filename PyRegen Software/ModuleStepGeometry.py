import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from ModuleDataStore import step_data

scriptDir = os.path.dirname(os.path.abspath(__file__))
global step_windows
current_steps, buttons, step_windows = [], [], []

def create_step(root, tab3, step_number):
    #Placeholder for finish/reset functions
    def placeholder():
        pass
    
    global scriptDir, step_list, step_windows



    #Location of the step window along the width of the user's screen
    window_width = 300*(step_number + 1)

    
    #Generate the step window
    step_window = tk.Toplevel(root)
    step_window.title(f' Segment {step_number + 1}')
    step_window.geometry(f'330x350+{window_width}+300')


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


    #Image for reference
    im2_path = os.path.join(scriptDir, 'Interface Images', 'Step Window Image.png')
    image2 = Image.open(im2_path)
    photo2 = ImageTk.PhotoImage(image2)

    im2_label = ttk.Label(step_window, image=photo2)
    im2_label.image = photo2
    im2_label.grid(column=0, columnspan=2, row=6, rowspan=3, padx=5, pady=5, sticky='ne')

    #Ip definition
    IP_def = ttk.Label(step_window, text='IP = Injector Plate').grid(column=0, row=10, padx=5, pady=5, sticky='W')
    

    #Append data to preliminary list
    current_steps.append((cw_entry, ch_entry, step_loc, Ni, tInput))

    
    #Another step function 'Add':
    def another_step():
        #Check if the entries are filled correctly:
        #
        #Real positive numbers, except for the position


        
        try:
            entries = tuple(float(entry.get()) for entry in current_steps[-1])
        except ValueError:
            messagebox.showerror('Error 1', 'Fill all the entries with real numbers')
            return

        if len(entries) != 5 or any(x < 0 for i, x in enumerate(entries) if i != 2):
            messagebox.showerror('Error 1', 'Fill all the entries with valid numbers')
            return

        
    
        #Create button for the current step
        step_button = ttk.Button(tab3, text=f'Step {step_number + 1}', command = lambda: step_window.deiconify())
        step_button.grid(row=step_number + 5, column=0, padx=5, pady=5, sticky='W')

        buttons.append(step_button)


        #Create step 'i + 1':
        create_step(root, tab3, step_number + 1)



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
                
        #Check if the entries are filled correctly:
        #
        #Real positive numbers, except for the position


        
        try:
            entries = tuple(float(entry.get()) for entry in current_steps[-1])
        except ValueError:
            messagebox.showerror('Error 1', 'Fill all the entries with real numbers')
            return

        if len(entries) != 5 or any(x < 0 for i, x in enumerate(entries) if i != 2):
            messagebox.showerror('Error 1', 'Fill all the entries with valid numbers')
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

        step_window.destroy()

        #Destroy the existing buttons
        for button in buttons:
            button.destroy()

        step_list.destroy()
        buttons.clear()


    # Reconfig the reset button to activate the 'reset' function
    reset_button.config(command = reset)

    return


