import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from ModuleDataStore import segment_data

scriptDir = os.path.dirname(os.path.abspath(__file__))
current_segment, buttons = [], []

def create_seg(root, tab3, seg_number):
    #Placeholder for finish/reset functions
    def placeholder():
        pass
    
    global scriptDir, seg_list

    #Initiate the windows list
    seg_windows = []
    

    #Location of the segment window along the width of the user's screen:
    window_width = 300*(seg_number + 1)
    
    #Generate the first window
    seg_window = tk.Toplevel(root)
    seg_window.title(f' Segment {seg_number + 1}')
    seg_window.geometry(f'350x490+{window_width}+300')


    #Join the window in the segment windows list
    seg_windows.append(seg_window)


    ''' ***************** LABELS FOR ENTRIES **************** '''


    #Channel width at the inlet
    ttk.Label(seg_window, text='Inlet Channel Width (mm):').grid(column=0, row=0, padx=5, pady=5, sticky='W')
    cw_entry_in = ttk.Entry(seg_window)
    cw_entry_in.grid(column=1, row=0, padx=5, pady=5, sticky='W')

    #Channel width at the outlet
    ttk.Label(seg_window, text='Outlet Channel Width (mm):').grid(column=0, row=1, padx=5, pady=5, sticky='W')
    cw_entry_out = ttk.Entry(seg_window)
    cw_entry_out.grid(column=1, row=1, padx=5, pady=5, sticky='W')


    #Channel height at the inlet
    ttk.Label(seg_window, text='Inlet Channel Height (mm):').grid(column=0, row=2, padx=5, pady=5, sticky='W')
    ch_entry_in = ttk.Entry(seg_window)
    ch_entry_in.grid(column=1, row=2, padx=5, pady=5, sticky='W')

    #Channel height at the outlet
    ttk.Label(seg_window, text='Outlet Channel Height(mm):').grid(column=0, row=3, padx=5, pady=5, sticky='W')
    ch_entry_out = ttk.Entry(seg_window)
    ch_entry_out.grid(column=1, row=3, padx=5, pady=5, sticky='W')


    #Channel segment inlet location
    ttk.Label(seg_window, text='Segment inlet (Distance from IP, m):').grid(column=0, row=4, padx=5, pady=5, sticky='W')
    inlet_loc = ttk.Entry(seg_window)
    inlet_loc.grid(column=1, row=4, padx=5, pady=5, sticky='W')

    #Channel segment outlet location
    ttk.Label(seg_window, text='Segment outlet (Distance from IP, m):').grid(column=0, row=5, padx=5, pady=5, sticky='W')
    outlet_loc = ttk.Entry(seg_window)
    outlet_loc.grid(column=1, row=5, padx=5, pady=5, sticky='W')


    
    #Number of cooling channels
    ttk.Label(seg_window, text='Number of Channels').grid(column=0, row=6, padx=2, pady=0, sticky='W')
    Ni = ttk.Entry(seg_window)
    Ni.grid(column=1, row=6, padx=5, pady=5,  sticky='W')

    #Cooling channel thickness
    ttk.Label(seg_window, text='Wall thickness (mm)').grid(column=0, row=7, padx=2, pady=0, sticky='W')
    tInput = ttk.Entry(seg_window)
    tInput.grid(column=1, row=7, padx=2, pady=0, sticky='W')



    #Images for reference
    im3_path = os.path.join(scriptDir, 'Interface Images', 'Segment Window Image.png')
    image3 = Image.open(im3_path)
    photo3 = ImageTk.PhotoImage(image3)

    im2_label = ttk.Label(seg_window, image=photo3)
    im2_label.image = photo3
    im2_label.grid(column=0, columnspan=2, row=9, rowspan=3, padx=5, pady=5, sticky='N')

    #IP definition
    IP_def = ttk.Label(seg_window, text='IP = Injector Plate').grid(column=0, row=13, padx=5, pady=5, sticky='W')


    
    

    #Append data to preliminary list
    current_segment.append((cw_entry_in, cw_entry_out, ch_entry_in, ch_entry_out, inlet_loc, outlet_loc, Ni, tInput))


    #Another step function 'Add':
    def plus_seg():
        #Check if the entries are filled correctly:
        #
        #Real positive numbers, except for the position


        
        try:
            entries = tuple(float(entry.get()) for entry in current_segment[-1])
        except ValueError:
            messagebox.showerror('Error', 'Fill all the entries with real numbers')
            return

        if len(entries) != 8 or any(x < 0 for i, x in enumerate(entries) if i != 4 and i != 5):
            messagebox.showerror('Error', 'Fill all the entries with valid numbers')
            return


        
            
        #Create button for the current step
        seg_button = ttk.Button(tab3, text=f'Segment {seg_number + 1}', command = lambda: seg_window.deiconify())
        seg_button.grid(row=seg_number + 5, column=0, padx=5, pady=5, sticky='W')

        buttons.append(seg_button)


        #Hide step 'i' and create step 'i + 1':
        create_seg(root, tab3, seg_number + 1)


    # 'Add' button
    add_button = ttk.Button(seg_window, text='Add', command=plus_seg)
    add_button.grid(column=0, row=8, padx=5, pady=5, sticky='W')


    #Finish button
    def finish():
        global seg_list
        global segment_data



        #Disable entries and buttons from the segment windows
        for i in range(0, len(current_segment)):
            for entry in current_segment[i]:
                entry.config(state='disabled')

        
        #Check if the entries are filled correctly:
        #
        #Real positive numbers, except for the position


        
        try:
            entries = tuple(float(entry.get()) for entry in current_segment[-1])
        except ValueError:
            messagebox.showerror('Error 1', 'Fill all the entries with real numbers')
            return


        if len(entries) != 8 or any(x < 0 for i, x in enumerate(entries) if i != 4 and i != 5):
            messagebox.showerror('Error 1', 'Fill all the entries with valid numbers')
            return


        if seg_number >= 1:
            if float(current_segment[-2][5].get()) != float(current_segment[-1][4].get()):
                messagebox.showerror('Error', 'The last channel segment outlet must be equal to the current segment inlet')
                return
        


        # Retrieve the values and append to segment_data
        for i in range(0, len(current_segment)):
            segment_values = [entry.get() for entry in current_segment[i]]
            segment_data.append(segment_values)


        
        finish_button.config(state='disabled')


        #Button at the end of the sections list
        last_seg_button = ttk.Button(tab3, text=f'Segment {seg_number + 1}', command=lambda: seg_window.deiconify())
        last_seg_button.grid(row=seg_number + 5, column=0, padx=5, pady=5, sticky='W')


        #Append last segment button to buttons list
        buttons.append(last_seg_button)

        #The buttons list refers to the list inside the "create_seg" function, hold the buttons order, and number for
        #showing in the interface and deletion


        for window in seg_windows:
            window.withdraw()


    #Finish geometry creation button:
    finish_button = ttk.Button(tab3, text='Finish', command=finish)
    finish_button.grid(column=0, row=2, padx=5, pady=2, sticky='W')


    #"Segment list" label
    seg_list = ttk.Label(tab3, text='Segment list:')
    seg_list.grid(column=0, row=4, padx=5, pady=0, sticky='W')


    #Button to reset the window
    reset_button = ttk.Button(tab3, text='Reset', command=placeholder)
    reset_button.grid(column=0, row=3, padx=5, pady=0, sticky='W')


    #Append buttons to buttons list
    buttons.append(finish_button)
    buttons.append(reset_button)



    ''' **** RESET FUNCTION **** '''
    def reset():
        global current_steps, segment_data, seg_list

        #Empty the values lists
        current_segment.clear()
        segment_data.clear()


        #Update the state of the finish/smooth channels button and the windows 
        finish_button.config(state='normal')

        seg_window.destroy()

        #Destroy the existing buttons
        for button in buttons:
            button.destroy()

        seg_list.destroy()

        buttons.clear()


    # Reconfig the reset button to activate the 'reset' function
    reset_button.config(command = reset)


    return