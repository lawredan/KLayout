#Import the needed extensions
import math
import klayout.db as db
import time
from kl_feature_functions import *
from kl_pdm_functions import *

layout = db.Layout()
layout.dbu=0.001 #um

TopCell = layout.create_cell("TopCell")
layer = layout.layer(1,0)
mask_ly = layout.layer(2,0)
TopBox = db.DBox(0,0,2398.6,4405)
TopCell.shapes(mask_ly).insert(TopBox)

spc_coords = []
pdm_coords = []

def Line_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("LineArray")
    tone="D"
    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    angle=0
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    ## Horiz Line array
    angle=90

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Array(xpos:float=0,ypos:float=0):

    SpaceArray = layout.create_cell("SpaceArray")

    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    spacing = 5 #um
    big_space = 50 #um
    tone="C"
    angle=0

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    ## Horiz Line array
    angle=90

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def Litho_Gain_Array(xpos:float=0,ypos:float=0):
    LithoGainArray = layout.create_cell("GainArray")
    tone=["D","D","C","C","D","D","C","C","D","D","C","C","D","D","C","C"]
    size=[0.8,0.8,0.8,0.8,0.8,0.35,0.35,0.35,0.35,0.35,0.25,0.25,0.25,0.25,0.25,0.1,0.1,0.1,0.1]
    pitch=0.5
    cell_size=25 #um
    angle=[0,90,0,90,0,90,0,90,45,135,45,135,45,135,45,135]

    x2y=1
    metro_structure=True
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch,cell_size,angle[j],x2y,metro_structure)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LithoGainArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LithoGainArray,db.DVector(xpos,ypos)))

def Dot_Array(xpos:float=0,ypos:float=0):
    DotArray = layout.create_cell("DotArray")
    tone="D"
    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    angle=0
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False]
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    ## 1:3 array
    x2y=3

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))

def Hole_Array(xpos:float=0,ypos:float=0):
    HoleArray = layout.create_cell("HoleArray")
    tone="C"
    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    angle=0
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False]
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            HoleArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    ## 1:3 array
    x2y=3

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            HoleArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(HoleArray,db.DVector(xpos,ypos)))

