#Import the needed extensions
import math
import klayout.db as db
import time
import pandas as pd
from KLayout_SPC_functions import *
from KLayout_PDM_functions import *
from KLayout_SPC_array_functions import *


def KLayout_SPC_Wrapper(negative_resist_tone:bool,min_size_limit:float):

    """
    @brief This file is used to actually generate a layout.
    It feeds parameters into the array functions, which in turn feed parameters into the SPC functions.
    This can be manually updated to fit other layout or array needs.

    @param negative_resist_tone - Boolean to define whether to have polygons written (True) or non-writte (False).
    @param min_size_limit - Defines the smallest feature size (in um) to include in the layout. Leaving as 0 will output a "Full" file, providing a number X greater than 0 will append a "X_um_limit" to the file name.
    """

    #### Initial setup ####

    #Create the layout
    layout = db.Layout()
    layout.dbu=0.001 #um

    #Create the initial structures, including masking layer
    TopCell = layout.create_cell("TopCell")
    layer = layout.layer(1,0)
    mask_ly = layout.layer(2,0)
    TopBox = db.DBox(0,0,2398.6,4405)
    TopCell.shapes(mask_ly).insert(TopBox)

    #Lists for coordinate storage during construction
    spc_coords = []
    pdm_coords = []

    #Define number of cells in array
    array_x_num = 18
    array_y_num = 18

    #Define array conditions
    spacing = 2 #um
    offset = 50 #um
    cell_size = 35 #um

    #Generate the .gds file
    start_pos_x = 25
    start_pos_y = 25
    x_step_size = 680
    y_step_size = 730

    print("Beginning cell creation process...")
    initialTime = time.time()



    #### Line Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y

    #Define array and cell naming conventions
    arrayname = "1D Dark Array"
    cellname = "Line_Cell"

    #Define array parameters
    tone = ["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.03,0.04,0.05,0.06,0.07,0.08,0.1,0.12,0.16,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Line_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Space Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+x_step_size
    ArrayY = start_pos_y

    #Define array and cell naming conventions
    arrayname = "1D Clear Array"
    cellname = "Space_Cell"

    #Define array parameters
    tone = ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.03,0.04,0.05,0.06,0.07,0.08,0.1,0.12,0.16,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Space_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Litho Gain Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+2*x_step_size
    ArrayY = start_pos_y

    #Define names
    arrayname = "Litho 1D Gain Array"
    cellname = "Litho_Gain_Cell"

    #Define array parameters
    tone=["D","D","C","C","D","D","C","C","D","D","C","C","D","D","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.8,0.8,0.8,0.8,0.35,0.35,0.35,0.35,0.25,0.25,0.25,0.25,0.1,0.1,0.1,0.1]
    pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    angle=[0,90,0,90,0,90,0,90,45,135,45,135,45,135,45,135]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Litho_Gain_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Dot Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y+y_step_size

    #Define names
    arrayname = "2D Dark Array"
    cellname = "Dot_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04,0.06,0.08,0.1,0.2,0.3,0.5,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.3,0.5,0.8,1.0]
    pitch=[1,0.65,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.65,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle=[0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    x2y=[1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Dot_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Hole Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+x_step_size
    ArrayY = start_pos_y+y_step_size

    #Define names
    arrayname = "2D Clear Array"
    cellname = "Hole_Cell"

    #Define array parameters
    tone=["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04,0.06,0.08,0.1,0.2,0.3,0.5,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.3,0.5,0.8,1.0]
    pitch=[1,0.65,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.65,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle=[0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    x2y=[1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Hole_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### AnyAngle Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+2*x_step_size
    ArrayY = start_pos_y+y_step_size

    #Define names
    arrayname = "1D Angled Array"
    cellname = "Any_Angle_LS_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3]
    pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.01]
    angle=[0,10,20,30,45,60,70,80,90,100,110,120,135,150,160,170,45,45]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    AnyAngle_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Line Fidcol Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y+3*y_step_size

    #Define names
    arrayname = "1D Dark Fidcol Array"
    cellname = "Line_Fidcol_Cell"

    #Define array parameters
    tone = ["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.03,0.04,0.05,0.06,0.07,0.08,0.1,0.12,0.16,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Line_Fidcol_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Space Fidcol Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+x_step_size
    ArrayY = start_pos_y+3*y_step_size

    #Define names
    arrayname = "1D Clear Fidcol Array"
    cellname = "Space_Fidcol_Cell"

    #Define array parameters
    tone = ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.03,0.04,0.05,0.06,0.07,0.08,0.1,0.12,0.16,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01,1,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    print(f"Writing {arrayname}...")
    startTime=time.time()
    Space_Fidcol_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Line End Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y+2*y_step_size

    #Define names
    arrayname = "1D Feature Ends Array"
    cellname = "LEnd_and_SEnd_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0]
    pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    angle=[0,0,0,0,0,45,45,45,45,45,90,90,90,90,90,30,30,30]
    end_spacing = [0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,1.0,2.0]
    metro_structure=[True,True,True,True,True,True,True,False,False,True,True,True,True,True,True,True,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    LineSpaceEnd_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,end_spacing,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### SRAF Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+x_step_size
    ArrayY = start_pos_y+2*y_step_size

    #Define names
    arrayname = "1D with Assists Array"
    cellname = "LS_SRAF_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"


    size=[0.12,0.12,0.12,0.2,0.2,0.2,0.4,0.4,0.4,0.12,0.12,0.12,0.2,0.2,0.2,0.4,0.4,0.4]
    sraf_factor=[0.25,0.25,0.3,0.3,0.35,0.35,0.25,0.25,0.3,0.3,0.35,0.35,0.25,0.25,0.3,0.3,0.35,0.35]
    sraf_step_factor=[2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5]
    sraf_num=[1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3]
    pitch=[0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005]
    angle=[0,45,90,0,45,90,0,45,90,0,45,90,0,45,90,0,45,90]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    LS_SRAF_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,sraf_factor,sraf_step_factor,sraf_num,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Curvilinear Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+2*x_step_size
    ArrayY = start_pos_y+2*y_step_size

    #Define names
    arrayname = "Curvilinear Array"
    cellname = "Curvilinear_Cell"

    #Define array parameters
    #Spiral
    spiral_tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(spiral_tone)):
            if spiral_tone[i] == "D":
                spiral_tone[i] = "C"
            elif spiral_tone[i] == "C":
                spiral_tone[i] = "D"

    spiral_size=[0.1,0.2,0.3,0.4,0.5,0.6,0.8,1,2,0.1,0.2,0.3,0.4,0.5,0.6,0.8,1,2]
    spiral_inner_r=[1,1,1,1,1,1,1,1,1]
    spiral_outer_r=[17,17,17,17,17,17,17,17,17]
    spiral_spacing=[0.2,0.3,0.5,1,2,0.2,0.3,0.5,1]
    spiral_rampancy=[False,False,False,False,False,True,True,True,True]

    #Horn
    horn_tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(horn_tone)):
            if horn_tone[i] == "D":
                horn_tone[i] = "C"
            elif tone[i] == "C":
                horn_tone[i] = "D"

    horn_initial_size=[0.06,0.08,0.1,0.12,0.15,0.2,0.4,0.6,1,0.06,0.08,0.1,0.12,0.15,0.2,0.4,0.6,1]
    horn_step_size=[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
    horn_power=[0.5,1,2,0.5,1,2,0.5,1,2]
    horn_spacing=[1,1,1,1,1,1,1,1,1]
    horn_angle=[0,0,0,45,45,45,90,90,90]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Curvilinear_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,
                    spiral_tone,spiral_size,spiral_inner_r,spiral_outer_r,spiral_spacing,spiral_rampancy,
                    horn_tone,horn_initial_size,horn_step_size,horn_power,horn_spacing,horn_angle,min_size_limit)

    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### LCDU Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+2*x_step_size
    ArrayY = start_pos_y+3*y_step_size

    #Define names
    arrayname = "1D LCDU Array"
    cellname = "LS_LCDU_Cell"

    #Define array parameters
    tone=["D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24]
    pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    angle=[0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    LCDU_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### LS Repeat Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y+4*y_step_size

    #Define names
    arrayname = "1D Repeat Array"
    cellname = "LS_Repeat_Cell"

    #Define array parameters
    tone = ["D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","D","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.06,0.06,0.06,0.1,0.1,0.1,0.2,0.2,0.2,0.3,0.3,0.3,0.5,0.5,0.5,1,1,1]
    pitch=[1,0.5,0.2,0.01,1,0.5,0.2,0.01,1,0.5,0.2,0.01,1,0.5,0.2,0.01,0.5,0.5]
    angle = [0,0,0,0,90,90,90,90,0,0,0,0,90,90,90,90,45,45]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    LS_Repeat_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### HD Repeat Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+x_step_size
    ArrayY = start_pos_y+4*y_step_size

    #Define names
    arrayname = "2D Repeat Array"
    cellname = "HD_Repeat_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04,0.04,0.04,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,0.5,0.5,0.5,2.0,2.0,2.0]
    pitch=[1,0.5,0.01,1,0.5,0.01,1,0.5,0.01,1,0.5,0.01,1,0.5,0.01,1,0.5,0.01]
    angle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    x2y=[1,1,1,2,2,2,3,3,3,1,1,1,2,2,2,3,3,3]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    HD_Repeat_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### Stagger HH Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+2*x_step_size
    ArrayY = start_pos_y+4*y_step_size

    #Define names
    arrayname = "2D Hammerhead Array"
    cellname = "HD_HH_Cell"

    #Define array parameters
    tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04, 0.04, 0.04, 0.06, 0.06, 0.06, 0.08, 0.08, 0.08, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4]
    pitch=[0.01,0.01,0.01,0.01,0.5,0.5,0.5,0.5,0.01,0.01,0.01,0.01,0.01,0.5,0.5,0.5,0.5,0.01]
    angle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    x2y=[1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,3]
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    stagger = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
    HH_list = [False,True,True,True,False,True,True,True,True,False,True,True,True,False,True,True,True,True]
    HH_amount = [0,0.004,0.008,0.016,0,0.004,0.008,0.016,0.008,0,0.004,0.008,0.016,0,0.004,0.008,0.016,0.008]
    HH_position = ["Inside","Edge","Outside","Inside","Edge","Outside","Inside","Edge","Outside","Inside","Edge","Outside","Inside","Edge","Outside","Inside","Edge","Outside"]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    HD_HH_Stagger_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure,metro_spacing,
                        stagger,HH_list,HH_amount,HH_position,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #### PDM Array ####--------------------------------------------------------------------------------------------------------------------------

    #Define array position
    ArrayX = start_pos_x+3*x_step_size
    ArrayY = start_pos_y

    #Define name
    arrayname = "Programmed Defects"

    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    PDM_Array(arrayname,layout,layer,TopCell,pdm_coords,ArrayX,ArrayY,negative_resist_tone)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")





    #--------------------------------------------------------------------------------------------------------------------------
    #Writing the file

    startTime=time.time()
    print("Writing .oas file...")
    if negative_resist_tone: oasis_tone = "NCAR"
    else: oasis_tone = "PCAR"

    if min_size_limit>0:
        layout.write(f"{oasis_tone}_Universal_SPC_{min_size_limit}um_limit.oas")
    else:
        layout.write(f"{oasis_tone}_Universal_SPC_Full.oas")

    xtime = time.time()-startTime
    print(f"Finished writing file after {xtime} sec")


    #### Write the MFX file: ####
    with open(f'SPC_coord_file_{min_size_limit}um.mfx' if min_size_limit>0 else 'SPC_coord_file_Full.mfx','w') as f:
        
        #Set up initial lines in text file
        f.write('mfxjob,')
        f.write('\n')
        f.write('align,1,10700,76200,cross,')
        f.write('\n')
        f.write('align,2,141700,76200,cross,')
        f.write('\n')

        #Iterate over coordinate list to fill out the file
        site = 1

        for lines in range(len(spc_coords)):
            
            #Define coords and feature name
            x_coord = spc_coords[lines][0]
            y_coord = spc_coords[lines][1]
            feat_name = spc_coords[lines][2][0]

            #Check angle for scan direction
            angle = spc_coords[lines][2][4]

            #Fix the contact scan direction since it was set up rotated from the LS function
            if 'Cont' in feat_name:
                angle = 90-angle
                feat_type = 'cont'
            else:
                feat_type = 'line'

            if angle == 0:
                scan_dir = 'X'
            elif angle == 90:
                scan_dir = 'Y'
            else:
                scan_dir = 'A'
            

            #Define nominal and tone
            nominal = spc_coords[lines][2][2]
            
            if spc_coords[lines][2][1] == 'D':
                tone = 'o'
            elif spc_coords[lines][2][1] == 'C':
                tone = 'c'

            f.write(f'site,{site},{x_coord},{y_coord},{feat_name},{scan_dir},{nominal},{feat_type},{tone},na,')
            f.write('\n')
            site+=1
        
        f.write('end,')


    #### Write the PDM coordinate file ####
    pdm_xcoords = []
    pdm_ycoords = []
    pdm_name = []
    for z in range(len(pdm_coords)):
        pdm_xcoords.append(pdm_coords[z][0])
        pdm_ycoords.append(pdm_coords[z][1])
        pdm_name.append(pdm_coords[z][2])

    df = pd.DataFrame({'X Coord':pdm_xcoords,'Y Coord':pdm_ycoords,'Name':pdm_name})
    df.to_csv(f'SPC_PDM_Coordinates_{min_size_limit}um.csv' if min_size_limit>0 else 'SPC_PDM_Coordinates_Full.csv')

    zTime = time.time() - initialTime
    print(f"Entire process finished in {zTime/60}min!")


#Create all the desired layouts
#KLayout_SPC_Wrapper(False,0)
#KLayout_SPC_Wrapper(False,0.05)
#KLayout_SPC_Wrapper(False,0.1)
#KLayout_SPC_Wrapper(False,0.24)
#KLayout_SPC_Wrapper(True,0)
#KLayout_SPC_Wrapper(True,0.05)
#KLayout_SPC_Wrapper(True,0.1)
KLayout_SPC_Wrapper(True,0.24)