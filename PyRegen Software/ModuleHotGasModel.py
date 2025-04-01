
#  ModuleHotGasModel.py
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
from rocketcea.cea_obj import CEA_Obj

#Global variables definition and default injPsi = 1
global Pc, Tc
injPsi = 1

def initialize_hg(c: CEA_Obj, Pc, MR, eps, Rt):
    global SMF, Tc

    #Get "Species Mass Fraction" from CEA, noted "SMF"
    SMF = c.get_SpeciesMassFractions(Pc = Pc, MR = MR, eps = eps, min_fraction=0.00001)
    #Define chamber transport properties list
    ch_transport = c.get_Chamber_Transport(Pc=Pc, MR=MR, eps=eps)           # Get chamber transport properties

    viscosity = ch_transport[1] * 10000                                     # Chamber viscosity (milipoise)
    spec_heat = ch_transport[0] * 4184                                      # Chamber Specific heat (BTU/lbm*deg R to J/kg*K)
    Pr = ch_transport[3]                                                    # Chamber Prandtl number
    C_star = c.get_Cstar(Pc=Pc, MR=MR) / 3.28                               # Characteristic velocity (ft/s to m/s)
    Tc = c.get_Tcomb(Pc=Pc, MR=MR) / 1.8                                    # Combustion temperature (deg R to K)                                         

    '''
        Hot side heat transfer coefficient intialization. The following is a constant value, only dependent on known gas properties at
    stagnation point. The relation is further calibrated for injection effects and Mach/temperature effects.
        The baseline model is the simplified Bartz correlation. The 1.18 constant comes from the generated throat geometry, and the 
    pre-calculated ratio of throat diameter and curvature radius, raised to the power of 0.1.
        The constant CBartz can be updated to 0.023 or 0.026 or other values based on experimental results
    '''
    CBartz = 0.023      #Constant used for Bartz Correlation, 0.023 or 0.026
    h_g = (CBartz / math.pow(2 * Rt * 0.01, 2)) * 1.18 * (math.pow(viscosity, 0.2) * spec_heat / math.pow(Pr, 0.6)) * math.pow((Pc / 14.5 ) / C_star, 0.8)

    return h_g

def hot_gas_properties(c: CEA_Obj, argPc, MR, eps, eps_i, x_points, y_points, i, Rt, CR):
    global Pc, injPsi
    #Update the global Pc/Rt/CR variables to the function argument
    Pc = argPc
    from rocketcea.cea_obj import CEA_Obj

    #Define 'x' and stagnetion temperature 'T_0'
    x = x_points[i]
    T_0 = c.get_Tcomb(Pc=Pc, MR=MR) / 1.8

    if min(x_points) < -1.5 * Rt * math.sin(0.785) - Rt * (math.sqrt(CR) - 1):
        from rocketcea.cea_obj import CEA_Obj
        full_output = c.get_full_cea_output(Pc=Pc, MR=MR, eps = 2)
        lines = full_output.split('\n')

        for line in lines:
            if 'MACH NUMBER' in line:
                M_chamber = float(line.split()[3])

    #If the cell is located in the chamber section:
    if x < -1.5 * Rt * math.sin(0.785) - Rt * (math.sqrt(CR) - 1):
        T = T_0                                                                         # Chamber temperatuer
        M = M_chamber                                                                   # Chamber Mach number
        gam = c.get_Chamber_MolWt_gamma(Pc=Pc, MR=MR, eps=eps)[1]                       # Chamber gamma




    #If the cell is located in the convergent section of the nozzle
    elif x < 0 and x > -1.5 * Rt * math.sin(0.785) - Rt * (math.sqrt(CR) - 1):
        from rocketcea.cea_obj import CEA_Obj

        #Run the CEA case
        full_output = c.get_full_cea_output(Pc=Pc, MR=MR, subar=eps_i)

        #After fetching the full output, split it in lines:
        lines = full_output.split('\n')
            
        M = None
        T = None

        #Search through the full output for 'MACH NUMBER' ; 'T, K' and 'GAMMAs':
        for line in lines:
            if 'MACH NUMBER' in line:
                    
                #Fetch the respective value:
                M = float(line.split()[-2])
                    
            if 'T, K' in line:
                    
                T = float(line.split()[-2])

            if 'GAMMAs' in line:

                gam = float(line.split()[-2])




    #If the cell is located in the divergent nozzle section:
    else:
        T = c.get_Temperatures(Pc=Pc, MR=MR, eps=eps_i)[2] / 1.8            # Hot gas temperature
        M = c.get_MachNumber(Pc=Pc, MR=MR, eps=eps_i)                       # Hot gas Mach number
        gam = c.get_IvacCstrTc_exitMwGam(Pc=Pc, MR=MR, eps=eps_i)[4]        # Hot gas gamma


    #Adiabatic wall temperature
    T_aw = T * (1 + 0.87 * math.pow(M, 2) * (gam - 1) / 2)

    gas_properties = [gam, M, T, T_aw]

    return gas_properties


def hotgas_model(hotside_model_args, T_wg):
    global SMF, Pc, Tc, injPsi      #Global variables definiton

    #Local arguments list initialization and unpacking
    args = hotside_model_args
    gas_properties, eps, hg_initial, charLength = args

    #Gas properties list in order: 0-gamma, 1-Mach, 2-Gas temperature 3-Adiabatic wall temperature
    #Retrieve the gas properties from the list
    gam = gas_properties[0]
    M = gas_properties[1]
    T_aw = gas_properties[3]

    #Calculate 'sigma', the Temperature(T_wg) dependent term of hg
    term_0 = 1 + math.pow(M, 2) * (gam - 1) / 2
    sigma = math.pow((0.5 * (T_wg / Tc) * term_0 + 0.5), 0.68) * math.pow(term_0, -0.12)

    #Update hg, and calculate hot side heat flux
    h_g = hg_initial * math.pow(1 / eps, 0.9) * sigma
    Q_flux_g = h_g * (T_aw - T_wg)

    #Radiative heat flux

    #Partial pressures of H2O and CO2, the only significant parts of radiative heat transfer
    partial_pressure_H2O = SMF[1]['H2O'][-1] * Pc / 14.7 if 'H2O' in SMF[1] else 0
    partial_pressure_CO2 = SMF[1]['*CO2'][-1] * Pc / 14.7 if '*CO2' in SMF[1] else 0
    Le = 0.006 * charLength

    #Calculate radiative heat fluxes
    Q_flux_H2O = 4.07 * pow(partial_pressure_H2O, 0.8) * pow(Le, 0.6) * (pow(T_aw/100, 3) - pow(T_wg/100, 3))
    Q_flux_CO2 = 4.07 * pow(partial_pressure_CO2 * Le, 1/3) * (pow(T_aw/100, 3.5) - pow(T_wg/100, 3.5))

    #Update hot side heat flux
    Q_flux_g += Q_flux_H2O + Q_flux_CO2



    return Q_flux_g