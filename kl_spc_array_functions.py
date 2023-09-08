#Import the needed extensions
import klayout.db as db
from kl_feature_functions import *
from kl_pdm_functions import *
import klayout.lib as lib #This is needed to access the TEXT PCELL
from tqdm import tqdm #For timing execution of the loop

"""
These functions array the functions in "kl_feature_functions" and "kl_pdm_functions".
They choose two parameters to array the cells, one vertically and one horizontally.
Changing these is currently done manually, and needs to be done carefully to avoid issues.
"""

def Line_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):

    LineArray = layout.create_cell("LineArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))


    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):

    SpaceArray = layout.create_cell("SpaceArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    SpaceArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))
   

    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def Litho_Gain_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                     cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):

    LithoGainArray = layout.create_cell("GainArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LithoGainArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LithoGainArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))
    
    TopCell.insert(db.DCellInstArray(LithoGainArray,db.DVector(xpos,ypos)))

def Dot_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
              cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    DotArray = layout.create_cell("DotArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=contact_cell(cellname,tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   

    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    DotArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))

def Hole_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    HoleArray = layout.create_cell("HoleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=contact_cell(cellname,tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            HoleArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    HoleArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(HoleArray,db.DVector(xpos,ypos)))

def AnyAngle_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                   cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    LineArray = layout.create_cell("AnyAngleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Line_Fidcol_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                      cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    LineArray = layout.create_cell("LineFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Space_Fidcol_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                       cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):

    SpaceArray = layout.create_cell("SpaceFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            SpaceArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    SpaceArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(SpaceArray,db.DVector(xpos,ypos)))

def LineSpaceEnd_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                       cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],end_spacing:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    LineArray = layout.create_cell("LineSpaceEndArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(angle))):
        for i in range(0,len(size)):
            holder=LEnd_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],size[i]*end_spacing[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def LS_SRAF_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                  cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],sraf_factor:list=[],sraf_step_factor:list=[],sraf_num:list=[]):
    
    LineArray = layout.create_cell("LS_SRAF_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(angle))):
        for i in range(0,len(size)):
            holder=SRAF_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[i],sraf_factor[j]*size[i],sraf_step_factor[j]*size[i],sraf_num[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
        
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))
    
    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def Curvilinear_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                      cell_size:float=25,spiral_tone:list=[],spiral_size:list=[],spiral_inner_r:list=[],spiral_outer_r:list=[],spiral_spacing:list=[],spiral_rampancy:list=[],
                      horn_tone:list=[],horn_initial_size:list=[],horn_step_size:list=[],horn_power:list=[],horn_spacing:list=[],horn_angle:list=[]):
    
    CurveArray = layout.create_cell("Curve_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y
    
    #Horn Cell

    for j in tqdm(range(0,len(horn_angle))):
        for i in range(0,len(horn_initial_size)):
            holder=Horn_cell(cellname,horn_tone[i],horn_initial_size[i],horn_step_size[i],horn_power[j],horn_spacing[j],cell_size,horn_angle[j])
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
            holder=Spiral_cell(cellname,spiral_tone[i],spiral_size[i],spiral_inner_r[j],spiral_outer_r[j],spiral_spacing[j],cell_size,spiral_rampancy[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            CurveArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    CurveArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(CurveArray,db.DVector(xpos,ypos)))

def LCDU_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    LineArray = layout.create_cell("LCDU_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[i],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def LS_Repeat_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                    cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    LineArray = layout.create_cell("LSRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            LineArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    LineArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(LineArray,db.DVector(xpos,ypos)))

def HD_Repeat_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                    cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[]):
    
    DotArray = layout.create_cell("HDRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=contact_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[j],metro_structure[i],metro_spacing[i])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    DotArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))

def HD_HH_Stagger_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                        cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[],
                        stagger:list=[],HH_list:list=[],HH_amount:list=[]):
    
    DotArray = layout.create_cell("HD_HH_Stagger_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            holder=contact_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[i],metro_structure[i],metro_spacing[i],stagger[i],HH_list[j],HH_amount[j])
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            DotArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x,current_y,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
   
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    DotArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(DotArray,db.DVector(xpos,ypos)))


#Warning, massive....
def PDM_Array(arrayname:str,layout:db.Layout,layer:int,TopCell:db.Cell,pdm_coords:list=[],xpos:float=0,ypos:float=0,negative_resist_tone:bool=True):
    ContArray = layout.create_cell("PDM_Array")

    if negative_resist_tone: tone="D"
    else: tone = "C"

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
    if negative_resist_tone: tone="C"
    else: tone = "D"

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

    if negative_resist_tone:tone = "D"
    else: tone = "C"

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

    if negative_resist_tone:tone = "D"
    else: tone = "C"

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

    if negative_resist_tone: tone = "D"
    else: tone = "C"

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

    if negative_resist_tone: tone = "D"
    else: tone = "C"

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

    if negative_resist_tone: tone = "D"
    else: tone = "C"

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

    if negative_resist_tone: tone = "C"
    else: tone = "D"

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
        
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    ContArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(50-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(ContArray,db.DVector(xpos,ypos)))



