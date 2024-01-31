#Import the needed extensions
import math
import klayout.db as db
import time
import pandas as pd
from KLayout_SPC_functions import *
from KLayout_PDM_functions import *
from KLayout_SPC_array_functions import *


def KLayout_test_Wrapper(naming:str,negative_resist_tone:bool,min_size_limit:float,curve_features:bool,offangle_features:bool):

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

    #Lists for coordinate storage during construction
    spc_coords = []

    #Define number of cells in array
    #array_x_num = 18
    #array_y_num = 18

    #Define array conditions
    spacing = 2 #um
    offset = 50 #um
    cell_size = 40 #um

    #Generate the .gds file
    start_pos_x = cell_size/2
    start_pos_y = cell_size/2
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
    tone = ["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    #X array variables
    size=[0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.25,0.3,0.35,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    metro_structure=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Y array variables
    pitch=[0.001,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,1]
    angle = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if not offangle_features:
        for i in range(len(angle)):
            angle[i] = (angle[i]//45)*45


    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Line_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")


    #### 1:1 Dot Array ####--------------------------------------------------------------------------------------------------------------------------

    y_step_size = len(pitch) * (cell_size+spacing) + 50

    #Define array position
    ArrayX = start_pos_x
    ArrayY = start_pos_y+y_step_size

    #Define names
    arrayname = "2D Dark Array 1:1AR"
    cellname = "1AR_Dot_Cell"

    #Define array parameters

    #X parameters
    tone=["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"

    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.35,0.4,0.5]
    x2y=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    metro_structure=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    metro_spacing = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

    #Y parameters
    pitch=[0.001,0.055,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.74,1]
    angle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if not offangle_features:
        for i in range(len(angle)):
            angle[i] = (angle[i]//45)*45


    #Write the cell
    print(f"Writing {arrayname}...")
    startTime=time.time()
    Dot_Array(arrayname,cellname,layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure,metro_spacing,min_size_limit)
    xtime = time.time()-startTime
    print(f"Done w/ {arrayname} after {xtime} sec...")

    #--------------------------------------------------------------------------------------------------------------------------
    #Writing the file

    startTime=time.time()
    print("Writing .oas file...")
    if negative_resist_tone: oasis_tone = "NCAR"
    else: oasis_tone = "PCAR"

    if min_size_limit>0:
        layout.write(f"{oasis_tone}_test_{naming}_{min_size_limit}um_limit.oas")
    else:
        layout.write(f"{oasis_tone}_test_{naming}_Full.oas")

    xtime = time.time()-startTime
    print(f"Finished writing file after {xtime} sec")


    #### Write the MFX file: ####
    with open(f'Test_coord_file_{naming}_{min_size_limit}um.mfx' if min_size_limit>0 else f'Test_coord_file_{naming}_Full.mfx','w') as f:
        
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
            if 'Cont' in feat_name or 'Dot' in feat_name or 'Hole' in feat_name or 'HD' in feat_name:
                angle = 90-angle
                feat_type = 'cont'
            else:
                feat_type = 'line'

            #Set measure orientation
            if angle == 0:
                scan_dir = 'x'
            elif angle == 90:
                scan_dir = 'y'
            else:
                scan_dir = 'a'
            
            #Reverse orientation for certain features
            if 'End' in feat_name or 'Horn' in feat_name:
                if angle == 0:
                    scan_dir = 'y'
                elif angle == 90:
                    scan_dir = 'x'
                else:
                    scan_dir = 'a'

            if 'Spiral' in feat_name:
                scan_dir = 'x'

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


    zTime = time.time() - initialTime
    print(f"Entire process finished in {zTime/60}min!")


#Create all the desired layouts

print(f"Starting process...")
fullstartTime=time.time()

KLayout_test_Wrapper("EBeam",True,0,True,True)


xfinaltime = time.time()-fullstartTime
print(f"Full process completed after {xfinaltime/60}min!")