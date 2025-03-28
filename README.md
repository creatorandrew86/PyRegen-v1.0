# PyRegen-v1.0
The first, Open-Source version of PyRegen

# How to Run The Software
Put all the files "PyRegen Software" in the same folder (or download it directly) and run the "RUN.py" file, either with "python RUN.py" or directly from the file explorer (open the file with python).

# Confusing Parts
This sections details how you should fill the channel geometry entries, especially the location related ones.

## Stepped Channel
![Stepped Channel Image](https://github.com/creatorandrew86/PyRegen-v1.0/blob/main/Images/Stepped%20Channel%20Image%20(2).png?raw=true)
![Stepped Channel Entries](https://github.com/creatorandrew86/PyRegen-v1.0/blob/main/Images/Stepped%20Channel%20Entries.png?raw=true)

Stepped Channel means the width and height of the channel remain constant!

The third entry -- Step End (Distance from IP = Injector Plate) -- refers to the red distance on the first image.
Note : The "Step End" means the ending location of the step IN THE DIRECTION OF THE COOLANT FLOW (distance from Injector Plate). For example, if the coolant flow would be reversed in the first image, "Step End" would be represented by the dotted line next to the nozzle exit, and the distance for the entry would be taken as such.

## Segmented Channel
![Segmented Channel Image](https://github.com/creatorandrew86/PyRegen-v1.0/blob/main/Images/Segmented%20Channel%20Image.png?raw=true)
![Segmented Channel Entries](https://github.com/creatorandrew86/PyRegen-v1.0/blob/main/Images/Segmented%20Channel%20Entries.png?raw=true)

Segmented Channels means that the width and height of the channel vary from specified values at the inlet and outlet, following a linear or cubic spline pattern!

The 5th and 6th entries -- Segment Inlet/Outlet (Distance from IP = Injector Plate) -- refer to the green and red distances outlined on the first image.
Note : The segment coordinates go from Inlet to Outlet IN THE DIRECTION OF THE COOLANT FLOW (distance from Injector Plate). For example, if the coolant flow would be reversed in the first image, the segment inlet would be the dotted line closer to the injector plate, and the outlet would be the dotted line closer to the nozzle exit, and the distances for the inlet/outlet would be taken as such.