def AnyAngle_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("AnyAngleArray")
    tone=["D","D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C","C",]
    size=[0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,1,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,1]
    pitch=0.5
    cell_size=25 #um
    angle=[0,11.25,22.5,33.75,45,56.25,67.5,78.75,90,101.25,112.5,123.75,135,146.25,157.5,168.75,180]
    x2y=1
    metro_structure=False
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[i],size[i],size[i]/pitch,cell_size,angle[j],x2y,metro_structure)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Line_Fidcol_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("LineFidcolArray")
    tone="D"
    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    angle=0
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    ## Horiz Line array
    angle=90

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Fidcol_Array(xpos:float=0,ypos:float=0):

    SpaceArray = layout.create_cell("SpaceFidcolArray")

    size=[0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.5,0.6,0.8,1.0,2.0,4.0]
    pitch=[1,0.6,0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.01]
    cell_size=25 #um
    x2y=1
    metro_structure=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False]
    spacing = 5 #um
    big_space = 50 #um
    tone="C"
    angle=0

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    ## Horiz Line array
    angle=90

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone,size[i],size[i]/pitch[j],cell_size,angle,x2y,metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def LineSpaceEnd_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("LineSpaceEndArray")
    tone=["D","D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C","C",]
    size=[0.04,0.06,0.08,0.1,0.2,0.3,0.4,0.6,0.8,1.0,0.04,0.06,0.08,0.1,0.2,0.3,0.4,0.6,0.8,1.0]
    pitch=0.5
    cell_size=25 #um
    angle=[0,0,0,0,0,45,45,45,45,45,90,90,90,90,90,30,30,30,30,30]
    end_spacing = [0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0,0.5,0.75,1.0,1.5,2.0]
    metro_structure=True
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=LEnd_cell(tone[i],size[i],size[i]/pitch,cell_size,angle[j],size[i]*end_spacing[j],metro_structure)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def LS_SRAF_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("LS_SRAF_Array")
    tone=["D","D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C","C",]
    size=[0.12,0.12,0.16,0.16,0.16,0.16,0.2,0.2,0.2,0.2,0.12,0.12,0.16,0.16,0.16,0.16,0.2,0.2,0.2,0.2]
    sraf_size=[0.35,0.37,0.4,0.42,0.45,0.35,0.37,0.4,0.42,0.45,0.35,0.37,0.4,0.42,0.45,0.35,0.37,0.4,0.42,0.45]
    #sraf_step=[0.6,0.8,1.0,1.4,2,0.6,0.8,1.0,1.4,2,0.6,0.8,1.0,1.4,2,0.6,0.8,1.0,1.4,2]
    sraf_num=2
    pitch=0.005
    cell_size=25 #um
    angle=[0,0,0,0,0,45,45,45,45,45,90,90,90,90,90,30,30,30,30,30]
    
    metro_structure=True
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=SRAF_cell(tone[i],size[i],size[i]/pitch,cell_size,angle[j],sraf_size[j]*size[i],2*size[i],sraf_num,metro_structure)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Curvilinear_Array(xpos:float=0,ypos:float=0):
    CurveArray = layout.create_cell("Curve_Array")
    tone=["D","D","D","D","D","D","D","D","D","D","C","C","C","C","C","C","C","C","C","C",]
    initial_size=[0.06,0.08,0.1,0.12,0.15,0.2,0.3,0.4,0.5,1,0.06,0.08,0.1,0.12,0.15,0.2,0.3,0.4,0.5,1]
    step_size=0.01
    power=[1,2,3,1,2,3,1,2,3,1]
    cell_size=25 #um
    angle=[0,0,0,45,45,45,90,90,90,30]
    
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(initial_size)):
            holder=Horn_cell(tone[i],initial_size[i],step_size,power[j],1,cell_size,angle[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            CurveArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    inner_r = 1
    outer_r = (cell_size/2)-spacing
    little_space = [0.5,0.7,1,1.5,2,0.5,0.7,1,1.5,2]
    rampancy = [False,False,False,False,False,True,True,True,True,True]

    for j in range(0,len(angle)):
        for i in range(0,len(initial_size)):
            holder=Spiral_cell(tone[i],initial_size[i],inner_r,outer_r,little_space[j],cell_size,rampancy[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            CurveArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(CurveArray,db.DVector(xpos,ypos)))

def LCDU_Array(xpos:float=0,ypos:float=0):
    LineArray = layout.create_cell("LCDU_Array")
    tone=["D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C"]
    size=0.24
    pitch=0.5
    cell_size=25 #um
    angle=[0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90,0,90]
    x2y=1
    metro_structure=True
    spacing = 5 #um
    big_space = 50 #um

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(tone)):
            holder=LS_cell(tone[i],size,size/pitch,cell_size,angle[j],x2y,metro_structure)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))



#Warning, massive....
def PDM_Array(xpos:float=0,ypos:float=0):
    ContArray = layout.create_cell("PDM_Array")

    tone="D"
    cell_size=20 #um
    spacing = 5 #um
    big_space = 50 #um
    row_per_def = 2

    initial_x = big_space
    initial_y = big_space
    current_x = initial_x
    current_y = initial_y


#### Pillars ####
    size=0.26
    pitch=0.78

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)


#### Contacts ####
    tone="C"    

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    
    size = 0.18
    pitch = 0.18+0.36
    
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
#### Vert Line Space ####

    tone = "D"
    size = 0.26
    pitch = 0.26*2
    horiz = False

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.18*2
    horiz = False

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)


#### Horiz Line Space ####

    tone = "D"
    size = 0.26
    pitch = 0.26*2
    horiz = True

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.18*2
    horiz = True

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

