#Import the needed extensions
import math
import klayout.db as db

#### PDM Functions ####

def contact_pdm(tone:str="C",size:float=0.26,pitch:float=0.78,cell_size:float=20,defect_num:int = 5,spacing:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >6 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Feature, 2-Half Missing Feature, 3-Small Extension, 4-Corner Extension, 5-Bridged Feature, 6-Etch Block")

    if defect_num == 1:
        defecttype = "Missing_Feature"
    elif defect_num == 2:
        defecttype = "Half_Missing_Feature"
    elif defect_num == 3:
        defecttype = "Small_Extension"
    elif defect_num == 4:
        defecttype = "Corner_Extension"
    elif defect_num == 5:
        defecttype = "Bridged_Feature"    
    elif defect_num == 6:
        defecttype = "Etch_Block"
    else: defecttype="Control"

    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_cont = layout.layer(1,0) #line layer, sacrificial


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    ContCell = layout.create_cell(f"{size}um_contact")

    #Define contact dimensions
    c_left = -size/2
    c_right = size/2
    c_bottom = -size/2
    c_top = size/2

    #Create the main feature shape and insert it into the ContCell
    cont_iso = db.DBox(c_left, c_bottom, c_right, c_top)
    ContCell.shapes(l_cont).insert(cont_iso)

    #Creates formatting regions for later use
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellRegion = db.Region(1000*CellBox)
    LL_point = math.ceil(((cell_size)/2)/pitch)*-pitch


#### Generate the Cell ####
        
    cont_array = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,LL_point,LL_point),
                 db.DVector(pitch,0),db.DVector(0,pitch), math.ceil((cell_size)/pitch),math.ceil((cell_size)/pitch))
    TopCell.insert(cont_array)
    TopCell.flatten(-1,True)


#### Add defect structure if applicable ####
    if defect_num == 1:
         MissingFeature = db.DBox(c_left,c_bottom,c_right,c_top)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(RemoveRegion)
    elif defect_num == 2:
         MissingFeature = db.DBox(0,c_bottom,c_right,c_top)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(RemoveRegion)
    elif defect_num == 3:
         AddingFeature = db.DBox(c_right,-size/4,c_right+size/2,size/4)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(AddingRegion)            
    elif defect_num == 4:
         AddingFeature = db.DBox(c_left-size/2,c_bottom+size/2,c_right-size/2,c_top+size/2)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(AddingRegion) 
    elif defect_num == 5:
         AddingFeature = db.DBox(c_right,-size/4,pitch-size/2,size/4)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(AddingRegion)          
    elif defect_num == 6:
         AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_cont))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(AddingRegion)  

    #Flip the tone if needed
    if tone == "C":
         Cell_shapes = db.Region(TopCell.shapes(l_cont))
         Clear_region = CellRegion - Cell_shapes
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(Clear_region)
         if defect_num == 6:
            AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
            AddingRegion = db.Region(1000*AddingFeature)
            Target = db.Region(TopCell.shapes(l_cont))
            AddingRegion = Target | AddingRegion
            TopCell.shapes(l_cont).clear()
            TopCell.shapes(l_cont).insert(AddingRegion) 

    
    TopCell.name = (f"Cont_Array_{tone}_{size}umSize_{pitch}pitch_w_{defecttype}")

    TopCell.flatten(-1,True)
    Top_Region = db.Region(TopCell.shapes(l_cont))

    #Export GDS
    #layout.write("Cont_PDM.gds")

    return Top_Region,TopCell.name

