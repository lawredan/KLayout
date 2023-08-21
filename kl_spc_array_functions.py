#Import the needed extensions
import math
import klayout.db as db
import time
import pandas as pd
from kl_feature_functions import *
from kl_pdm_functions import *


def Line_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LineArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float = 50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):

    SpaceArray = layout.create_cell("SpaceArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   
    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def Litho_Gain_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LithoGainArray = layout.create_cell("GainArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LithoGainArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LithoGainArray,db.DVector(xpos,ypos)))

def Dot_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    DotArray = layout.create_cell("DotArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   
    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))

def Hole_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    HoleArray = layout.create_cell("HoleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            HoleArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(HoleArray,db.DVector(xpos,ypos)))

def AnyAngle_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("AnyAngleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Line_Fidcol_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float = 50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LineFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Fidcol_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float = 50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):

    SpaceArray = layout.create_cell("SpaceFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def LineSpaceEnd_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float = 50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],end_spacing:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LineSpaceEndArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=LEnd_cell(tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],size[i]*end_spacing[j],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def LS_SRAF_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float = 50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],sraf_factor:list=[],sraf_step_factor:list=[],sraf_num:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LS_SRAF_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(angle)):
        for i in range(0,len(size)):
            holder=SRAF_cell(tone[i],size[i],size[i]/pitch[j],cell_size,angle[i],sraf_factor[j]*size[i],sraf_step_factor[j]*size[i],sraf_num[j],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Curvilinear_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,
                      spiral_tone:list=[],spiral_size:list=[],spiral_inner_r:list=[],spiral_outer_r:list=[],spiral_spacing:list=[],spiral_rampancy:list=[],
                      horn_tone:list=[],horn_initial_size:list=[],horn_step_size:list=[],horn_power:list=[],horn_spacing:list=[],horn_angle:list=[]):
    
    CurveArray = layout.create_cell("Curve_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y
    
    #Horn Cell

    for j in range(0,len(horn_angle)):
        for i in range(0,len(horn_initial_size)):
            holder=Horn_cell(horn_tone[i],horn_initial_size[i],horn_step_size[i],horn_power[j],horn_spacing[j],cell_size,horn_angle[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            CurveArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Spiral Cell

    for j in range(0,len(spiral_spacing)):
        for i in range(0,len(spiral_size)):
            holder=Spiral_cell(spiral_tone[i],spiral_size[i],spiral_inner_r[j],spiral_outer_r[j],spiral_spacing[j],cell_size,spiral_rampancy[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            CurveArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(CurveArray,db.DVector(xpos,ypos)))

def LCDU_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LCDU_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[i],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def LS_Repeat_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    LineArray = layout.create_cell("LSRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=LS_cell(tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def HD_Repeat_Array(layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[]):
    
    DotArray = layout.create_cell("HDRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in range(0,len(pitch)):
        for i in range(0,len(size)):
            holder=contact_cell(tone[j],size[i],round(size[i]/pitch[i],4),cell_size,angle[j],x2y[i],metro_structure[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   
    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))

#Warning, massive....
def PDM_Array(layout:db.Layout,layer:int,TopCell:db.Cell,pdm_coords:list=[],xpos:float=0,ypos:float=0):
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

