# Import the needed extensions
import math
import klayout
import pya

tone = input("(D)ark or (C)lear feature: ")
size = int(input("Size (in nm) of the line: "))
pitch = int(input("Pitch (in nm): "))
length = int(input("Length of the line (in nm): "))

layout = pya.Layout()
Unit = layout.create_cell(f"LS_Array_{tone}_{size}_{pitch}")

l_outline = layout.layer(11,0) #overlay layer for the cell
l_line = layout.layer(1,0) #line layer

#Create the overlay shape
overlay = Unit.shapes(l_outline).insert(pya.Box((-length/2),0,(length/2),length))

#Check pitch of the LS array
pitch_check = math.floor(length/pitch)
if pitch_check < 2:
    iso = True
else:
    iso = False

#Create the LS array
if iso:
    line_vert = Unit.shapes(l_line).insert(pya.Box((length-size)/2,0,(length+size)/2,length))
else:
    for num in range(0,math.floor(pitch_check/2),1):
        if num == 0:
            line_vert = Unit.shapes(l_line).insert(pya.Box((num*pitch)-(size/2),0,(num*pitch+size)-(size/2),length))
        else:
            line_vert = Unit.shapes(l_line).insert(pya.Box((num*pitch)-(size/2),0,(num*pitch+size)-(size/2),length))
            line_vert = Unit.shapes(l_line).insert(pya.Box((-num*pitch)-(size/2),0,(-num*pitch+size)-(size/2),length))

#Export GDS
layout.write(f"LS_test_t{tone}_s{size}_p{pitch}_l{length}.gds")