#### Vert Line w/ SRAF ####

    tone = "D"
    size = 0.26
    pitch = 0.26*2
    horiz = False
    sraf_size = 0.078
    sraf_step = 0.26
    sraf_num = 2

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.26*2
    sraf_size = 0.054
    sraf_step = 0.18
    sraf_num = 2

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

#### Horiz Line w/ SRAF ####

    tone = "D"
    size = 0.26
    pitch = 0.26*2
    horiz = True
    sraf_size = 0.078
    sraf_step = 0.26
    sraf_num = 2

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.26*2
    sraf_size = 0.054
    sraf_step = 0.18
    sraf_num = 2

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)



#### Dark Field ####

    tone = "D"
    size = 0.13

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.13

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.26
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    size = 0.52
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.52
   
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)


#### Clear Field ####

    tone = "C"
    size = 0.65

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.13

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.26
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    size = 0.52
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.52
   
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            ContArray.insert(temparray)
            name = holder[1]
            pdm_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    TopCell.insert(db.DCellInstArray(ContArray,db.DVector(xpos,ypos)))


start_pos_x = 50
start_pos_y = 50
step_size = 650

startTime=time.time()
Line_Array(start_pos_x,start_pos_y)
xtime = time.time()-startTime
print(f"Done w/ Line Array after {xtime} sec")

startTime=time.time()
Space_Array(start_pos_x+step_size,start_pos_y)
xtime = time.time()-startTime
print(f"Done w/ Space Array after {xtime} sec")

startTime=time.time()
Litho_Gain_Array(start_pos_x+2*step_size,start_pos_y)
xtime = time.time()-startTime
print(f"Done w/ Litho Gain Array after {xtime} sec")

startTime=time.time()
Dot_Array(start_pos_x,start_pos_y+step_size)
xtime = time.time()-startTime
print(f"Done w/ Dot Array after {xtime} sec")

startTime=time.time()
Hole_Array(start_pos_x+step_size,start_pos_y+step_size)
xtime = time.time()-startTime
print(f"Done w/ Hole Array after {xtime} sec")

startTime=time.time()
AnyAngle_Array(start_pos_x+2*step_size,start_pos_y+step_size)
xtime = time.time()-startTime
print(f"Done w/ Any Angle Array after {xtime} sec")

startTime=time.time()
Line_Fidcol_Array(start_pos_x,start_pos_y+3*step_size)
xtime = time.time()-startTime
print(f"Done w/ Line Fidcol Array after {xtime} sec")

startTime=time.time()
Space_Fidcol_Array(start_pos_x+step_size,start_pos_y+3*step_size)
xtime = time.time()-startTime
print(f"Done w/ Space Fidcol Array after {xtime} sec")

startTime=time.time()
LineSpaceEnd_Array(start_pos_x,start_pos_y+2*step_size)
xtime = time.time()-startTime
print(f"Done w/ LEnd Array after {xtime} sec")

startTime=time.time()
LS_SRAF_Array(start_pos_x+step_size,start_pos_y+2*step_size)
xtime = time.time()-startTime
print(f"Done w/ SRAF Array after {xtime} sec")

startTime=time.time()
Curvilinear_Array(start_pos_x+2*step_size,start_pos_y+2*step_size)
xtime = time.time()-startTime
print(f"Done w/ Curvilinear Array after {xtime} sec")

startTime=time.time()
LCDU_Array(start_pos_x+2*step_size,start_pos_y+3*step_size)
xtime = time.time()-startTime
print(f"Done w/ LCDU Array after {xtime} sec")

startTime=time.time()
PDM_Array(start_pos_x+3*step_size,start_pos_y)
xtime = time.time()-startTime
print(f"Done w/ PDM Array after {xtime} sec")

startTime=time.time()
print("Writing .gds file...")
layout.write("SPC.gds")
xtime = time.time()-startTime
print(f"Finished writing file after {xtime} sec")

print(spc_coords)
print(pdm_coords)