def LS_PDM(tone:str="D",size:float=0.260,pitch:float=0.520,cell_size:float=20,horiz:bool=False,defect_num:int=5,spacing:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >6 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Line, 2-Half Missing Feature, 3-Small Extension, 4-Bridged Line, 5-Combination Defect, 6-Etch Block")

    if defect_num == 1:
        defecttype = "Missing_Line"
    elif defect_num == 2:
        defecttype = "Half_Missing_Feature"
    elif defect_num == 3:
        defecttype = "Small_Extension"
    elif defect_num == 4:
        defecttype = "Bridged_Line"
    elif defect_num == 5:
        defecttype = "Combination_Defect"
    elif defect_num == 6:
        defecttype = "Etch_Block"
    else: defecttype="Control"

    if horiz:
        angle=90
    else:
        angle=0

    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_line = layout.layer(1,0) #line layer, sacrificial

    #Conver angle from degrees to radians
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")

    #Define line dimensions (top and bottom 2x to provide extra length for angled cells)
    l_left = -size/2
    l_right = size/2
    l_bottom = -(cell_size)/2
    l_top = (cell_size)/2

    #Create the main feature shape and insert it into the LineCell cell
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_bottom, l_right, l_top))

    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellRegion = db.Region(1000*CellBox)

#### Generate the Cell ####
   
    #Instance a left and right array of the LineCell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
    ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(pitch,0),db.DVector(0,0),math.ceil(cell_size/2/pitch),0)
    ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(-pitch,0),db.DVector(0,0),math.ceil(cell_size/2/pitch),0)
    TopCell.insert(ls_array_right)
    TopCell.insert(ls_array_left)
    TopCell.flatten(-1,True)


#### Add defect structure if applicable ####
    if defect_num == 1:
         MissingFeature = db.DBox(l_left,l_left,l_right,l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(RemoveRegion)
    elif defect_num == 2:
         MissingFeature = db.DBox(l_left,l_left,0,l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(RemoveRegion)
    elif defect_num == 3:
         AddingFeature = db.DBox(l_right,-size/2,l_right+size/2,size/2)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(AddingRegion)            
    elif defect_num == 4:
         AddingFeature = db.DBox(l_right,-size/2,pitch-size/2,size/2)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(AddingRegion) 
    elif defect_num == 5:
         AddingFeature = db.DBox(l_right,-size,l_right+size/2,0)
         AddingRegion = db.Region(1000*AddingFeature)
         MissingFeature = db.DBox(0,0,l_right,size)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         FinalRegion = AddingRegion - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(FinalRegion)  
    elif defect_num == 6:
         AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(AddingRegion) 

#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    TopCell.transform(t)

    #Flip the tone if needed
    if tone == "C":
         Cell_shapes = db.Region(TopCell.shapes(l_line))
         Clear_region = CellRegion - Cell_shapes
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(Clear_region)
         if defect_num == 6:
            AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
            AddingRegion = db.Region(1000*AddingFeature)
            Target = db.Region(TopCell.shapes(l_line))
            AddingRegion = Target | AddingRegion
            TopCell.shapes(l_line).clear()
            TopCell.shapes(l_line).insert(AddingRegion) 

    TopCell.name = (f"LS_Array_{tone}_{size}umSize_{angle}degrees_w_{defecttype}")

    TopCell.flatten(-1,True)
    Top_region = db.Region(TopCell.shapes(l_line))
    
    #Export GDS
    #layout.write("LS_PDM.gds")

    return Top_region,TopCell.name

def SRAF_PDM(tone:str="D",size:float=0.260,pitch:float=1.880,cell_size:float=20,horiz:bool=False,sraf_size:float=0.050,sraf_step:float=0.26,sraf_num:int=2,defect_num:int=5,spacing:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >6 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Line, 2-Half Missing Feature, 3-Small Extension, 4-Bridged Line, 5-Combination Defect, 6-Etch Block")

    if defect_num == 1:
        defecttype = "Missing_Line"
    elif defect_num == 2:
        defecttype = "Half_Missing_Feature"
    elif defect_num == 3:
        defecttype = "Small_Extension"
    elif defect_num == 4:
        defecttype = "Missing_SRAF"
    elif defect_num == 5:
        defecttype = "Shifted_SRAF"
    elif defect_num == 6:
        defecttype = "Etch_Block"
    else: defecttype="Control"

    if horiz:
        angle=0
    else:
        angle=90
    
    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_line = layout.layer(1,0)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")
    srafSideCell = layout.create_cell(f"{sraf_size}um_side_SRAF")

    #Define line dimensions
    l_left = -size/2
    l_right = size/2
    l_bottom = -(cell_size)/2
    l_top = (cell_size)/2

    #Define sraf dimensions
    sraf_side_left = -sraf_size/2
    sraf_side_right = sraf_size/2
    sraf_side_top = l_top
    sraf_side_bottom = l_bottom

    #Create the main feature shapes and insert it into their respective cells
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_bottom, l_right, l_top))
    srafSideCell.shapes(l_line).insert(db.DBox(sraf_side_left, sraf_side_bottom, sraf_side_right, sraf_side_top))

    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellRegion = db.Region(1000*CellBox)
    pitch = 2*((2*size)+(sraf_size))
    num_lines = math.ceil(cell_size/pitch)


#### Generate the Cell ####

    #Create sraf sub-instances
    if sraf_num>1:
         srafSideGroup = layout.create_cell("SRAF_side_instance")
         
         srafSideInst1a = db.DCellInstArray(srafSideCell,db.DTrans(db.DTrans.M0,-(1.5*size+sraf_size/2),0),db.DVector(-(size+sraf_size),0),db.DVector(0,0),sraf_num,0)
         srafSideInst1b = db.DCellInstArray(srafSideCell,db.DTrans(db.DTrans.M90,(1.5*size+sraf_size/2),0),db.DVector((size+sraf_size),0),db.DVector(0,0),sraf_num,0)
         srafSideGroup.insert(srafSideInst1a)
         srafSideGroup.insert(srafSideInst1b)

    else:
         srafSideGroup = srafSideCell

    #Add SRAF instances to the LineCell
    srafSideToLine = db.DCellInstArray(srafSideGroup,db.DTrans(db.DTrans.M0,0,0))
    LineCell.insert(srafSideToLine)

    #Create array
    LineArray1 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)
    LineArray2 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(-pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)

    TopCell.insert(LineArray1)
    TopCell.insert(LineArray2)
        
    TopCell.flatten(-1,True)

