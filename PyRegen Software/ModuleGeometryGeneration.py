import math, numpy as np
import ModulePropellants
import ModuleNozzleGeometry
from rocketcea.cea_obj import CEA_Obj


def geometry_generator(geometry_generator_args):
    args = geometry_generator_args
    
    #Unpack arguments list || Order: General - CEA Inputs - Tkinter inputs
    #List order: CR, Pc, MR, L*, eps, Ox, Fuel, it_num, x_init, x_final, OxTemp, Fuel_Temp, entries_list, nozzleType, points_filepath
    CR, Pc, MR, charLength, eps, it_number, x_initial, x_final = args[0], args[1], args[2], args[3], args[4], args[7] \
                                                                    ,args[8], args[9]
    
    Ox, Fuel, OxTemp, FuelTemp, Rt, eng_mass_flux = args[5], args[6], args[10], args[11], args[12], args[13]

    geometry_entries_list, nozzleType, points_filepath = args[14], args[15], args[16]

    #Unpack entries list
    NozzleLength_entry, alpha_entry, RtValues_var, mfrValues_var = geometry_entries_list


    #CEA Setup || Ox and Fuel definition
    CEA_Fuel, CEA_Ox = ModulePropellants.propellant(Ox, Fuel, OxTemp, FuelTemp)

    #Setup the CEA case || Noted as "c"
    c = CEA_Obj(oxName=CEA_Ox, fuelName=CEA_Fuel, fac_CR=CR)

    gam = c.get_exit_MolWt_gamma(Pc=Pc, MR=MR, eps=eps)[1]              # Specific heats ratio of the exit gas (Gamma)
    mach_exit = c.get_MachNumber(Pc=Pc, MR=MR, eps=eps)                 # Mach number at the nozzle exit
    rho_th = c.get_Densities(Pc=Pc, MR=MR, eps=eps)[1] * 16.01          # Throat gas density (lb/ft^3 to kg/m^3)
    a_th = c.get_SonicVelocities(Pc=Pc, MR=MR, eps=eps)[1] / 3.28       # Throat gas sound velocity (ft/s to m/s)

    #Calculate Rt using mass flow and CEA values: density(rho) and speed of sound(a) at the throat(index th)
    if mfrValues_var.get() == 1:
        Rt = math.sqrt(0.318 * eng_mass_flux / (rho_th*a_th)) * 100

    #Handle no input case
    elif RtValues_var.get() == 0 and mfrValues_var.get() == 0:
        print("Choose mass flow rate or throat radius input - Tab 1")


    #Calculate engine mass flow rate (kg/s) and exit gas velocity (ft/s to m/s)
    A_throat = math.pi * math.pow(Rt, 2) / 10000                        # Throat area (m^2)
    m_dot = round(rho_th * a_th * A_throat, 2)                          # Mass flow rate (kg/s)
    v_exit = c.get_MachNumber(Pc=Pc, MR=MR, eps=eps)*c.get_SonicVelocities(Pc=Pc, MR=MR, eps=eps)[2] / 3.28 

    #Exit Prandtl-Meyer Angle
    nu_exit = math.degrees(math.sqrt((gam + 1) / (gam - 1)) * math.atan(math.sqrt((gam - 1) / (gam + 1) * (mach_exit ** 2 - 1))) - math.atan(math.sqrt(mach_exit ** 2 - 1)))


    '''

    ********************************************************************************************************************************
                                                                NOZZLE GEOMETRY

        The nozzle is split into a number of iteration points (stations at which the thermal analysis will take place later), and calculates
        the coordinates of the point, or gets them from the input file

        Iteration points will be calles "stations".

    ********************************************************************************************************************************
    
    '''

    #Check if the nozzle length or nozzle angle(Bell/Conical) have been given, and attribute the values(given or default)    
    NozzleLength = float(NozzleLength_entry.get())/100 if NozzleLength_entry.get() else 0.8
    alpha = math.radians(float(alpha_entry.get()) if alpha_entry.get() else 15)


    #Call the 'NozzleGeometry' function
    if nozzleType == 0 or nozzleType == 1:

        #Get lists for (x, y, eps) at each iteration point
        x_points, y_points, eps_list = ModuleNozzleGeometry.NozzleGeometry(Rt, CR, eps, charLength, it_number, nozzleType, nu_exit, alpha, NozzleLength)
    

    if nozzleType == 2:

        # Open the file using the filepath
        with open(points_filepath, "r") as file:
            for line in file:

                # Split each line into values (assuming they are space-separated)
                values = line.split()
                
                # Append the values to their respective lists
                x_points.append(float(values[0]))  
                y_points.append(float(values[1]))  
                eps_list.append(float(values[2])) 

    #Combine the geometry lists into another list
    geometry_list = [x_points, y_points, eps_list, Rt]


    #Get the coolant entry/exit points in "x" coordinates
    x_i = -(math.fabs(x_points[0]) - x_initial * 100)
    x_f = -(math.fabs(x_points[0]) - x_final * 100)



    #Search the inlet and outlet iteration points(stations)
    x_points_array = np.array(x_points)
    i_initial = np.where((x_points_array >= x_i) & (np.roll(x_points_array, 1) <= x_i))[0][0]
    i_final = np.where((np.roll(x_points_array, -1) >= x_f) & (x_points_array <= x_f))[0][0]



    return c, geometry_list, i_initial, i_final, CEA_Ox, CEA_Fuel, m_dot, v_exit
