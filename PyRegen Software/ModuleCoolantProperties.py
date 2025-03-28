
#  ModuleCoolantProperties.py
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


'''
------------------------------------------------------------------------------------------------------------------------------------------
                                        MODULE COOLANT PROPERTIES - FLUID / WALL ANALYSIS

        This module applies the corrected Sieder-Tate correlation to the fluid at every station, and calculates the cold side
    heat flux thorugh the wall (using a 1D heat equation with the cooling fin theory).

        The module input represents known properties of the channel/fluid, dependent on only geometry

        Module output (from function 2): cold side convective heat flux and the hot side temperature

------------------------------------------------------------------------------------------------------------------------------------------

'''




# -- Imports -- 
import math
import CoolProp.CoolProp as CP

#Import Auxiliary Modules
import ModuleThermalConductivity

#Initialization of hl (Liquid <<coolant>> heat transfer coefficient)
def initialize_hl(initialize_hl_args):
    global C2_Int  #Global variable definition

    #Local arguments list initiation and unpacking
    args = initialize_hl_args
    x_1, y_1, show_x, show_y, Dh, f, coolant_properties = args

    #Coolant properties list for information transfer to "Coolant Model" || Order: 0-Re, 1-Pr, 2-Thermal conductivity "k"
    coolant_Re = coolant_properties[0]
    coolant_Pr = coolant_properties[1]
    coolant_k = coolant_properties[2]


    '''
        Cold side heat transfer coefficient initiation. The following is constant value, only dependent on coolant properties
    and not wall temperature(T_wl). The correlation is further corrected for channel roughness and coolant entry.
        The factors dependent on T_wl are updated in the coldside_model function.
        The baseline model is the Sieder-Tate correlation for Nusselt Number, which is the most accurate when there are high temperature
    differences between the bulk of the fluid and the convection walls
    '''
    h_l = 0.027 * math.pow(coolant_Re, 0.8) * math.pow(coolant_Pr, 0.333) * coolant_k / Dh


    #Channel Roughness Correction factor
    f_s = 0.0032 + 0.221*math.pow(coolant_Re, -0.237)                   # Smooth tube friction factor                        
    zeta = f/f_s                                                        # Ratio between un-calibrated friction factor(Ff) and smooth tube Ff
    term0 = 1.5*math.pow(coolant_Pr, -1/6)*math.pow(coolant_Re, -1/8)   # Intermediary term


    #Calibration factor 1, accounting for the channel roughness:
    C1 = zeta*(1 + term0*(coolant_Pr - 1))/(1 + term0*(zeta*coolant_Pr - 1))

    #Coolant entry correction factor
    #Distance travelled by the coolant since entering the channel
    s = math.sqrt(math.pow(math.fabs(math.fabs(x_1 - math.fabs(show_x[0]))), 2) + math.pow(math.fabs(math.fabs(y_1 - math.fabs(show_y[0]))), 2))
    
    #"C2_Int" is an intermediary term, that is then updated based on cold wall temperature in the coldside_model function
    C2_Int = math.pow(s/Dh, -0.7)   

    #Update hl
    h_l *= C1
    
    #Return coolant heat transfer coefficient
    return h_l

def coldside_model(coldside_model_args, T_wl_guess):
    global C2_Int       #Global variable definiton

    #Initialize local arguments list and unpack
    args = coldside_model_args
    channel_geometry, hl_initial, coolant_T, wall_material, wall_k_entry = args

    #Unpack the channel_geometry list || 0-cw, 1-ch, 2-N, 3-Wall thickness(ts), 4-Hot side area(A_hot), 5-Station cell length(dl), 6-Landwidth(lw)
    cw = channel_geometry[0]
    ch = channel_geometry[1]
    N = channel_geometry[2]
    ts = channel_geometry[3]
    A_hot = channel_geometry[4]
    dl = channel_geometry[5]
    lw = channel_geometry[6]
    

    #Update entry calibration factor based on T_wl
    C2 = 1 + C2_Int * math.pow(float(T_wl_guess) / coolant_T, 0.1)
    h_l = hl_initial * math.pow(coolant_T / float(T_wl_guess), 0.14) * C2

    #Wall thermal conductiviti based on current cold wall temperature
    wall_k = float(wall_k_entry.get()) if wall_material == 'Custom' else ModuleThermalConductivity.get_k(T_wl_guess, wall_material)

    # Cooling fin theory
    m = math.sqrt(2 * h_l / (wall_k * lw))
    Lc = ch + lw / 2
    fin_eff = math.tanh(m * Lc) / (m * Lc)

    # Update heat transfer coefficient
    h_l *= (2 * fin_eff * ch + cw) * dl / (A_hot / N)

    # Cold side heat flux
    Q_flux_l = h_l * (T_wl_guess - coolant_T)

    #Guess hot wall temperature
    T_wall = Q_flux_l * (ts / wall_k)
    T_wg_guess = T_wl_guess + T_wall  # Hot wall temperature

    return Q_flux_l, T_wg_guess