#### Add defect structures if applicable ####
    if defect_num == 1:
         MissingFeature = db.DBox(l_left,l_left,l_right,l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(RemoveRegion)
    elif defect_num == 2:
         MissingFeature = db.DBox(0,l_left,l_right,l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         RemoveRegion = Target - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(RemoveRegion)
    elif defect_num == 3:
         AddingFeature = db.DBox(l_right,l_left,2*l_right,l_right)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(AddingRegion)            
    elif defect_num == 4:
         MissingFeature = db.DBox(l_right+sraf_step,2*l_left,l_right+sraf_step+sraf_size,2*l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         MissingRegion = Target - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(MissingRegion) 
    elif defect_num == 5:
         AddingFeature = db.DBox(l_right+sraf_step/2,2*l_left,l_right+sraf_step/2+sraf_size,2*l_right)
         AddingRegion = db.Region(1000*AddingFeature)
         MissingFeature = db.DBox(l_right+sraf_step,2*l_left,l_right+sraf_step+sraf_size,2*l_right)
         MissingRegion = db.Region(1000*MissingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         FinalRegion = AddingRegion - MissingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(FinalRegion)
    elif defect_num == 6:
         AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
         AddingRegion = db.Region(1000*AddingFeature)
         Target = db.Region(TopCell.shapes(l_line))
         AddingRegion = Target | AddingRegion
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(AddingRegion) 

#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    TopCell.transform(t)

    #Flip the tone if needed
    if tone == "C":
         Cell_shapes = db.Region(TopCell.shapes(l_line))
         Clear_region = CellRegion - Cell_shapes
         TopCell.shapes(l_line).clear()
         TopCell.shapes(l_line).insert(Clear_region)
         if defect_num == 6:
            AddingFeature = db.DBox(-5*size,-5*size,5*size,5*size)
            AddingRegion = db.Region(1000*AddingFeature)
            Target = db.Region(TopCell.shapes(l_line))
            AddingRegion = Target | AddingRegion
            TopCell.shapes(l_line).clear()
            TopCell.shapes(l_line).insert(AddingRegion) 

    TopCell.name = (f"Line_w_SRAF_{tone}_{size}umSize_{angle}degrees_{sraf_num}SRAFs_{sraf_size}um_size_w_{defecttype}")

    TopCell.flatten(-1,True)
    Top_region = db.Region(TopCell.shapes(l_line))

    #Export GDS
    #layout.write("SRAF_PDM.gds")

    return Top_region,TopCell.name

def FullField_PDM(tone:str="C",size:float=0.520,cell_size:float=20,defect_num:int=2,min_size_limit:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >2 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Single Defect, 2-Multiple Defects")

    if defect_num == 1:
        defecttype = "Single_Defect"
    elif defect_num == 2:
        defecttype = "Multiple_Defects"
    else: defecttype="Control"
    
    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_cont = layout.layer(1,0)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")

    #Define line dimensions
    l_left = -size/2
    l_right = size/2
    l_bottom = -size/2
    l_top = size/2

    #Create the main feature shapes and insert it into their respective cells
    if defect_num>0:
        TopCell.shapes(l_cont).insert(db.DBox(l_left, l_bottom, l_right, l_top))

    #Setup initial conditions and parameters
    current_radius = 2*size
    current_angle = math.pi/5
    da = math.pi/5
    dr = size/2
    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellRegion = db.Region(1000*CellBox)
    num_cont = 1
    current_size = size/2
    pos = []
    neg = []
    size_store = []
    
    #Corrects if no min-size limit defined
    if min_size_limit<=40:
         min_size_limit=40
    
    #Places the defect features
    while current_size > min_size_limit:
        pos.append(db.DPoint(current_radius*math.cos(current_angle),current_radius*math.sin(current_angle)))
        neg.append(db.DPoint(-current_radius*math.cos(current_angle),-current_radius*math.sin(current_angle)))
        current_radius += dr
        current_angle = (current_angle+da)%(2*math.pi)
        current_size = current_size/2
        size_store.append(current_size)
        num_cont+=1



#### Add defect structures if applicable ####
    if defect_num == 2:
         [TopCell.shapes(l_cont).insert(db.DBox(-size_store[i],-size_store[i],size_store[i],size_store[i]).move(db.DVector(pos[i]))) for i in range(len(size_store))]
         [TopCell.shapes(l_cont).insert(db.DBox(-size_store[i],-size_store[i],size_store[i],size_store[i]).move(db.DVector(neg[i]))) for i in range(len(size_store))]

  

    if tone=="C":
         Shapes = db.Region(TopCell.shapes(l_cont))
         DarkField = CellRegion-Shapes
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(DarkField)
    else:
         TopCell.shapes(l_cont).insert(db.DBox(-cell_size/2,-cell_size/2,-cell_size/2 + 1,cell_size/2))
         TopCell.shapes(l_cont).insert(db.DBox(-cell_size/2,-cell_size/2,cell_size/2,-cell_size/2 + 1))
         TopCell.shapes(l_cont).insert(db.DBox(cell_size/2 - 1,-cell_size/2,cell_size/2,cell_size/2))
         TopCell.shapes(l_cont).insert(db.DBox(-cell_size/2,cell_size/2 - 1,cell_size/2,cell_size/2))

    TopCell.name = (f"FullField_{tone}_{size}umSize_w_{defecttype}")

    TopCell.flatten(-1,True)
    Top_region = db.Region(TopCell.shapes(l_cont))

    #Export GDS
    #layout.write("FullField_PDM.gds")

    return Top_region,TopCell.name

