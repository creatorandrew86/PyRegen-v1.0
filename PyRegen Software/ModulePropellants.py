import re

#Define global variables
global SubmitOx_var, card_input
SubmitOx_var, SubmitFuel_var = False, False

def parse_chemical_formula(formula):
        # Define a regular expression pattern to find elements and their subscripts
            pattern = r'([A-Z][a-z]*)(\d*)'
            matches = re.findall(pattern, formula)
        
        # Initialize an empty list to hold the parsed output
            parsed_formula = []
        
            for element, subscript in matches:
                
            # If there's no subscript, assume it is 1
                if not subscript:
                    subscript = '1'
                    
            # Append element and subscript to the list
                parsed_formula.append(element)
                parsed_formula.append(subscript)
        
        # Join the list into a string with spaces separating the elements and subscripts
            return ' '.join(parsed_formula)

def CustomOxidizer(root):
    import tkinter as tk
    from tkinter import ttk

    #Global variables
    global SubmitOx_var, card_input
    SubmitOx_var = False

    #Initialize the window
    window = tk.Toplevel(root)
    window.geometry('450x270')
    window.title('Oxidizer Input')

    #Submit function
    def SubmitOx(user_input):
        #Global variables and storing boolean
        global SubmitOx_var, card_input
        SubmitOx_var = True

        #Create the CEA Card text and CEA Card
        card_input = user_input.get('1.0', tk.END).strip()

        #Destrop the window
        window.destroy()

    #Example oxidizer
    def ExampleFunc(root):
        window = tk.Toplevel(root)
        window.title('Oxidizer Example')
        window.geometry('500x160')

        #Initiate the "example" text window
        example = tk.Text(window, width=60, height=6, wrap='word')
        example.pack(pady=8)

        #Generate and insert the example text
        example_text = """
        oxid N2O4(L)   N 2 O 4   wt%=96.5
        h,cal=-4676.0     t(k)=298.15
        oxid SiO2  Si 1.0 O 2.0    wt%=3.5
        h,cal=-216000.0     t(k)=298.15  rho=1.48
        """

        example.tag_configure('left', justify='left')
        example.insert(tk.END, example_text, 'left')

        #Disable "example"
        example.config(state='disabled')

        #Warning
        ttk.Label(window, text='The values (h, cal; t(k); rho) that are not known can be left empty. \
The CEA default values \n will be chosen').pack(pady=5)


    #Set up the text box
    user_input = tk.Text(window, width=50, height=12)
    user_input.pack(pady=8)

    #Button frame
    button_frame = tk.Frame(window)
    button_frame.pack(pady=8)

    #Submit button
    submit_button = ttk.Button(button_frame, text='Submit', command = lambda: SubmitOx(user_input))
    submit_button.pack(side='left', pady=5)

    #Example button
    example_button = ttk.Button(button_frame, text='See Example', command = lambda: ExampleFunc(root))
    example_button.pack(side='left', pady=5)




def CustomFuel(root):
    import tkinter as tk
    from tkinter import ttk

    #Global variables
    global SubmitFuel_var, card_input
    SubmitFuel_var = False

    #Initialize the window
    window = tk.Toplevel(root)
    window.geometry('450x270')
    window.title('Fuel Input')


    #Submit function
    def SubmitFuel(user_input):
        #Global variables and storing boolean
        global SubmitFuel_var, card_input
        SubmitFuel_var = True

        #Create the CEA Card text and CEA Card
        card_input = user_input.get('1.0', tk.END).strip()

        #Destrop the window
        window.destroy()


    #Example fill function
    def ExampleFunc(root):
        window = tk.Toplevel(root)
        window.title('Fuel Example')
        window.geometry('500x160')

        #Initiate the "example" text window
        example = tk.Text(window, width=60, height=6, wrap='word')
        example.pack(pady=8)

        #Generate and insert the example text
        example_text = """
        fuel CH6N2(L)  C 1.0   H 6.0   N 2.0     wt%=60.00
        h,cal=12900.0     t(k)=298.15   rho=.874
        fuel   AL AL 1.0   wt%=40.00
        h,cal=0.0     t(k)=298.15   rho=0.1
        """

        example.tag_configure('left', justify='left')
        example.insert(tk.END, example_text, 'left')

        #Disable "example"
        example.config(state='disabled')

        #Warning
        ttk.Label(window, text='The values (h, cal; t(k); rho) that are not known can be left empty. \
The CEA default values \n will be chosen').pack(pady=5)
        

    #Set up the text box
    user_input = tk.Text(window, width=50, height=12)
    user_input.pack(pady=8)

    #Button frame
    button_frame = tk.Frame(window)
    button_frame.pack(pady=8)

    #Submit button
    submit_button = ttk.Button(button_frame, text='Submit', command = lambda: SubmitFuel(user_input))
    submit_button.pack(side='left', padx=5)

    #Example button
    example_button = ttk.Button(button_frame, text='See Example', command = lambda: ExampleFunc(root))
    example_button.pack(side='left', padx=5)


    

def propellant(Ox, Fuel, OxTemp, FuelTemp):
    #Import CEA
    from rocketcea.cea_obj import add_new_oxidizer, add_new_fuel

    #Global variables
    global SubmitOx_var, card_input

    #Parsed Propellants formula
    parsedOx = parse_chemical_formula(Ox)
    parsedFuel = parse_chemical_formula(Fuel)

    #Oxidizer temperature poll
    if OxTemp:
        #OxTemp = float(OxTemp_entry.get())
        OxCard = f'''
        oxid {Ox}    {parsedOx}   wt% = 100
        t(k) = {OxTemp}
        '''
        
        #This is the blueprint for the card input for CEA
        add_new_oxidizer('Ox', OxCard)
        Oxidizer = 'Ox'

    elif SubmitOx_var:
        card = f'''{card_input}'''
        add_new_oxidizer('Ox', card)
        Oxidizer = 'Ox'
         
    else:
        Oxidizer = Ox

    #Fuel temp poll
    if FuelTemp:
        from rocketcea.cea_obj import add_new_fuel
        #FuelTemp = float(FuelTemp_entry.get())
        FuelCard = f'''
        fuel {Fuel}    {parsedFuel}    wt% = 100
        t(k) = {FuelTemp}
        '''
        
        #This is the blueprint for the card input for CEA
        add_new_fuel('Fuel',  FuelCard)
        CEA_Fuel = 'Fuel'

    elif SubmitFuel_var:
        card = f'''{card_input}'''
        add_new_fuel('Fuel', card)
        CEA_Fuel = 'Fuel'

    else:
        CEA_Fuel = Fuel

    return CEA_Fuel, Oxidizer
        



    

