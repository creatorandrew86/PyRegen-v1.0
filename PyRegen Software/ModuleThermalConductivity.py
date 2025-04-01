
#  ModuleThermalConducitvity.py
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
import numpy as np

x_copper = [
    218.69639794168094, 289.8799313893653, 363.6363636363636, 
    426.2435677530017, 496.56946826758144, 577.1869639794168, 
    638.9365351629502, 704.1166380789022, 769.2967409948542, 
    816.4665523156089
]

y_copper = [
    397.48886910062333, 391.93232413178987, 387.2306322350846, 
    383.6687444345503, 379.5369545859305, 375.9750667853963, 
    373.12555654496884, 371.4158504007124, 369.2787177203918, 
    367.8539626001781
]

# GRCop42

x_GRCop42 = [
    298.45626072041165, 330.188679245283, 358.49056603773585, 
    393.6535162950257, 436.53516295025725, 538.5934819897084, 
    596.9125214408233, 647.5128644939965, 692.1097770154373, 
    726.4150943396226, 777.0154373927959, 818.1818181818181, 
    849.0566037735848, 891.0806174957117, 936.5351629502572, 
    971.6981132075472, 998.2847341337907, 1030.017152658662, 
    1066.895368782161
]

y_GRCop42 = [
    347.76491540516474, 348.9047195013357, 349.61709706144256, 
    350.6144256455922, 351.0418521816563, 351.32680320569904, 
    350.7569011576135, 348.9047195013357, 347.33748886910064, 
    345.9127337488869, 343.34817453250224, 340.9260908281389, 
    339.0739091718611, 336.5093499554764, 332.80498664292077, 
    329.3855743544078, 326.82101513802314, 323.68655387355295, 
    320.1246660730187
]


# GRCop84

x_GRCop84 = [
    203.2590051457976, 229.84562607204114, 260.72041166380785, 
    297.598627787307, 340.4802744425386, 381.6466552315609, 
    435.67753001715266, 464.8370497427101, 542.0240137221269, 
    575.4716981132075, 663.8078902229845, 727.2727272727273, 
    779.5883361921098, 819.0394511149228, 867.9245283018868, 
    906.5180102915951, 938.2504288164665, 976.8439108061749, 
    1071.1835334476843, 1110.6346483704974, 1144.9399656946825, 
    1174.9571183533446, 1197.2555746140652
]

y_GRCop84 = [
    274.8174532502226, 276.09973285841494, 279.66162065894923, 
    284.22083704363314, 289.06500445235974, 293.62422083704365, 
    298.1834372217275, 300.7479964381122, 304.3098842386465, 
    305.44968833481744, 306.01959038290295, 304.59483526268923, 
    303.45503116651827, 301.88780053428314, 299.46571682991987, 
    296.61620658949244, 294.90650044523596, 292.0569902048085, 
    284.5057880676759, 281.3713268032057, 277.66696349065006, 
    274.959928762244, 272.9652715939448
]


def get_k(x_input, mat):
    if mat == 'Copper':
        x_val, y_val = x_copper, y_copper
    elif mat == 'GRCop 42':
        x_val, y_val = x_GRCop42, y_GRCop42
    elif mat == 'GRCop 84':
        x_val, y_val = x_GRCop84, y_GRCop84
        
    else:
        raise ValueError('Invalid Material')


    if x_input < x_val[-1]:
        x_input = x_val[-1]

    y_out = np.interp(x_input, x_val, y_val)
    return y_out
