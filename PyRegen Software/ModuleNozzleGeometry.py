
#  ModuleNozzleGeometry.py
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

def NozzleGeometry(Rt, CR, eps, L_char, it_number, a, nu_exit, alpha, NozzleLength):

    #Turn angle at the throat
    theta_max = math.radians(nu_exit/2) if a == 0 else alpha

    #Exit theta preset to 0 and list initialization
    theta_e = 0
    x_points, y_points, eps_list = [], [], []

    #Point "0", throat location
    x0 = 0.382 * Rt * math.sin(theta_max)
    y0 = Rt * (1.382 - 0.382 * math.cos(theta_max))

    # Point '2'/Nozzle exit coordinates
    y2 = Rt * math.sqrt(eps)
    x2 = Rt * (math.sqrt(eps) - 1) * NozzleLength / math.tan(math.radians(15))

    #Slopes of the ines originating at the throat/exit
    m1 = math.tan(theta_max)
    m2 = math.tan(theta_e)

    # y-Intercept points:
    C_1 = y0 - m1 * x0
    C_2 = y2 - m2 * x2

    # Point '1'/Intersection of the 2 lines coordinates
    x1 = (C_2 - C_1) / (m1 - m2)
    y1 = (m1 * C_2 - m2 * C_1) / (m1 - m2)

    #Number of iterations for every section

    it_1 = int(round(0.35*it_number, 0))                        # Chamber section
    it_2 = int(round(0.06*it_number, 0))                        # Convergent nozzle section
    it_3 = int(round(0.1*it_number, 0))                         # Throat curvature 1
    it_4 = int(round(0.05*it_number, 0))                        # Throat curvature 2
    it_5 = int(it_number - (it_1 + it_2 + it_3 + it_4))         # Divergent nozzle section

    #Bezier curve algorithm step
    t = 1/(it_5 - 1)
    

    d_theta_1 = math.radians(45 / (it_3  - 1))
    theta_end = math.radians(45)
    d_theta_2 = theta_max / (it_4 - 1)

    xi = -1.5 * Rt * math.sin(math.radians(45))
    yi = Rt * (2.5 - 1.5 * math.sin(math.radians(45)))
    yf = Rt * math.sqrt(CR)
    xf = -(yf - yi - xi)
    d_x = (math.fabs(xf) - math.fabs(xi)) / (it_2 - 1)

    #Conical Nozzle Geometry
    yf_conical = y2
    xf_conical = (Rt*(math.sqrt(eps) - 1))/math.tan(alpha)
    dx_conical = xf_conical/(it_5 - 1)

    # Creating the points list from the geometry
    for i in range(it_1 - 1):
        y = Rt * math.sqrt(CR)
        x = xf - L_char + i * L_char / (it_1 - 1)
        eps_e = math.pow(y/Rt, 2)
        x_points.append(x)
        y_points.append(y)
        eps_list.append(eps_e)

    for i in range(it_2 - 1):
        x = xf + d_x * i
        y = xi - x + yi
        eps_e = math.pow(y/Rt, 2)
        x_points.append(x)
        y_points.append(y)
        eps_list.append(eps_e)

    for i in range(it_3):
        theta = theta_end - d_theta_1 * i
        x = -1.5 * Rt * math.sin(theta)
        y = Rt * (2.5 - 1.5 * math.cos(theta))
        eps_e = math.pow(y/Rt, 2)
        x_points.append(x)
        y_points.append(y)
        eps_list.append(eps_e)

    for i in range(it_4):
        theta = d_theta_2 * (i + 1)
        x = 0.382 * Rt * math.sin(theta)
        y = Rt * (1.382 - 0.382 * math.cos(theta))
        eps_e = math.pow(y/Rt, 2)
        x_points.append(x)
        y_points.append(y)
        eps_list.append(eps_e)

    if a == 0:
        for i in range(2, it_5):
            x = x0 * (math.pow(1 - t, 2)) + x1 * 2 * t * (1 - t) + x2 * (math.pow(t, 2))
            y = y0 * (math.pow(1 - t, 2)) + y1 * 2 * t * (1 - t) + y2 * (math.pow(t, 2))
            eps_e = math.pow(y/Rt, 2)
            x_points.append(x)
            y_points.append(y)
            eps_list.append(eps_e)
            t += 1 / (it_5 - 1)

    if a == 1:
        for i in range(2, it_5):
            x = x0 + dx_conical*i
            y = x*math.tan(alpha) + y0
            eps_e = math.pow(y/Rt, 2)
            x_points.append(x)
            y_points.append(y)
            eps_list.append(eps_e)

    return x_points, y_points, eps_list
