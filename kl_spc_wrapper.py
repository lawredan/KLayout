#Import the needed extensions
import math
import klayout.db as db
import time
import pandas as pd
from kl_feature_functions import *
from kl_pdm_functions import *
from kl_spc_array_functions import *

layout = db.Layout()
layout.dbu=0.001 #um

TopCell = layout.create_cell("TopCell")
layer = layout.layer(1,0)
mask_ly = layout.layer(2,0)
TopBox = db.DBox(0,0,2398.6,4405)
TopCell.shapes(mask_ly).insert(TopBox)

spc_coords = []
pdm_coords = []

#Define number of cells in array
array_x_num = 18
array_y_num = 18



#Generate the .gds file
start_pos_x = 35
start_pos_y = 35
step_size = 700

print("Beginning cell creation process...")


#--------------------------------------------------------------------------------------------------------------------------
#Line Array 

ArrayX = start_pos_x
ArrayY = start_pos_y

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone = ["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.2,0.3,0.4,0.6,0.8,1.0,2.0,4.0]
line_pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]

startTime=time.time()

Line_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,line_pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Line Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Space Array

ArrayX = start_pos_x+step_size
ArrayY = start_pos_y

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone = ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.2,0.3,0.4,0.6,0.8,1.0,2.0,4.0]
space_pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]

startTime=time.time()

Space_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,space_pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Space Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Litho Gain Array

ArrayX = start_pos_x+2*step_size
ArrayY = start_pos_y

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","D","C","C","D","D","C","C","D","D","C","C","D","D","C","C"]
size=[0.8,0.8,0.8,0.8,0.35,0.35,0.35,0.35,0.25,0.25,0.25,0.25,0.1,0.1,0.1,0.1]
pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
angle=[0,90,0,90,0,90,0,90,45,135,45,135,45,135,45,135]
x2y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]

startTime=time.time()

Litho_Gain_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Litho Gain Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Dot Array

ArrayX = start_pos_x
ArrayY = start_pos_y+step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
size=[0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0]
pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle=[0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y=[1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False]

startTime=time.time()

Dot_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Dot Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Hole Array

ArrayX = start_pos_x+step_size
ArrayY = start_pos_y+step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
size=[0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0]
pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle=[0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y=[1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False]

startTime=time.time()

Hole_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Hole Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#AnyAngle Array

ArrayX = start_pos_x+2*step_size
ArrayY = start_pos_y+step_size

spacing = 5 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
size=[0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3]
pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
angle=[0,10,20,30,45,60,70,80,90,100,110,120,135,150,160,170,0,90]
x2y=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]


startTime=time.time()

AnyAngle_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Any Angle Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Line Fidcol Array

ArrayX = start_pos_x
ArrayY = start_pos_y+3*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone = ["D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D","D"]
size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.2,0.3,0.4,0.6,0.8,1.0,2.0,4.0]
pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]

startTime=time.time()

Line_Fidcol_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Line Fidcol Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Space Fidcol Array

ArrayX = start_pos_x+step_size
ArrayY = start_pos_y+3*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone = ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]
size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.2,0.3,0.4,0.6,0.8,1.0,2.0,4.0]
pitch=[1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01,1,0.6,0.5,0.4,0.3,0.2,0.15,0.1,0.01]
angle = [0,0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,90,90]
x2y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]

startTime=time.time()

Space_Fidcol_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ Space Fidcol Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#Line End Array

ArrayX = start_pos_x
ArrayY = start_pos_y+2*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
size=[0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1.0]
pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
angle=[0,0,0,0,0,45,45,45,45,45,90,90,90,90,90,30,30,30]
end_spacing = [0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,1.0,2.0]
metro_structure=[True,True,True,True,True,True,True,False,False,True,True,True,True,True,True,True,False,False]

startTime=time.time()
LineSpaceEnd_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,end_spacing,metro_structure)
xtime = time.time()-startTime
print(f"Done w/ LEnd Array after {xtime} sec...")

