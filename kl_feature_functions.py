# Import the needed extensions
import math
import klayout
import pya

def ls_cell(tone="D",size=100,pitch=200,dimension=10000,angle=45,x2y=1):

    layout = pya.Layout()
    Unit = layout.create_cell(f"LS_Array_{tone}_{size}_{pitch}_{angle}")

    l_outline = layout.layer(11,0) #overlay layer for the cell
    l_line = layout.layer(2,0) #line layer, sacrificial

    #Create the overlay shape
    overlay = Unit.shapes(l_outline).insert(pya.Box((-dimension/2),-dimension/2,(dimension/2),dimension/2))

    #Check pitch of the LS array
    pitch_check = math.floor(dimension/pitch)
    iso = pitch_check < 2 #boolean

    #Define line dimensions
    l_left = -size/2
    l_bottom = -dimension/2
    l_right = size/2
    l_top = dimension/2
    l_2bottom = -dimension
    l_2top = dimension

    #Create the LS array
    if iso:
        line_vert = Unit.shapes(l_line).insert(pya.Box(l_left, l_bottom, l_right, l_top))
    else:
        for num in range(-pitch_check,pitch_check,1):
                coord_x = num*pitch
                line_vert = Unit.shapes(l_line).insert(pya.Box(coord_x+l_left,l_2bottom,coord_x+l_right,l_2top))


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
    layout.write(f"LS_test_t{tone}_s{size}_p{pitch}_l{dimension}_a{angle}.gds")


def contact_cell(tone="D",size=100,pitch=200,dimension=10000,angle=0,x2y=3):

    layout = pya.Layout()
    Unit = layout.create_cell(f"HD_Array_{tone}_{size}_{pitch}_{angle}_{x2y}to1")

    l_outline = layout.layer(11,0) #overlay layer for the cell
    l_cont = layout.layer(2,0) #contact layer, sacrificial

    #Create the overlay shape
    overlay = Unit.shapes(l_outline).insert(pya.Box((-dimension/2),-dimension/2,(dimension/2),dimension/2))

    #Define the true pitch, after taking x2y into account
    true_pitch_x = (pitch-size) + (size*x2y)
    true_pitch_y = (pitch)

    #Check pitch of the cont array
    pitch_check = math.floor(dimension/true_pitch_y)
    iso = pitch_check < 2 #boolean

    #Set contact dimensions
    c_left = -size*x2y/2
    c_bottom = -size/2
    c_right = size*x2y/2
    c_top = size/2

    #Create the cont array
    if iso:
        cont = Unit.shapes(l_cont).insert(pya.Box(c_left,c_bottom,c_right,c_top))
    else:
        for i in range(-pitch_check,pitch_check,1):
            for j in range(-pitch_check,pitch_check,1):
                coord_x = i*true_pitch_x
                coord_y = j*true_pitch_y
                cont = Unit.shapes(l_cont).insert(pya.Box(coord_x+c_left,coord_y+c_bottom,coord_x+c_right,coord_y+c_top))


    #Does the angle transformation for the holes/dots for rotations
    t = pya.ICplxTrans(1,angle,0,0,0)
    Unit.shapes(l_cont).transform(t)

    #Removes polygons extending beyond the overlay layer by only including those within the overlay region
    r1 = pya.Region(Unit.shapes(l_cont))
    r2 = pya.Region(Unit.shapes(l_outline))
    r_and = r1 & r2
    l_diff = layout.layer(1,0)
    r_diff = Unit.shapes(l_diff).insert(r_and)



    #Export GDS
    layout.write(f"Contact_test_t{tone}_s{size}_p{pitch}_l{dimension}_a{angle}_{x2y}to1.gds")


def lsraf_cell(tone="D",size=300,pitch=100,dimension=5000,angle=0,sraf=60,sraf_num=2):

    layout = pya.Layout()
    Unit = layout.create_cell(f"LSRAF_Array_{tone}_{size}_{pitch}_{angle}_{sraf}_{sraf_num}")

    lsraf_outline = layout.layer(11,0) #overlay layer for the cell
    lsraf_line = layout.layer(2,0) #line layer, sacrificial

    #Create the overlay shape
    overlay = Unit.shapes(lsraf_outline).insert(pya.Box((-dimension/2),-dimension/2,(dimension/2),dimension/2))

    #Define vertical line dimensions
    l_left = -size/2
    l_bottom = -(dimension-(sraf_num+1)*(pitch+sraf))/2
    l_right = size/2
    l_top = (dimension-(sraf_num+1)*(pitch+sraf))/2
    sraf_side_left = -sraf/2
    sraf_side_bottom = l_bottom
    sraf_side_right = sraf/2
    sraf_side_top = l_top
    sraf_end_left = l_left
    sraf_end_bottom = -sraf/2
    sraf_end_right = l_right
    sraf_end_top = sraf/2

    #Create the structure
    line_vert = Unit.shapes(lsraf_line).insert(pya.Box(l_left, l_bottom, l_right, l_top))
    for num in range(-sraf_num,sraf_num+1,1):
        coord = num*pitch
        if coord < 0:
            line_vert = Unit.shapes(lsraf_line).insert(pya.Box(l_left+(coord+sraf_side_left),sraf_side_bottom,l_left+(coord+sraf_side_right),sraf_side_top))
            line_vert = Unit.shapes(lsraf_line).insert(pya.Box(sraf_end_left,l_bottom+(coord+sraf_end_bottom),sraf_end_right,l_bottom+(coord+sraf_end_top)))
        elif coord > 0:
            line_vert = Unit.shapes(lsraf_line).insert(pya.Box(l_right+(coord+sraf_side_left),sraf_side_bottom,l_right+(coord+sraf_side_right),sraf_side_top))
            line_vert = Unit.shapes(lsraf_line).insert(pya.Box(sraf_end_left,l_top+(coord+sraf_end_bottom),sraf_end_right,l_top+(coord+sraf_end_top)))

    #Does the angle transformation for the lines for rotations
    t = pya.ICplxTrans(1,angle,0,0,0)
    Unit.shapes(lsraf_line).transform(t)

    #Removes polygons extending beyond the overlay layer by only including those within the overlay region
    r1 = pya.Region(Unit.shapes(lsraf_line))
    r2 = pya.Region(Unit.shapes(lsraf_outline))
    r_and = r1 & r2
    l_diff = layout.layer(1,0)
    r_diff = Unit.shapes(l_diff).insert(r_and)


    #Export GDS
    layout.write(f"LSRAF_test_t{tone}_s{size}_p{pitch}_l{dimension}_a{angle}_sraf{sraf}_numsrafs{sraf_num}.gds")

lsraf_cell()