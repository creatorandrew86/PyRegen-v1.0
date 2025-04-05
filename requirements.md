# Software Requirements
The main python requirement for PyRegen is version 3.6+, but 3.10+ is recommended

The PyRegen Software imports and uses the following python extensions : NASA CEA, numpy, matplotlib, tkinter, scipy and CoolProp


To install numpy, matplotlib, tkinter, scipy and CoolProp, write the following commands into command prompt (Windows 8 and above)
```python
pip install numpy matplotlib tkinter scipy CoolProp
```

... Or to update:

```python
pip install --upgrade numpy
pip install --upgrade matplotlib
pip install --upgrade tkinter
pip install --upgrade scipy
pip install --upgrade CoolProp
```

For Linux:
```python
sudo pip install numpy matplotlib tkinter scipy
```

## RocketCEA

It is recommended to use a RocketCEA version higher than 1.2.0, for installation purposes!!
After you have installed the previous, mainly numpy matplotlib and scipy, give the following command, and replace 1.2.0 with the wanted version:
```python
pip install rocketcea-1.2.0.tar.gz
```

You can find more information regarding RocketCEA installation, along with a potential gfortran requirement (for older systems), and Linux version here:

[Link Text](https://rocketcea.readthedocs.io/en/latest/quickstart.html)