#--------------------------------------------------------------------------------------------------------------------------
#SRAF Array

ArrayX = start_pos_x+step_size
ArrayY = start_pos_y+2*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
size=[0.12,0.12,0.12,0.2,0.2,0.2,0.4,0.4,0.4,0.12,0.12,0.12,0.2,0.2,0.2,0.4,0.4,0.4]
sraf_factor=[0.25,0.25,0.3,0.3,0.35,0.35,0.25,0.25,0.3,0.3,0.35,0.35,0.25,0.25,0.3,0.3,0.35,0.35]
sraf_step_factor=[2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5,2.5,3.5]
sraf_num=[1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3]
pitch=[0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005]
angle=[0,45,90,0,45,90,0,45,90,0,45,90,0,45,90,0,45,90]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]

startTime=time.time()

LS_SRAF_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,sraf_factor,sraf_step_factor,sraf_num,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ SRAF Array after {xtime} sec...")


#--------------------------------------------------------------------------------------------------------------------------
#Curvilinear Array

ArrayX = start_pos_x+2*step_size
ArrayY = start_pos_y+2*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

#Spiral
spiral_tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
spiral_size=[0.1,0.2,0.3,0.4,0.5,0.6,0.8,1,2,0.1,0.2,0.3,0.4,0.5,0.6,0.8,1,2]
spiral_inner_r=[1,1,1,1,1,1,1,1,1]
spiral_outer_r=[17,17,17,17,17,17,17,17,17]
spiral_spacing=[0.2,0.3,0.5,1,2,0.2,0.3,0.5,1]
spiral_rampancy=[False,False,False,False,False,True,True,True,True]

#Horn
horn_tone=["D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C"]
horn_initial_size=[0.06,0.08,0.1,0.12,0.15,0.2,0.4,0.6,1,0.06,0.08,0.1,0.12,0.15,0.2,0.4,0.6,1]
horn_step_size=[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
horn_power=[0.5,1,2,0.5,1,2,0.5,1,2]
horn_spacing=[1,1,1,1,1,1,1,1,1]
horn_angle=[0,0,0,45,45,45,90,90,90]

startTime=time.time()

Curvilinear_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,
                  spiral_tone,spiral_size,spiral_inner_r,spiral_outer_r,spiral_spacing,spiral_rampancy,
                  horn_tone,horn_initial_size,horn_step_size,horn_power,horn_spacing,horn_angle)

xtime = time.time()-startTime
print(f"Done w/ Curvilinear Array after {xtime} sec...")


#--------------------------------------------------------------------------------------------------------------------------
#LCDU Array

ArrayX = start_pos_x+2*step_size
ArrayY = start_pos_y+3*step_size

spacing = 2 #um
offset = 50 #um
cell_size = 35 #um

tone=["D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C"]
size=[0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24,0.24]
pitch=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
angle=[0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90]
x2y=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]

startTime=time.time()

LCDU_Array(layout,layer,TopCell,spc_coords,ArrayX,ArrayY,spacing,offset,cell_size,tone,size,pitch,angle,x2y,metro_structure)

xtime = time.time()-startTime
print(f"Done w/ LCDU Array after {xtime} sec...")



#--------------------------------------------------------------------------------------------------------------------------
#PDM Array

ArrayX = start_pos_x+2.9*step_size
ArrayY = start_pos_y

startTime=time.time()

PDM_Array(layout,layer,TopCell,pdm_coords,ArrayX,ArrayY)

xtime = time.time()-startTime
print(f"Done w/ PDM Array after {xtime} sec...")




startTime=time.time()
print("Writing .oas file...")
layout.write("SPC.oas")
xtime = time.time()-startTime
print(f"Finished writing file after {xtime} sec")


#### Write the MFX file: ####
with open('SPC_coord_file.mfx','w') as f:
    
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
df.to_csv('SPC_PDM_Coordinates.csv')
