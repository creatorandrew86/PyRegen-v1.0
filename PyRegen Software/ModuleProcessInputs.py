
#  ModuleProcessInputs.py
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



# Main function
def process_inputs(entries_list):

    # Boolean to store the existence of an error as True or False
    input_error = False
    #Unpack the entries list || Single or double value lines are entries without units, written like that for readability
    (FuelTemp_entry, OxTemp_entry, chamber_pressure, mixture_ratio, contraction_ratio,
     throat_radius, mass_flux, char_length, eps_entry, coolant_pressure, coolant_temp,
     coolant_mfr, coolant_entry_point, coolant_exit_point, number_it, RtValues_var,
     FuelTemp_unit, OxTemp_unit, chamber_pressure_unit, throat_radius_unit, mass_flux_unit,
     char_length_unit, coolant_pressure_unit, coolant_temp_unit, coolant_mfr_unit,
     coolant_entry_point_unit, coolant_exit_point_unit) = entries_list
    
    # Propellants' temperature conversion plus input verification (the value is optional)

    # ---------------------------------------------------------------------------------------------------------------------------- #
    #Fuel
    if FuelTemp_entry.get().strip():
        if FuelTemp_unit == 'K':
            FuelTemp = float(FuelTemp_entry.get())
        elif FuelTemp_unit == 'C':
            FuelTemp = float(FuelTemp_entry.get()) + 273.16
        elif FuelTemp_unit == 'F':
            FuelTemp = (float(FuelTemp_entry.get()) - 32)/1.8 + 273.16
        elif FuelTemp_unit == 'R':
            FuelTemp = float(FuelTemp_entry.get()) * 5/9
        else:
            print("Choose one of the unit options")

    else:
        FuelTemp = None

    # ---------------------------------------------------------------------------------------------------------------------------- #
    #Oxidizer
    if OxTemp_entry.get().strip():
        if OxTemp_unit == 'K':
            OxTemp = float(OxTemp_entry.get())
        elif OxTemp_unit == 'C':
            OxTemp = float(OxTemp_entry.get()) + 273.16
        elif OxTemp_unit == 'F':
            OxTemp = (float(OxTemp_entry.get()) - 32)/1.8 + 273.16
        elif FuelTemp_unit == 'R':
            OxTemp = float(OxTemp_entry.get()) * 5/9
        else:
            print("Choose one of the unit options")

    else:
        OxTemp = None

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Handle inputs with no unit (MR, CR, eps, number of stations(it_number))
    if mixture_ratio.get().strip():
        MR = float(mixture_ratio.get())
    else:
        print("Fill the Mixture Ratio Entry - Tab 1")
        input_error = True


    if contraction_ratio.get().strip():
        CR = float(contraction_ratio.get())
    else:
        print("Fill the Contraction Ratio Entry - Tab 1")
        input_error = True


    if eps_entry.get().strip():
        eps = float(eps_entry.get())
    else:
        print("Fill the Expansion Ratio Entry - Tab 1")
        input_error = True

    if number_it.get().strip() and float(number_it.get()) <= 500:
        it_number = float(number_it.get())
    else:
        print("Fill the Number of Iterations Entry with a Number less than 500 - Tab 2")
        input_error= True


    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Chamber pressure
    if chamber_pressure.get().strip():
        if chamber_pressure_unit == 'psi':
            Pc = float(chamber_pressure.get())
        elif chamber_pressure_unit == 'bar':
            Pc = float(chamber_pressure.get()) * 14.5038
        elif chamber_pressure_unit == 'atm':
            Pc = float(chamber_pressure.get()) * 14.7
        elif chamber_pressure_unit == 'kPa':
            Pc = float(chamber_pressure.get()) * 0.145038
        else:
            print("Choose one of the unit options")
            input_error = True
    else:
        print("Fill the Chamber Pressure Entry - Tab 1")
        input_error = True



    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Characteristic Length
    if char_length.get().strip():
        if char_length_unit == 'm':
            charLength = float(char_length.get()) * 100 / CR
        elif char_length_unit == 'cm':
            charLength = float(char_length.get()) / CR
        elif char_length_unit == 'in':
            charLength = float(char_length.get()) * 2.54 / CR
        elif char_length_unit == 'ft':
            charLength = float(char_length.get()) * 30.48 / CR 
        else:
            print("Choose one of the unit options")
            input_error = True
    else:
        print("Fill the Characteristic Length Entry - Tab 1")
        input_error = True

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Throat Radius || Input Fetch or Calculate
    if RtValues_var.get() == 1:
        if throat_radius.get().strip():
            if throat_radius_unit == 'm':
                Rt = float(throat_radius.get()) * 100 
            elif throat_radius_unit == 'cm':
                Rt = float(throat_radius.get()) 
            elif throat_radius_unit == 'in':
                Rt = float(throat_radius.get()) * 2.54 
            elif throat_radius_unit == 'ft':
                Rt = float(throat_radius.get()) * 30.48 
            else:
                print("Choose one of the unit options")
                input_error = True
        else:
            print("Fill the Throat Radius Entry - Tab 1")
            input_error = True
        
        eng_mass_flux = None

    # Engine Mass Flux Condition
    else:
        if mass_flux.get().strip():
            if mass_flux_unit == 'kg/s':
                eng_mass_flux = float(mass_flux.get())
            elif mass_flux_unit == 'lb/s':
                eng_mass_flux = float(mass_flux.get()) * 0.453
            elif mass_flux_unit == 'oz/s':
                eng_mass_flux = float(mass_flux.get()) * 0.0283
            else:
                print("Choose one of the unit options")
                input_error = True
        else:
            print("Fill the Mass Flux Entry - Tab 1")
            input_error = True

        Rt = None



    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Coolant Inlet Pressure
    if coolant_pressure.get().strip():
        if coolant_pressure_unit == 'bar':
            coolant_P = float(coolant_pressure.get())
        elif coolant_pressure_unit == 'atm':
            coolant_P = float(coolant_pressure.get()) * 1.01325
        elif coolant_pressure_unit == 'kPa':
            coolant_P = float(coolant_pressure.get()) / 100
        elif coolant_pressure_unit == 'psi':
            coolant_P = float(coolant_pressure.get()) / 14.7
        else:
            print("Choose one of the unit options")
            input_error = True
    else:
        print("Fill the Coolant Pressure Entry - Tab 2")
        input_error = True

    #Update coolant_P
    coolant_P *= 101325

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Coolant Inlet Temperature
    if coolant_temp.get().strip():
        if coolant_temp_unit == 'K':
            coolant_T = float(coolant_temp.get())
        elif coolant_temp_unit == 'C':
            coolant_T = float(coolant_temp.get()) + 273.16
        elif coolant_temp_unit == 'F':
            coolant_T = (float(coolant_temp.get()) - 32) / 1.8 + 273.16
        elif coolant_temp_unit == 'R':
            coolant_T = float(coolant_temp.get()) * 5/9
        else:
            print("Choose one of the unit options")
    else:
        print("Fill the Coolant Inlet Temperature Entry - Tab 2")
        input_error = True

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Coolant Mass Flow Rate
    if coolant_mfr.get().strip():
        if coolant_mfr_unit == 'kg/s':
            mfr = float(coolant_mfr.get())
        elif coolant_mfr_unit == 'lb/s':
            mfr = float(coolant_mfr.get()) * 0.453
        elif coolant_mfr_unit == 'oz/s':
            mfr = float(coolant_mfr.get()) * 0.0283
        else:
            print("Choose one of the unit options")
            input_error = True
    else:
        print("Fill the Coolant Mass Flow Rate Entry - Tab 2")
        input_error = True

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Coolant Entry Point
    if coolant_entry_point.get().strip():
        if coolant_entry_point_unit == 'm':
            x_initial = float(coolant_entry_point.get())  
        elif coolant_entry_point_unit == 'cm':
            x_initial = float(coolant_entry_point.get()) * 0.01 
        elif coolant_entry_point_unit == 'in':
            x_initial = float(coolant_entry_point.get()) * 0.0254  
        elif coolant_entry_point_unit == 'ft':
            x_initial = float(coolant_entry_point.get()) * 0.3048 
        else:
            print("Choose one of the unit options for Coolant Entry Point")
            input_error = True
    else:
        print("Fill the Coolant Entry Point Entry - Tab 2")
        input_error = True

    # ---------------------------------------------------------------------------------------------------------------------------- #
    # Coolant Exit Point
    if coolant_exit_point.get().strip():
        if coolant_exit_point_unit == 'm':
            x_final = float(coolant_exit_point.get())  # 
        elif coolant_exit_point_unit == 'cm':
            x_final = float(coolant_exit_point.get()) * 0.01  
        elif coolant_exit_point_unit == 'in':
            x_final = float(coolant_exit_point.get()) * 0.0254
        elif coolant_exit_point_unit == 'ft':
            x_final = float(coolant_exit_point.get()) * 0.3048 
        else:
            print("Choose one of the unit options for Coolant Exit Point")
            input_error = True
    else:
        print("Fill the Coolant Exit Point Entry - Tab 2")
        input_error = True

    # Error if x_final = x_intial
    if x_final == x_initial:
        print("The coolant entry point cannot be equal to the exit point")
        input_error = True

    output_list = [FuelTemp, OxTemp, Pc, MR, CR, eps, it_number, charLength, Rt, 
                   eng_mass_flux, coolant_P, coolant_T, mfr, x_initial, x_final]
    

    return output_list, input_error
        