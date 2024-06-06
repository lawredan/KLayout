#Import the needed extensions
import klayout.db as db
from KLayout_SPC_functions import *
from KLayout_PDM_functions import *
import klayout.lib as lib #This is needed to access the TEXT PCELL
from tqdm import tqdm #For timing execution of the loop

"""
These functions array the functions in SPC and PDM functions.
They choose two parameters to array the cells, one vertically and one horizontally.
Changing these is currently done manually, and needs to be done carefully to avoid issues.
"""

def Line_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):

    LineArray = layout.create_cell("LineArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i]>=min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):

    SpaceArray = layout.create_cell("SpaceArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                SpaceArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                     cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):

    LithoGainArray = layout.create_cell("GainArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LithoGainArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
              cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    DotArray = layout.create_cell("DotArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=contact_cell(cellname,tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                DotArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    HoleArray = layout.create_cell("HoleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=contact_cell(cellname,tone[i],size[i],round(size[i]/pitch[j],4),cell_size,angle[j],x2y[i],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                HoleArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                   cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    LineArray = layout.create_cell("AnyAngleArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                      cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    LineArray = layout.create_cell("LineFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                       cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):

    SpaceArray = layout.create_cell("SpaceFidcolArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                SpaceArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                       cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],end_spacing:list=[],metro_structure:list=[],metro_spacing:list=[],
                       min_size_limit:float=0):
    
    LineArray = layout.create_cell("LineSpaceEndArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(angle))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LEnd_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[j],size[i]*end_spacing[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                  cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],sraf_factor:list=[],sraf_step_factor:list=[],sraf_num:list=[],min_size_limit:float=0):
    
    LineArray = layout.create_cell("LS_SRAF_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(angle))):
        for i in range(0,len(size)):
            if (size[i] >= min_size_limit) and ((sraf_factor[j]*size[i])>= min_size_limit):
                holder=SRAF_cell(cellname,tone[i],size[i],size[i]/pitch[j],cell_size,angle[i],sraf_factor[j]*size[i],sraf_step_factor[j]*size[i],sraf_num[j])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                      horn_tone:list=[],horn_initial_size:list=[],horn_step_size:list=[],horn_power:list=[],horn_spacing:list=[],horn_angle:list=[],min_size_limit:float=0):
    
    CurveArray = layout.create_cell("Curve_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y
    
    #Horn Cell

    for j in tqdm(range(0,len(horn_angle))):
        for i in range(0,len(horn_initial_size)):
            if horn_initial_size[i] >= min_size_limit:
                holder=Horn_cell(cellname,horn_tone[i],horn_initial_size[i],horn_step_size[i],horn_power[j],horn_spacing[j],cell_size,horn_angle[j])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                CurveArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos+0.9*math.cos(horn_angle[j]*math.pi/180)*(cell_size/2-horn_spacing[j]),
                                   current_y+ypos+0.9*math.sin(horn_angle[j]*math.pi/180)*(cell_size/2-horn_spacing[j]),
                                   name]) #Moves coordinate to horn ends
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    #Spiral Cell

    for j in range(0,len(spiral_spacing)):
        for i in range(0,len(spiral_size)):
            if spiral_size[i] >= min_size_limit:
                holder=Spiral_cell(cellname,spiral_tone[i],spiral_size[i],spiral_inner_r[j],spiral_outer_r[j],spiral_spacing[j],cell_size,spiral_rampancy[j])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                CurveArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos+spiral_inner_r[j],current_y+ypos+spiral_size[i]/10,name]) #Ypos addition moves the coordinate into the feature itself
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
               cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    LineArray = layout.create_cell("LCDU_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[i],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                    cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    LineArray = layout.create_cell("LSRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=LS_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                LineArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                    cell_size:float=25,tone:list=[],size:list=[],pitch:list=[],angle:list=[],x2y:list=[],metro_structure:list=[],metro_spacing:list=[],min_size_limit:float=0):
    
    DotArray = layout.create_cell("HDRepeatArray")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=contact_cell(cellname,tone[j],size[i],size[i]/pitch[j],cell_size,angle[j],x2y[j],metro_structure[i],metro_spacing[i])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                DotArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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
                        stagger:list=[],HH_list:list=[],HH_amount:list=[],min_size_limit:float=0):
    
    DotArray = layout.create_cell("HD_Stagger_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    for j in tqdm(range(0,len(pitch))):
        for i in range(0,len(size)):
            if size[i] >= min_size_limit:
                holder=contact_cell(cellname,tone[j],size[i],size[i]/pitch[i],cell_size,angle[j],x2y[j],metro_structure[i],metro_spacing[i],
                                    stagger[i],HH_list[j],HH_amount[j])
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                DotArray.insert(temparray)
                name = holder[1:]
                spc_coords.append([current_x+xpos,current_y+ypos,name])
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


#Warning, large
def Misc_Array(arrayname:str,cellname:str,layout:db.Layout,layer:int,TopCell:db.Cell,spc_coords:list=[],xpos:float=0,ypos:float=0,spacing:float=5,offset:float=50,
                        cell_size:float=25,negative_resist_tone:bool=True,min_size_limit:float=0):
    
    MiscArray = layout.create_cell("Misc_Array")

    initial_x = offset
    initial_y = offset
    current_x = initial_x
    current_y = initial_y

    #Define tone by rows
    tone=["D","C","D","C","D","C","D","C","D","C","D","C","D","C","D","C"]
    if not negative_resist_tone:
        for i in range(len(tone)):
            if tone[i] == "D":
                tone[i] = "C"
            elif tone[i] == "C":
                tone[i] = "D"
    row=0

    #18x18

    #Row 1: Large 1D Dark
    size = [1,1.5,2,2.5,3,4,5,6,7,8,9,10,12,14,15,16,18,20]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=LS_cell(cellname,tone[row],size[i],100,cell_size,0,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 2: Large 1D Clear
    size = [1,1.5,2,2.5,3,4,5,6,7,8,9,10,12,14,15,16,18,20]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=LS_cell(cellname,tone[row],size[i],100,cell_size,0,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 3: Stairstep Dark
    size = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.4 ,0.4 ,0.4, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1.0, 1.0, 1.0]
    pitch = [0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=StairStep_cell(cellname,tone[row],size[i],size[i],size[i],size[i]/pitch[i],cell_size,True,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1
    
    #Row 4: Stairstep Clear
    size = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.4 ,0.4 ,0.4, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1.0, 1.0, 1.0]
    pitch = [0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25,0.001,0.15,0.25]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=StairStep_cell(cellname,tone[row],size[i],size[i],size[i],size[i]/pitch[i],cell_size,True,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 5: CR Squares Dark (Solid)
    size = [0.04,0.04,0.04,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,0.5,0.5,0.5,1.0,1.0,1.0]
    pitch = [0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=Polygon_cell(cellname,tone[row],4,size[i],size[i]/2,size[i]/pitch[i],cell_size,45,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 6: CR Squares Clear (Solid)
    size = [0.04,0.04,0.04,0.06,0.06,0.06,0.1,0.1,0.1,0.3,0.3,0.3,0.5,0.5,0.5,1.0,1.0,1.0]
    pitch = [0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5,0.1,0.2,0.5]
    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=Polygon_cell(cellname,tone[row],4,size[i],size[i]/2,size[i]/pitch[i],cell_size,45,False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 7: Solid Shapes Dark (3,3,3,4,4,4,5,5,5,6,6,6,8,8,8,100,100,100)
    size = [0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2]
    vertices = [4,4,4,4,4,4,5,5,5,6,6,6,8,8,8,100,100,100]
    pitch = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
    angle = [0,0,0,45,45,45,0,0,0,60,60,60,67.5,67.5,67.5,0,0,0]

    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=Polygon_cell(cellname,tone[row],vertices[i],size[i],size[i]/2,size[i]/pitch[i],cell_size,-angle[i],False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1

    #Row 8: Solid Shapes Clear (3,3,3,4,4,4,5,5,5,6,6,6,8,8,8,100,100,100)
    size = [0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2,0.1,0.5,2]
    vertices = [4,4,4,4,4,4,5,5,5,6,6,6,8,8,8,100,100,100]
    pitch = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
    angle = [0,0,0,45,45,45,0,0,0,60,60,60,67.5,67.5,67.5,0,0,0]

    for i in range(0,len(size)):
        if size[i] >= min_size_limit:
            holder=Polygon_cell(cellname,tone[row],vertices[i],size[i],size[i]/2,size[i]/pitch[i],cell_size,-angle[i],False)
            tempcell=layout.create_cell(holder[1])
            tempcell.shapes(layer).insert(holder[0])
            temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
            MiscArray.insert(temparray)
            name = holder[1:]
            spc_coords.append([current_x+xpos,current_y+ypos,name])
        current_x+=(spacing+cell_size)
    current_x=initial_x
    current_y+=(spacing+cell_size)
    row+=1
   
    #Add text description of Array
    parameters = {
        "layer": db.LayerInfo(layer,0),
        "text": f"{arrayname}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    MiscArray.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(offset-cell_size/2),0)))

    TopCell.insert(db.DCellInstArray(MiscArray,db.DVector(xpos,ypos)))


#Warning, massive....
def PDM_Array(arrayname:str,layout:db.Layout,layer:int,TopCell:db.Cell,pdm_coords:list=[],xpos:float=0,ypos:float=0,negative_resist_tone:bool=True,min_size_limit:float=0):
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
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size >= min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)


#### Contacts ####
    if negative_resist_tone: tone="C"
    else: tone = "D"

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    
    size = 0.18
    pitch = 0.18+0.36
    
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=contact_pdm(tone,size,pitch,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if size >= min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.18*2
    horiz = False

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.18
    pitch = 0.18*2
    horiz = True

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=LS_PDM(tone,size,pitch,cell_size,horiz,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[3,0,3,0,3,0,3,0,3,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    defect_num=[4,0,4,0,4,0,4,0,4,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    defect_num=[5,0,5,0,5,0,5,0,5,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if sraf_size>=min_size_limit:
                holder=SRAF_PDM(tone,size,pitch,cell_size,horiz,sraf_size,sraf_step,sraf_num,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.13

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.26
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    size = 0.52
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.52
   
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.13

    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.26
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)
    
    size = 0.52
   
    defect_num=[1,0,1,0,1,0,1,0,1,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
            current_x+=(spacing+cell_size)
        current_x=initial_x
        current_y+=(spacing+cell_size)

    size = 0.52
   
    defect_num=[2,0,2,0,2,0,2,0,2,0]
    for j in range(0,row_per_def):
        for i in range(0,len(defect_num)):
            if size>=min_size_limit:
                holder=FullField_PDM(tone,size,cell_size,defect_num[i],spacing)
                tempcell=layout.create_cell(holder[1])
                tempcell.shapes(layer).insert(holder[0])
                temparray=db.DCellInstArray(tempcell,db.DVector(current_x,current_y))
                ContArray.insert(temparray)
                name = holder[1]
                pdm_coords.append([current_x+xpos,current_y+ypos,name])
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



