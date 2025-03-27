'''
------------------------------------------------------------------------------------------------------------------------------------------
                                                MODULE PYREGEN - SOLVING ALGORITHM
    Module Inputs:
        -Coolant Initialization || Enthalpy, pressure, mass flow rate
        -Nozzle Geometry || Points list, general data (Rt, CR, L*) and cooling jacket location
        -Cooling Channels Geometry || Segment/Step Data lists and "var" values, booleans that indicate the type of channel picked
(See ModuleSegmentGeometry or ModuleStepGeometry)
        -CEA Inputs || Inputs used in the CEA Case (See ModuleHotGasModel): Pc, MR, eps
        -Entries || Advanced, optional entries to be processed in the models (Hot/Cold)

    Module Output:
        -Main data storage ("data_array"): Contains the values listed below at every station
        (coolant_T, coolant_P(Pa), coolant_P_show(bar), coolant_u, coolant_H, coolant_rho, hg, Q_flux, T_wg, T_wl, ch, cw, Dh, eps_i)
        Note: Values are defined in their respective definition section

    Note || Short explanation of the iterative solver:
            Since for the Newton's Law of Cooling (Q = h(T_fluid - T_wall)) at the extreme conditions (very high temperature -- gas and 
        very large temperature gradient -- coolant) the convective coefficient h is expressed as h = h(T_wall), an iterative approach
        is chosen, such as:
            1 - Guess first T_wl
            2 - Calculate Qflux_l, Qflux_l = hl(T_wl) * (T_wl - T_coolant)
            3 - Calculate T_wg and Qflux_g 
            4 - Check for convergence : Qflux_g - Qflux_l < error

    # Module Name: PyRegen
    # Author: Bogdan Toma

------------------------------------------------------------------------------------------------------------------------------------------

'''






import math, numpy as np, operator, CoolProp.CoolProp as CP
from rocketcea.cea_obj import CEA_Obj
from scipy.interpolate import interp1d, CubicSpline
from scipy.optimize import fsolve

#Import Auxiliary Modules
import ModuleHotGasModel
import ModuleCoolantProperties


