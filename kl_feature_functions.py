# Import the needed extensions
import math
import klayout
import pya

def ls_cell(tone,size,pitch,length,angle):
    
    # tone = input("(D)ark or (C)lear feature: ")
    # size = int(input("Size (in nm) of the line: "))
    # pitch = int(input("Pitch (in nm): "))
    # length = int(input("Length of the line (in nm): "))
    tone = "D"
    size = 100
    pitch = 5001
    length = 10000
    angle = 0

    layout = pya.Layout()
    Unit = layout.create_cell(f"LS_Array_{tone}_{size}_{pitch}_{angle}")

    l_outline = layout.layer(11,0) #overlay layer for the cell
    l_line = layout.layer(2,0) #line layer, sacrificial

    #Create the overlay shape
    overlay = Unit.shapes(l_outline).insert(pya.Box((-length/2),-length/2,(length/2),length/2))

    #Check pitch of the LS array
    pitch_check = math.floor(length/pitch)
    iso = pitch_check < 2 #boolean

    #Create the LS array
    if iso:
        line_vert = Unit.shapes(l_line).insert(pya.Box(-size/2,-length/2,size/2,length/2))
    else:
        for num in range(0,math.floor(pitch_check),1):
            if num == 0:
                line_vert = Unit.shapes(l_line).insert(pya.Box((num*pitch)-(size/2),-length,(num*pitch+size)-(size/2),length))
            else:
                line_vert = Unit.shapes(l_line).insert(pya.Box((num*pitch)-(size/2),-length,(num*pitch+size)-(size/2),length))
                line_vert = Unit.shapes(l_line).insert(pya.Box((-num*pitch)-(size/2),-length,(-num*pitch+size)-(size/2),length))

    #Does the angle transformation for the lines for rotations
    t = pya.ICplxTrans(1,angle,0,0,0)
    Unit.shapes(l_line).transform(t)

    #Removes polygons extending beyond the overlay layer by only including those within the overlay region
    r1 = pya.Region(Unit.shapes(l_line))
    r2 = pya.Region(Unit.shapes(l_outline))
    r_and = r1 & r2
    l_diff = layout.layer(1,0)
    r_diff = Unit.shapes(l_diff).insert(r_and)


    #Export GDS
    layout.write(f"LS_test_t{tone}_s{size}_p{pitch}_l{length}_a{angle}.gds")

ls_cell(1,2,3,4,5)