def PyRegen_func(PyRegen_args, c: CEA_Obj):
    #Initiate lists
    show_x, show_y = [], []

    #Unpack the args list:
    geometry_list, coolant_init_list, cea_list, channel_geometry_list, output_list = PyRegen_args

    #Unpack every list into variables:
    x_points, y_points, eps_list, Rt, CR, i_initial, i_final, charLength = geometry_list
    coolant_H, coolant_P, coolant, mfr = coolant_init_list
    Pc, MR, eps, wall_material = cea_list
    smooth_channel_var, stepped_channel_var, segment_data, step_data, wall_k_entry = channel_geometry_list
    data_array, mainOutput_args = output_list

    #Set negative/positive step and operator, depending of the direction of the coolant flow
    di, op = (1, operator.gt) if i_final > i_initial else (-1, operator.lt)

    #Initialize constant value (independent of station specific variables) for heat transfer coefficient of hot gas
    hg_initial = ModuleHotGasModel.initialize_hg(c, Pc, MR, eps, Rt)

    '''
        ****************************************************************************************************************
                                                MAIN LOOP OF ALL THE STATIONS
        ****************************************************************************************************************
    
    '''

    for it in range(abs(i_initial - i_final)):
        # Geometry
        i = i_initial + it * di                                                             # Station number
        x_1, y_1 = x_points[i], y_points[i]                                                 # Station entry coordinates (cm)
        x_2, y_2 = x_points[i + di], y_points[i + di]                                       # Station exit coordinates  (cm)

        #Station coordinates (median)
        x = (x_1 + x_2) / 2 
        y = (y_1 + y_2) / 2


        dl = (math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2)))/100               # Cell length (m)
        A_hot = math.pi * (dl*100) * (y_2 + y_1) / 10000                                    # Hot side area (m^2)
        eps_i = eps_list[i]


        #Append position properties to lists:
        show_x.append(x)
        show_y.append(y)

        

        ''' *********************** GET HOT GAS PROPERTIES FROM CEA *********************** '''

        gas_properties = ModuleHotGasModel.hot_gas_properties(c, Pc, MR, eps, eps_i, x_points, y_points, i, Rt, CR)

        #Gas properties list in order: 0-gamma, 1-Mach, 2-Gas temperature 3-Adiabatic wall temperature
        T_aw = gas_properties[3]

            

        ''' ************************* GET COOLING CHANNEL PROPERTIES FROM  ENTRY ************************* '''

        #Stepped Channels
        
        #Search thourgh the cooling jacket inputs (location):
        if stepped_channel_var:
            for j in range(len(step_data)):

                #Get the location of the step
                x_loc = -(math.fabs(x_points[0]) - float(step_data[j][2]) * 100)


                #Search the intervals, and find where the current cell location is, and attribute local variables to the entries:
                if op(x_loc, x):
                    
                    cw = float(step_data[j][0])/1000                        # Channel width (mm to m)
                    ch = float(step_data[j][1])/1000                        # Channel height (mm to m)
                    N = float(step_data[j][3])                              # Number of channels
                    ts = float(step_data[j][4])/1000                        # Wall thickness (mm to m)
                    
                    break


        #Smooth Channels

        #Search thourgh the cooling jacket inputs (location):
        if smooth_channel_var:
            for j in range(len(segment_data)):
                
                #Get the location of the step
                xOut_loc = -(math.fabs(x_points[0]) - float(segment_data[j][5]) * 100)
                xIn_loc = -(math.fabs(x_points[0]) - float(segment_data[j][4]) * 100)



                #Search the intervals, and find where the current cell location is, and attribute local variables to the entries:
                if op(xOut_loc, x):
                    
                    cw_in = float(segment_data[j][0])/1000                              # Channel width at the entry (mm to m)
                    cw_out = float(segment_data[j][1])/1000                             # Channel width at the exit (mm to m)

                    ch_in = float(segment_data[j][2])/1000                              # Channel height at the entry (mm to m)
                    ch_out = float(segment_data[j][3])/1000                             # Channel height at the exit (mm to m)

                    N = float(segment_data[j][6])                                       # Number of channels
                    ts = float(segment_data[j][7])/1000                                 # Wall thickness (mm to m)
                    
                    break



            xInterval = [xIn_loc, xOut_loc]                                             # Location interval for the spline
            cwInterval = [cw_in, cw_out]                                                # Segment channel width interval
            chInterval = [ch_in, ch_out]                                                # Segment channel height interval

            if xIn_loc > xOut_loc:
                xInterval = xInterval[::-1]                                             # Reverse the xInterval
                cwInterval = cwInterval[::-1]                                           # Reverse corresponding channel width
                chInterval = chInterval[::-1]                                           # Reverse corresponding channel height

            # Generate the cw and ch values || Smoothen the channel
            # Note: Comment or Uncomment the 2 lines "cw_spline =..." and "ch_spline =..." in order of your preference of the channel geometry

            #Part 1 -- Cubic Spline
            cw_spline = CubicSpline(xInterval, cwInterval, bc_type='clamped')
            ch_spline = CubicSpline(xInterval, chInterval, bc_type='clamped')

            #Part 2 -- Linear Interpolation
            #cw_spline = interp1d(xInterval, cwInterval, kind='linear', fill_value="extrapolate")
            #ch_spline = interp1d(xInterval, chInterval, kind='linear', fill_value="extrapolate")

            # Get the cw and ch values for the current location 'x'
            cw = cw_spline(x)
            ch = ch_spline(x)
                
            
        


        lw = cw * ((2*math.pi*(Rt*math.sqrt(eps_i) + ts*100))/(cw*N) - 1)        # Landtwidth (m)

        # Cooling channel geometry
        ch_area = cw * ch * N                           # Total cooling channel area (m^2)
        Dh = 2 * cw * ch / (cw + ch)                    # Cooling channel hydraulic diameter (m)

        #Channel geometry list
        channel_geometry = [cw, ch, N, ts, A_hot, dl, lw]



        #Check for surface roughness entry and set the value, or set the default value
        RelativeRoughness = 0.005



        ''' *************************** COOLING FLUID PROPERTIES || COOLPROP *************************** '''



        # Cooling fluid velocity/thermal properties
        try:
            coolant_T = CP.PropsSI('T', 'P', coolant_P, 'H', coolant_H, coolant)            # Get coolant temperature (K)
            coolant_rho = CP.PropsSI('D', 'P', coolant_P, 'H', coolant_H, coolant)          # Get coolant density (kg/m^3)
            coolant_k = CP.PropsSI('L', 'P', coolant_P, 'H', coolant_H, coolant)            # Get coolant thermal conductivity (W/mK)
            coolant_visc = CP.PropsSI('V', 'P', coolant_P, 'H', coolant_H, coolant)         # Get coolant viscosity (kg/ms)
            coolant_Pr = CP.PropsSI('Prandtl', 'P', coolant_P, 'H', coolant_H, coolant)     # Get coolant Prandtl number
            
        except Exception as e:
            print(e)
            return



        #Quasi 1D Flow Calculation || Part 1 || Conservation of Mass
        coolant_u = mfr / (coolant_rho * ch_area)                                   # Coolant velocity (m/s)
        coolant_Re = (coolant_rho * coolant_u * Dh) / coolant_visc                  # Coolant Reynolds number
        coolant_P_show = coolant_P/101325                                           # Coolant pressure in bar

        #Coolant properties list for information transfer to "Coolant Model"
        coolant_properties = [coolant_Re, coolant_Pr, coolant_k, coolant_T, coolant_rho, coolant_P]


        #Darcy-Weisbach Friction factor calculation
        f = 0.0055*(1 + math.pow(2*math.pow(10, 4)*RelativeRoughness + math.pow(10, 6)/coolant_Re, 1/3))
        initialize_hl_args = [x_1, y_1, show_x, show_y, Dh, f, coolant_properties]

 
        #Get initial hl from coolant properties. See "hl" definition in the coolant properties module
        hl_initial = ModuleCoolantProperties.initialize_hl(initialize_hl_args)

        #Cold/hot side models functions' arguments
        coldside_model_args = [channel_geometry, hl_initial, coolant_T, wall_material, wall_k_entry]
        hotside_model_args = [gas_properties, eps_i, hg_initial, charLength]

                           
        T_wl_initial = coolant_T + 10                            # Initial Guess of the cold wall temperature




        ''' ***************************************** ITERATIVE HEAT TRANSFER SOLVER ***************************************** '''




        def heat_flux_convergence(T_wl_guess, coldside_model_args, hotside_model_args):
            global Q_flux_l, Q_flux_g, T_wg_guess

            #Cold side model || Get cold side heat flux and hot wall temperature guess  ---  W/m^2 / K
            Q_flux_l, T_wg_guess = ModuleCoolantProperties.coldside_model(coldside_model_args, T_wl_guess)

            # Hot side model || Get hot side heat flux  ---  W/m^2
            Q_flux_g = ModuleHotGasModel.hotgas_model(hotside_model_args, T_wg_guess)

            # Residual
            return Q_flux_g - Q_flux_l


        #Get the solution for cold side wall temperature
        T_wl = fsolve(
            lambda T_guess: heat_flux_convergence(
                T_guess, coldside_model_args, hotside_model_args
            ),
            T_wl_initial
        )[0]


        
        #Calculate heat flux(W/m^2), heat transfer rate(W) and hot wall temperature(K) from solution | Convert Q_flux to float
        Q_flux = (Q_flux_g + Q_flux_l)/2
        Q_flux = float(Q_flux[0])
        Q_transfer = Q_flux * A_hot
        T_wg = T_wg_guess


        #Hot side convective transfer coefficient (W/m^2*K)
        hg = Q_flux/(T_aw - T_wg)
        hl = Q_flux/(T_wl - coolant_T)

        if it == 13:
            print(hl, hg, T_aw, T_wl, T_wg, Q_flux)


        #Values at the current station "i" and appending to main array
        station_values = np.array([float(val) for val in [coolant_T, coolant_P, coolant_P_show, coolant_u, coolant_H, coolant_rho, hg, Q_flux, T_wg, T_wl, ch, cw, Dh, eps_i, hl]])
        data_array = np.vstack([data_array, station_values])



        ''' ********************** 1-D COOLANT FLOW EVALUATION ********************** '''


        #Get wall properties for coolant | Used for Darcy friction factor calibration
        try:
            wall_rho = CP.PropsSI('D', 'T', T_wl, 'P', coolant_P, coolant)
            wall_visc = CP.PropsSI('V', 'T', T_wl, 'P', coolant_P, coolant)

        except Exception as e:
            print(e)
            return


        wall_Re = wall_rho * coolant_u * Dh / wall_visc                         # Wall Reynolds Number
        cal_factor_f = pow(T_wl / coolant_T, -0.6 + 5.6 * pow(wall_Re, -0.38))   # Calibration factor for 'f'

        #Calibrate Friction Factor
        f *= cal_factor_f




        #Conservation of momentum || Pressure drop calculation
        delta_P1 = f * coolant_rho * dl * pow(coolant_u, 2) / (2 * Dh)
        
        if it > 0:
            coolant_P += (data_array[-1, 5] * pow(data_array[-1, 3], 2)/2 - coolant_rho * pow(coolant_u, 2)/2)
            coolant_P -= delta_P1
            
            #Contraction/Expansion pressure drop
            if Dh != data_array[-1, 12]:
                zeta = Dh/data_array[-1, 12]
                
                if zeta < 1:
                    k = pow((pow(zeta, -2) - 1), 2)

                elif  zeta > 1:
                    k = 0.5 - 0.167*zeta - 1.125*pow(zeta, 2) - 0.208*pow(zeta, 3)

                elif zeta == 0:
                    k = 0

                delta_P2 = 0.5 * k * coolant_rho * pow(coolant_u, 2)

                coolant_P += delta_P2

        else:
            coolant_P -= coolant_rho * pow(coolant_u, 2)/2



        #Conservation of Energy || Fluid enthalpy calculation
        if it > 0:
            coolant_H += (Q_transfer)/mfr + 0.5 * (pow(data_array[-1, 3], 2) - pow(coolant_u, 2))
        
        else:
            coolant_H += (Q_transfer)/mfr


        # Update iteration
        it += 1

    #Append values and Tl/coolant_pShow lists to main output list
    mainOutput_args.append(float(np.max(data_array[:, 8])))
    mainOutput_args.append(float(np.max(data_array[:, 7])))
    mainOutput_args.append(float(np.max(data_array[:, 6])))
    mainOutput_args.append(data_array)                  # Whole data array


    ''' ***************** MAIN FUNCTION RETURN AND DATA PRINTTING ***************** '''


    #Fetch and round values for the short output:
    max_Twg = round(float(np.max(data_array[:, 8])), 2)             # Maximum hot wall temperature (K)
    max_Qflux = round(float(np.max(data_array[:, 7]))/1000, 2)      # Maximum gas side heat flux (W/m^2 to kW/m^2)
    final_P = round((data_array[-1, 2]), 1)                         # Coolant outlet pressure (bar)
    final_T = round(float(data_array[-1, 0]), 1)                    # Coolant outlet temperature (K)

    short_output_args = [max_Twg, max_Qflux, final_P, final_T]


    #Data map, used for plotting results                                                                                    
    data_map = {
        'Tl': data_array[:, 0].tolist(),
        'P': data_array[:, 2].tolist(),
        'Twl': data_array[:, 9].tolist(),
        'Twg': data_array[:, 8].tolist(),
        'hg': data_array[:, 6].tolist(),
        'hl': data_array[:, 14].tolist(),
        'u': data_array[:, 3].tolist(),
        'y': show_y,
        'x': show_x
    }


    #Main function return
    return short_output_args, data_array, data_map, mainOutput_args