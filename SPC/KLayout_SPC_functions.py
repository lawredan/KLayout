#Import the needed extensions
import math
import klayout.db as db

### Helper Functions ###

def CorrectToneOutput(layout:db.Layout,output_region,layer,cell_size,size,CellBox,CellBox_region,tone):
    sacrifice_cell = layout.create_cell("Sacrificial")
    sacrifice_cell.shapes(layer).insert(output_region)
    no_sliver_shapes = sacrifice_cell.begin_shapes_rec_overlapping(layer,((cell_size-min(4*size,1))/cell_size)*CellBox)
    output_region = db.Region(no_sliver_shapes)

    if tone == "C":
         output_region = CellBox_region - output_region
    else:
         output_region = CellBox_region & output_region
         
         
    sacrifice_cell.prune_cell()
    return output_region

def SliverChecker(angle,layout,TopCell,CellBox,size,layer):
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    sliver_checker = min(size/2,0.3/2) #defines sliver size based on minimum of feature size and a fixed value in um
    size_check = db.DBox(-sliver_checker,-sliver_checker,sliver_checker,sliver_checker)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(layer).width()<size_check.bbox().width() or layout.cell(j).dbbox(layer).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    return output_cell


#### SPC Cell Functions ####
def LS_cell(name:str="LS_Cell",tone:str="D",size:float=0.100,pitch:float=0.500,cell_size:float=25,angle:float=0,metro_structure:bool=True,metro_spacing:float=8):
    
#### Function definition ####
    """
@brief Function for generating a cell containing line or space structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Defines the width of the feature (in um).
    
    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.
    
    cell_size -- Defines the size of the square cell area (in um).
    
    angle -- Defines the angle of the feature (in degrees).
    
    metro_structure -- Determines whether metrology structure(s) are added to the cell.
    
    metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).
\n
---
\n
Return definitions:
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    angle -- Provides the angle used (in degrees).
    
    metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####
    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create a layout for use
    layout = db.Layout()
    layout.dbu = 0.001 #um, database units

    #Define initial layers
    l_line = layout.layer(1,0) #line layer, sacrificial

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.05 #boolean
    bar3 = pitch_check > 0.81 #boolean

    #Determine naming based on density
    if iso:
        pitch_type = 'iso'
    elif bar3:
        pitch_type = '3bar'
    else:
        pitch_type = f"{pitch}umPitch"

    #Convert angle from degrees to radians for calculations
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")

    #Define line dimensions. Top+Bottom is 2x cell size in order to provide extra length for angled features to fill the cell area.
    l_left = -size/2
    l_right = size/2
    l_2bottom = -cell_size
    l_2top = cell_size

    #Create the main feature shape and insert it into the LineCell cell
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_2bottom, l_right, l_2top))

    #Creates formatting regions for use later on
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)


#### Generate the cell features ####

    #Checks density to determine how to build the cell
    if iso:
        #Create instance array of the iso line (1 feature) and instert into the TopCell
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)

    elif bar3:
        #Create the two sides of the 3-bar feature
        Bar3Cell = layout.create_cell(f"{size}um_3bar_structure")
        Bar3Cell.shapes(l_line).insert(db.DBox(-cell_size,-cell_size,3*l_left,cell_size))
        Bar3Cell.shapes(l_line).insert(db.DBox(3*l_right,-cell_size,cell_size,cell_size))
        
        #Add instances of both the iso line and the two 3-bar polygons into the TopCell
        ls_3bar_line = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_line)    
        ls_3bar_edge = db.DCellInstArray(Bar3Cell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_edge)

    else:
        #Otherwise, assumes a dense pattern.            
        #Instances a left and right array of the LineCell to span the TopCell region.
        #Trigonometry used to calculate step sizes to preserve pitch when angled.
        ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((pitch*math.cos(rad_angle)),-pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((-pitch*math.cos(rad_angle)),pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        TopCell.insert(ls_array_right)
        TopCell.insert(ls_array_left)


#### Add metro structures if applicable ####

    if metro_structure:
        #Metro structure is a line jog/bridge placed 'metro_spacing'um above and below the center of the cell, then inserts it as an instance array into the TopCell
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        y_metro_size = min(0.25,size) #Defines a reasonable size for the metro structure
        MetroShape = db.DBox(-size/1.9,-y_metro_size,size/1.9,y_metro_size)
        MetroCell.shapes(l_line).insert(MetroShape)
        sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
        extra_angle = -size/metro_spacing
        metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),
                                         db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),
                                         db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)
        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Fixes slivers
    output_cell = SliverChecker(angle,layout,TopCell,CellBox,size,l_line)

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_w_metro")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees")
    
    TopCell.prune_cell()

    #Flatten the structure to export as a region
    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(l_line))

    #Flip the tone if clear (room for improvement with sliver guard)
    output_region = CorrectToneOutput(layout,output_region,l_line,cell_size,size,CellBox,CellBox_region,tone)

    #Export GDS (can comment out if not testing)
    #layout.clear()
    #RLayer = layout.layer(1,0)
    #RCell = layout.create_cell("Region")
    #RCell.shapes(RLayer).insert(output_region)
    #layout.write("LS_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,angle,metro_structure

def LS_fracture_cell(name:str="LS_Cell",tone:str="D",size:float=0.100,fracture:float=0.5,pitch:float=0.500,cell_size:float=25,angle:float=0,metro_structure:bool=True,metro_spacing:float=8):
    
#### Function definition ####
    """
@brief Function for generating a cell containing line or space structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Defines the width of the feature (in um).
    
    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.
    
    cell_size -- Defines the size of the square cell area (in um).
    
    angle -- Defines the angle of the feature (in degrees).
    
    metro_structure -- Determines whether metrology structure(s) are added to the cell.
    
    metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).
\n
---
\n
Return definitions:
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    angle -- Provides the angle used (in degrees).
    
    metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####
    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create a layout for use
    layout = db.Layout()
    layout.dbu = 0.001 #um, database units

    #Define initial layers
    l_line = layout.layer(1,0) #line layer, sacrificial

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.05 #boolean
    bar3 = pitch_check > 0.81 #boolean

    #Determine naming based on density
    if iso:
        pitch_type = 'iso'
    elif bar3:
        pitch_type = '3bar'
    else:
        pitch_type = f"{pitch}umPitch"

    #Convert angle from degrees to radians for calculations
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")

    #Define line dimensions. Top+Bottom is 2x cell size in order to provide extra length for angled features to fill the cell area.
    if fracture<1 and 0<fracture:
        l_left1 = -size/2
        l_right1 = -size/2+fracture*size
        l_left2 = l_right1
        l_right2 = size/2
        l_2bottom = -cell_size
        l_2top = cell_size
        #Create the main feature shape and insert it into the LineCell cell
        LineCell.shapes(l_line).insert(db.DBox(l_left1, l_2bottom, l_right1, l_2top))
        LineCell.shapes(l_line).insert(db.DBox(l_left2, l_2bottom, l_right2, l_2top))
    else:
        l_left = -size/2
        l_right = size/2
        l_2bottom = -cell_size
        l_2top = cell_size
        #Create the main feature shape and insert it into the LineCell cell
        LineCell.shapes(l_line).insert(db.DBox(l_left, l_2bottom, l_right, l_2top))



    #Creates formatting regions for use later on
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)


#### Generate the cell features ####

    #Checks density to determine how to build the cell
    if iso:
        #Create instance array of the iso line (1 feature) and instert into the TopCell
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)

    elif bar3:
        #Create the two sides of the 3-bar feature
        Bar3Cell = layout.create_cell(f"{size}um_3bar_structure")
        Bar3Cell.shapes(l_line).insert(db.DBox(-cell_size,-cell_size,3*l_left,cell_size))
        Bar3Cell.shapes(l_line).insert(db.DBox(3*l_right,-cell_size,cell_size,cell_size))
        
        #Add instances of both the iso line and the two 3-bar polygons into the TopCell
        ls_3bar_line = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_line)    
        ls_3bar_edge = db.DCellInstArray(Bar3Cell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_edge)

    else:
        #Otherwise, assumes a dense pattern.            
        #Instances a left and right array of the LineCell to span the TopCell region.
        #Trigonometry used to calculate step sizes to preserve pitch when angled.
        ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((pitch*math.cos(rad_angle)),-pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((-pitch*math.cos(rad_angle)),pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        TopCell.insert(ls_array_right)
        TopCell.insert(ls_array_left)


#### Add metro structures if applicable ####

    if metro_structure:
        #Metro structure is a line jog/bridge placed 'metro_spacing'um above and below the center of the cell, then inserts it as an instance array into the TopCell
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        y_metro_size = min(0.25,size) #Defines a reasonable size for the metro structure
        MetroShape = db.DBox(-size/1.9,-y_metro_size,size/1.9,y_metro_size)
        MetroCell.shapes(l_line).insert(MetroShape)
        sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
        extra_angle = -size/metro_spacing
        metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),
                                         db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),
                                         db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)
        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Fixes slivers
    output_cell = SliverChecker(angle,layout,TopCell,CellBox,size,l_line)

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_w_metro")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees")
    
    TopCell.prune_cell()

    #Flatten the structure to export as a region
    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(l_line))
    #if fracture<1 and 0<fracture:
    #    output_region + db.Region(db.DBox(l_left2, l_2bottom, l_right2, l_2top))

    #Flip the tone if clear (room for improvement with sliver guard)
    output_region = CorrectToneOutput(layout,output_region,l_line,cell_size,size,CellBox,CellBox_region,tone)

    #Export GDS (can comment out if not testing)
    #layout.clear()
    #RLayer = layout.layer(1,0)
    #RCell = layout.create_cell("Region")
    #RCell.shapes(RLayer).insert(output_region)
    #layout.write("LS_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,angle,metro_structure

def contact_cell(name:str="cont_Cell",tone:str="D",size:float=0.05,pitch:float=0.100,cell_size:float=25,angle:float=0,x2y:float=1,metro_structure:bool=True,metro_spacing:float=8,
                 stagger:bool=False,HH:bool=False,HH_amount:float=0,HH_double:bool=False):
    
#### Function definition ####
    """
@brief Function for generating a cell containing 2D dot or hole structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:

    name -- Defines the cell name.

    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).

    size -- Defines the width of the feature (in um).

    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.

    cell_size -- Defines the size of the square cell area (in um).

    angle -- Defines the angle of the feature (in degrees).

    x2y -- Defines the ratio between X and Y dimensions. A '1' indicates equal X and Y dimensions. Changing this value will affect the X dimension only to satisfy the ratio.

    metro_structure -- Determines whether metrology structure(s) are added to the cell.

    metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).

    stagger -- Determines whether the array will be staggered.
\n      "False" arrays the features orthogonally.
\n      x _ x _ x
\n      x _ x _ x
\n      x _ x _ x
\n      "True" alternates or "staggers" the features.
\n      _ x _ x _
\n      x _ x _ x
\n      _ x _ x _
\n
    HH -- Determines if hammerhead OPC features will be added to the 2D structures.

    HH_amount -- Defines how large the hammerhead should be (in um). Hammerheads are currently centered on the left and right edges of the 2D structure.

    HH_Double -- If True, places HH on both feature edge pairs (X and Y). If False, HH is only on one of the edge pairs.
\n
---
\n
    Return definitions:
    
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or donut.
    
    angle -- Provides the angle used (in degrees).

    x2y -- Provides the X:Y ratio used.
    
    metro_structure -- Provides whether or not metro structure(s) were included.

    """
#NOTE: Angled mode is currently configured up to 180 degrees, but metro structures do not currently work for angles besides 0 degrees!

#### Setup ####

    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_cont = layout.layer(1,0) #line layer, sacrificial

    #Determine X and Y sizes and pitches, based on x2y value (applies to X only, Y is untouched)
    xSize = round(size*x2y,3)
    ySize = round(size,3)
    xPitch = round(pitch*x2y,3)
    yPitch = round(pitch,3)

    #Check pitch of the contact array
    pitch_check = size/pitch
    iso = False
    donut = False
    dense = False
    
    if pitch_check < 0.05:
         iso = True
    elif pitch_check > 0.81:
         donut = True
    else:
         dense=True

    #Determine naming based on density
    if iso:
        pitch_type = 'iso'
    elif donut:
        pitch_type = 'donut'
    else:
        pitch_type = f"{pitch}umPitch"

    #Convert angle from degrees to radians for calculations
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cell
    TopCell = layout.create_cell(f"Initial_cell")
    ContCell = layout.create_cell(f"{size}um_{x2y}to1_contact")

    #Define contact dimensions
    c_left = -xSize/2
    c_right = xSize/2
    c_bottom = -ySize/2
    c_top = ySize/2


    #Create the main feature shape and insert it into the ContCell
    cont_iso = db.DBox(c_left, c_bottom, c_right, c_top)
    ContCell.shapes(l_cont).insert(cont_iso)

    #Check for Hammer Head and apply if desired
    #Applies hammer heads centered on the left and right edges of the contact feature, and replaces the existing contact feature with the hammerhead-ed feature.
    if HH:
         if ySize<0.1:
            HH_width = ySize*0.3
         else:
            HH_width = 0.03
         LeftHH = db.DBox(c_left,c_bottom-HH_amount,c_left+HH_width,c_top+HH_amount)
         RightHH = db.DBox(c_right-HH_width,c_bottom-HH_amount,c_right,c_top+HH_amount)
         if x2y == 1:
            if HH_double:
                TopHH = db.DBox(c_left-HH_amount,c_top-HH_width,c_right+HH_amount,c_top)
                BottomHH = db.DBox(c_left-HH_amount,c_bottom,c_right+HH_amount,c_bottom+HH_width)            
         ContCell.shapes(l_cont).insert(LeftHH)
         ContCell.shapes(l_cont).insert(RightHH)
         if x2y == 1:
            if HH_double:
                ContCell.shapes(l_cont).insert(TopHH)
                ContCell.shapes(l_cont).insert(BottomHH)
         hammer_region = db.Region(ContCell.shapes(l_cont))
         hammer_region=hammer_region.merged()
         ContCell.shapes(l_cont).clear()
         ContCell.shapes(l_cont).insert(hammer_region)

    #Creates the stagger array structure if stagger is True
    if stagger and dense:
         StaggerCont = db.Region(ContCell.shapes(l_cont))
         StaggerCell = layout.create_cell("StaggerCell")
         StaggerCell.shapes(l_cont).insert(StaggerCont)
         StaggerInstance = db.DCellInstArray(StaggerCell,db.DTrans(),db.DVector(xPitch/2,yPitch),db.DVector(-xPitch/2,-yPitch),2,2)
         ContCell.clear()
         ContCell.insert(StaggerInstance)

                                 

    #Creates formatting regions for later use
    cont_iso_region = db.Region(ContCell.shapes(l_cont))
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)
    LittleDonut = db.DBox(-1500*(xSize),-1500*(ySize),1500*(xSize),1500*(ySize))
    LittleDonut_region = db.Region(LittleDonut)
    DonutBox = LittleDonut_region-cont_iso_region
    DonutBox.break_(4,1)


#### Generate the Cell ####

    if iso:
        #Instances a single cell into the TopCell   
        cont_iso = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_iso)

    elif donut:
        #Create the DonutCell
        DonutCell = layout.create_cell(f"{size}um_donut_structure")
        DonutCell.shapes(l_cont).insert(DonutBox)
        
        #Add all into the TopCell
        cont_donut_ring = db.DCellInstArray(DonutCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_donut_ring)

    else:        
        #Instances the contact cell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.           
        #Define vector values for instance array for dense features
        Vxx = math.cos(rad_angle)*xPitch
        Vxy = -math.sin(rad_angle)*xPitch
        Vyx = math.sin(rad_angle)*yPitch
        Vyy = math.cos(rad_angle)*yPitch

        #Changes the vector components for a stagger array due to the different stagger polygons used
        if stagger:
             Vxx = Vxx
             Vxy = Vxy
             Vyx = Vyx*2
             Vyy = Vyy*2

        URQuad = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(Vxx,Vxy),db.DVector(Vyx,Vyy),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        LRQuad = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(Vxx,Vxy),-db.DVector(Vyx,Vyy),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        LLQuad = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        -db.DVector(Vxx,Vxy),-db.DVector(Vyx,Vyy),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        ULQuad = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        -db.DVector(Vxx,Vxy),db.DVector(Vyx,Vyy),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))        

        TopCell.insert(URQuad)
        TopCell.insert(LRQuad)
        TopCell.insert(LLQuad)
        TopCell.insert(ULQuad)


    #Moved this section to after listicle purge to avoid losing the metro assist features

    #### Add metro structure for dense features if applicable ####

    #if metro_structure:
    #    MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
    #    if  not (iso or donut):
    #        MetroShape = db.DPolygon([db.DPoint(-xPitch/2+xSize/3,-ySize/2),
    #                                  db.DPoint(-xPitch/2+xSize/3,ySize/2),
    #                                  db.DPoint(xPitch/2-xSize/3,ySize/2),
    #                                  db.DPoint(xPitch/2-xSize/3,-ySize/2)])
    #        MetroCell.shapes(l_cont).insert(MetroShape)
    #        MetroXCoord = (4*xPitch-xPitch/2)
    #        MetroYCoord = (4*yPitch)
    #        MetroXCoordRotated = (round((MetroXCoord*math.cos(-rad_angle)),3)-round((MetroYCoord*math.sin(-rad_angle)),3))
    #        MetroYCoordRotated = (round((MetroXCoord*math.sin(-rad_angle)),3)+round((MetroYCoord*math.cos(-rad_angle)),3))
    #        MetroXStep = -7*xPitch
    #        MetroYStep = -8*yPitch
    #        MetroXStepRotated = (round((MetroXStep*math.cos(-rad_angle)),3)-round((MetroYStep*math.sin(-rad_angle)),3))
    #        MetroYStepRotated = (round((MetroXStep*math.sin(-rad_angle)),3)+round((MetroYStep*math.cos(-rad_angle)),3))
    #        metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,MetroXCoordRotated,MetroYCoordRotated),
    #                                         db.DVector(MetroXStepRotated,MetroYStepRotated),db.DVector(0,0),2,2)
    #        TopCell.insert(metro_insert)





#### Angle transformations, sliver removal, and output ####


    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-xSize/2,-ySize/2,xSize/2,ySize/2)

    #Prunes 
    [listicle.append(j) for j in output_cell.each_child_cell()
     if layout.cell(j).dbbox(l_cont).width()<size_check.bbox().width()
     or layout.cell(j).dbbox(l_cont).height()<size_check.bbox().height()]
    
    [layout.cell(k).prune_cell() for k in listicle]

#### Add metro structure for dense features if applicable ####

    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        if  not (iso or donut):
            MetroShape = db.DPolygon([db.DPoint(-xPitch/2+xSize/3,-ySize/2),
                                      db.DPoint(-xPitch/2+xSize/3,ySize/2),
                                      db.DPoint(xPitch/2-xSize/3,ySize/2),
                                      db.DPoint(xPitch/2-xSize/3,-ySize/2)])
            MetroCell.shapes(l_cont).insert(MetroShape)
            MetroXCoord = (4*xPitch-xPitch/2)
            MetroYCoord = (4*yPitch)
            MetroXCoordRotated = (round((MetroXCoord*math.cos(-rad_angle)),3)-round((MetroYCoord*math.sin(-rad_angle)),3))
            MetroYCoordRotated = (round((MetroXCoord*math.sin(-rad_angle)),3)+round((MetroYCoord*math.cos(-rad_angle)),3))
            MetroXStep = -7*xPitch
            MetroYStep = -8*yPitch
            MetroXStepRotated = (round((MetroXStep*math.cos(-rad_angle)),3)-round((MetroYStep*math.sin(-rad_angle)),3))
            MetroYStepRotated = (round((MetroXStep*math.sin(-rad_angle)),3)+round((MetroYStep*math.cos(-rad_angle)),3))
            metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,MetroXCoordRotated,MetroYCoordRotated),
                                             db.DVector(MetroXStepRotated,MetroYStepRotated),db.DVector(0,0),2,2)
            output_cell.insert(metro_insert)

    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in output_cell.each_child_cell()]

    #Adds metro structure now for iso/donut structures
    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        if iso or donut:
            MetroShape = db.DPolygon([db.DPoint(-0.5,0),db.DPoint(0,0.5),db.DPoint(0.5,0),db.DPoint(0,-0.5)])
            MetroCell.shapes(l_cont).insert(MetroShape)
            metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,0,-metro_spacing),
                                             db.DVector(0,2*metro_spacing),db.DVector(0,0),2,0)
            output_cell.insert(metro_insert)    

    #Apply rotation only if orthogonal
    output_cell.flatten(-1,True)

    #Rename new cell
    if HH:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees_stagger_{stagger}_{HH_amount}nm_metro_{metro_structure}")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees_stagger_{stagger}_metro_{metro_structure}")
    
    output_region = db.Region(output_cell.shapes(l_cont))
    output_region = output_region.merge()
    
    sacrifice_cell = layout.create_cell("Sacrificial")
    sacrifice_cell.shapes(l_cont).insert(output_region)
    no_sliver_shapes = sacrifice_cell.begin_shapes_rec_touching(l_cont,((cell_size-min(4*xSize,cell_size*0.05))/cell_size)*CellBox)
    output_region = db.Region(no_sliver_shapes)
    output_region = CellBox_region & output_region

    #Flip the tone if clear, with sliver check based on portion of cell size (room for improvement here...)
    if tone == "C" and not donut:
         sacrifice_cell = layout.create_cell("Sacrificial")
         sacrifice_cell.shapes(l_cont).insert(output_region)
         no_sliver_shapes = sacrifice_cell.begin_shapes_rec_touching(l_cont,((cell_size-min(4*xSize,cell_size*0.05))/cell_size)*CellBox)
         output_region = db.Region(no_sliver_shapes)
         output_region = CellBox_region - output_region
         sacrifice_cell.prune_cell()
    elif tone == "D" and donut:
         output_region = CellBox_region - output_region

    output_region.merged()
    TopCell.delete()

    #Export GDS (can comment out if not testing)
    #layout.clear()
    #RLayer = layout.layer(1,0)
    #RCell = layout.create_cell("Region")
    #RCell.shapes(RLayer).insert(output_region)
    #layout.write("Cont_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,angle,x2y,metro_structure

def SRAF_cell(name:str="SRAF_Cell",tone:str="C",size:float=0.300,pitch:float=8.500,cell_size:float=25,angle:float=45,sraf_size:float=0.05,sraf_step:float=0.2,sraf_num:int=4):

#### Function Definition ####
    """
@brief Function for generating a cell containing 1D line/space features with 1D assist structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:

    name -- Defines the cell name.

    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).

    size -- Defines the width of the primary feature (in um).

    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.

    cell_size -- Defines the size of the square cell area (in um).

    angle -- Defines the angle of the feature (in degrees). Note: Angle support only for iso structures.

    sraf_size -- Defines the width of the 1D assist structure(s) (in um).

    sraf_step -- Defines the spacing between 1D assist structures and adjacent structures (in um).

    sraf_num -- Defines the number of assist features to include. Assist features are adjacent to all four sides of the primary line/space.

---
\n
Return definitions:
    
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso or dense.
    
    angle -- Provides the angle used (in degrees).
    
    sraf_num -- Provides the number of 1D assist features used.

    sraf_size -- Provides the width of the 1D assist features (in um).

    sraf_step -- Provides the spacing between 1D assist features (in um).

    """
#NOTE:Angle support only for iso structure, No Metro structures needed

#### Setup ####

    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_line = layout.layer(1,0)

    #Check pitches, and set pitch controls for future reference
    pitch_check = size/pitch
    iso = pitch_check < 0.1 #boolean
    too_dense = pitch_check >= 0.1 #also boolean

    sraf_pitch_check = sraf_step/sraf_size
    sraf_nok = sraf_pitch_check<=2

    if sraf_nok:
         sraf_step = 3*sraf_size
         print("SRAF step size too small. Defaulting to 3x sraf size for step size")

    sraf_spacing = sraf_num*(sraf_size+sraf_step)

    if too_dense:
        pitch = 3*(size/2 + sraf_spacing)
        num_lines = math.floor(cell_size/pitch)

    #Determine naming
    if iso:
        pitch_type = 'iso'
    else:
        pitch_type = 'dense'

    #Convert angle from degrees to radians
    #rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")
    srafSideCell = layout.create_cell(f"{sraf_size}um_side_SRAF")
    srafEndCell = layout.create_cell(f"{sraf_size}um_end_SRAF")

    #Define line dimensions
    l_left = -size/2
    l_right = size/2
    l_bottom = (-cell_size/2)+(1.5*sraf_spacing)
    l_top = (cell_size/2)-(1.5*sraf_spacing)

    #Define sraf dimensions
    sraf_side_left = -sraf_size/2
    sraf_side_right = sraf_size/2
    sraf_side_top = l_top
    sraf_side_bottom = l_bottom
    sraf_end_left = l_left
    sraf_end_right = l_right
    sraf_end_bottom = -sraf_size/2
    sraf_end_top = sraf_size/2

    #Create the main feature shapes and insert it into their respective cells
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_bottom, l_right, l_top))
    srafSideCell.shapes(l_line).insert(db.DBox(sraf_side_left, sraf_side_bottom, sraf_side_right, sraf_side_top))
    srafEndCell.shapes(l_line).insert(db.DBox(sraf_end_left, sraf_end_bottom, sraf_end_right, sraf_end_top))


    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)
    BigBox = db.DBox(-cell_size,-cell_size,cell_size,cell_size)


#### Generate the Cell ####

    #Create sraf sub-instances
    if sraf_num>=1:
         srafSideGroup = layout.create_cell("SRAF_side_instance")
         srafEndGroup = layout.create_cell("SRAF_end_instance")
         
         srafSideInst1a = db.DCellInstArray(srafSideCell,db.DTrans(db.DTrans.M0,-(size+sraf_step/2),0),db.DVector(-sraf_step,0),db.DVector(0,0),sraf_num,0)
         srafSideInst1b = db.DCellInstArray(srafSideCell,db.DTrans(db.DTrans.M90,(size+sraf_step/2),0),db.DVector(sraf_step,0),db.DVector(0,0),sraf_num,0)
         srafSideGroup.insert(srafSideInst1a)
         srafSideGroup.insert(srafSideInst1b)
         
         srafEndInst1a = db.DCellInstArray(srafEndCell,db.DTrans(db.DTrans.M0,0,l_top+(size/2)+(sraf_step/2)),db.DVector(0,sraf_step),db.DVector(0,0),sraf_num,0)
         srafEndInst1b = db.DCellInstArray(srafEndCell,db.DTrans(db.DTrans.M90,0,l_bottom-((sraf_step+size)/2)),db.DVector(0,-sraf_step),db.DVector(0,0),sraf_num,0)
         srafEndGroup.insert(srafEndInst1a)
         srafEndGroup.insert(srafEndInst1b)

    else:
         srafSideGroup = srafSideCell
         srafEndGroup = srafEndCell

    #Add SRAF instances to the LineCell
    srafSideToLine = db.DCellInstArray(srafSideGroup,db.DTrans(db.DTrans.M0,0,0))
    LineCell.insert(srafSideToLine)
    srafEndToLine = db.DCellInstArray(srafEndGroup,db.DTrans(db.DTrans.M0,0,0))
    LineCell.insert(srafEndToLine)

    #Generate the actual cell
    if iso:   
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)

    else:
        #Create array
        LineArray1 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)
        LineArray2 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(-pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)

        TopCell.insert(LineArray1)
        TopCell.insert(LineArray2)


#No metro structure for this feature type


#### Angle transformations, sliver removal, and output ####
    
    if iso:
        #Apply angle rotation for all cells
        t = db.ICplxTrans(1,angle,0,0,0)
        [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{sraf_num}SRAFs_{sraf_size}um_size_{sraf_step}um_apart")
    
    TopCell.prune_cell()

    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(l_line))

    #Flip the tone if clear
    if tone == "C":
         output_region = CellBox_region - output_region

    #Export GDS
    #layout.write("SRAF_Tester.gds")

    return output_region,output_cell.name,tone,size,pitch_type,angle,sraf_num,sraf_size,sraf_step

def LEnd_cell(name:str="LineEnd_Cell",tone:str="C",size:float=0.500,pitch:float=0.600,cell_size:float=25,angle:float=40,end_spacing:float=0.2,metro_structure:bool=True,metro_spacing:float=8):

#### Function definition ####
    """
@brief Function for generatating a cell containing line or space end structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Defines the width of the feature (in um).
    
    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.
    
    cell_size -- Defines the size of the square cell area (in um).
    
    angle -- Defines the angle of the feature (in degrees).

    end_spacing -- Defines the distance between the feature ends (in um).
    
    metro_structure -- Determines whether metrology structure(s) are added to the cell.
    
    metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).
\n
---
\n
Return definitions:
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    angle -- Provides the angle used (in degrees).

    end_spacing -- Provides the end spacing used (in um).
    
    metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####

    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create the layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Define initial layers
    l_line = layout.layer(1,0) #line layer

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.05 #boolean
    bar3 = pitch_check > 0.75 #also boolean

    #Determine naming
    if iso:
        pitch_type = 'iso'
    else:
        pitch_type = f"{pitch}umPitch"

    #Conver angle from degrees to radians
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line_{end_spacing}um_end_spacing")

    #Define line dimensions (top and bottom 2x to provide extra length for angled cells)
    l_left_low = -size/2
    l_right_low = size/2
    l_bottom_low = -cell_size
    l_top_low = -end_spacing/2
    l_left_high = l_left_low
    l_right_high = l_right_low
    l_bottom_high = -l_top_low
    l_top_high = -l_bottom_low
    

    #Create the main feature shape and insert it into the LineCell cell
    LineCell.shapes(l_line).insert(db.DBox(l_left_low, l_bottom_low, l_right_low, l_top_low))
    LineCell.shapes(l_line).insert(db.DBox(l_left_high, l_bottom_high, l_right_high, l_top_high))
   

    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)
    BigBox = db.DBox(-cell_size*1000,-cell_size*1000,cell_size*1000,cell_size*1000)
    BigBox_region = db.Region(BigBox)
    DenseLine = db.DBox(-1000*pitch/2,-1000*cell_size,1000*pitch/2,1000*cell_size)
    DenseLine_region = db.Region(DenseLine)


#### Generate the Cell ####

    if iso:    
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)


    else:   
        #Instance a left and right array of the LineCell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
        ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((pitch*math.cos(rad_angle)),-pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((-pitch*math.cos(rad_angle)),pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        TopCell.insert(ls_array_right)
        TopCell.insert(ls_array_left)


#### Add metro structures if applicable ####

    if metro_structure:
        #Metro structure is a line jog/bridge placed 'metro_spacing'um above and below the center of the cell, then inserts it as an instance array into the TopCell
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        y_metro_size = min(0.25,size) #Defines a reasonable size for the metro structure
        MetroShape = db.DBox(-size/1.9,-y_metro_size,size/1.9,y_metro_size)
        MetroCell.shapes(l_line).insert(MetroShape)
        sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
        extra_angle = -size/metro_spacing
        metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),
                                         db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),
                                         db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)
        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Fixes slivers
    output_cell = SliverChecker(angle,layout,TopCell,CellBox,size,l_line)

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{end_spacing}um_spacing_w_metro")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{end_spacing}um_spacing")
    
    TopCell.prune_cell()

    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(l_line))

    #Flip the tone if clear (room for improvement with sliver guard)
    output_region = CorrectToneOutput(layout,output_region,l_line,cell_size,size,CellBox,CellBox_region,tone)

    #Export GDS
    #layout.write("LEnd_Tester.gds")

    return output_region, output_cell.name,tone,size,pitch_type,angle,end_spacing,metro_structure

def Spiral_cell(name:str="Spiral_Cell",tone:str="C",size:float=0.2,inner_r:float=1,outer_r:float=12,spacing:float=0.2,cell_size:float=25,rampancy:bool=False):
    
    #Credit to (https://www.youtube.com/watch?v=2e6DuFj0Xws), he approached it from creating a PCell in KLayout for this shape,
    #but I followed the general framework of the other functions in this file to turn this into a function that outputs a spiral cell.

#### Function definition ####
    """
@brief Function for generating a cell containing a spiral structure.
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Defines the width of the feature (in um).
    
    inner_r -- Defines the inner radius start point for the spiral from the center of the cell (in um).

    outer_r -- Defines the outer radius ending point for the spiral from the center of the cell (in um). This value must be greater than 'inner_r' but less than half of 'cell_size'.

    spacing -- Defines the distance between the spiral's coils (in um).

    cell_size -- Defines the size of the square cell area (in um).
    
    rampancy -- Determines if spiral is uniform. 'True' will cause the spiral spacing to accelarate outwards, 'False' will keep the spiral spacing uniform.
\n
---
\n
Return definitions:

    Spiral_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    Spiral_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    spacing -- Provides the spiral spacing used (in um).

    inner_r -- Provides the inner radius used (in um).

    outer_r -- Provides the outer radius used (in um).

    rampancy -- Provides whether rampancy was applied.
    
    """


#### Setup ####

    #Initial tone and dimension checks
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    if inner_r>outer_r:
           return TypeError("Error: Outer radius must be larger than inner radius!")
    if outer_r>(cell_size/2):
           return TypeError("Error: Spiral extends beyond defined cell size!")
    
    #Create layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Create Spiral cell and layer
    SpiralCell = layout.create_cell("Spiral_Cell")
    l_spiral = layout.layer(1,0)

    #Setup initial conditions and parameters
    current_radius = inner_r
    current_angle = 0
    num_points = 64
    pts = []
    da = math.pi*(2/num_points)
    dr = (size+spacing)/num_points

#### Define the spiral points ####

    while current_radius<outer_r:
           if rampancy:
              pts.append(db.DPoint(current_radius*math.cos(current_angle),current_radius*math.sin(current_angle)))
              current_radius = (current_radius**1.005)+dr
              current_angle = (current_angle+da)%(2*math.pi)
           else:
              pts.append(db.DPoint(current_radius*math.cos(current_angle),current_radius*math.sin(current_angle)))
              current_radius += dr
              current_angle = (current_angle+da)%(2*math.pi)
        
    spiral_path = db.DPath(pts,size)
    SpiralCell.shapes(l_spiral).insert(spiral_path)

    if tone=="C":
           CellBox = db.DBox(-cell_size/2,-cell_size/2,cell_size/2,cell_size/2)
           SpiralRegion = db.Region(SpiralCell.shapes(l_spiral))
           ClearSpiral = db.Region(1000*CellBox)-SpiralRegion
           SpiralCell.clear_shapes()
           SpiralCell.shapes(l_spiral).insert(ClearSpiral)

    if rampancy:
        SpiralCell.name = f'Spiral_{tone}_{size}um_{inner_r}um_inner_{outer_r}um_outer_{spacing}um_spacing_w_Rampancy'
    else:
        SpiralCell.name = f'Spiral_{tone}_{size}um_{inner_r}um_inner_{outer_r}um_outer_{spacing}um_spacing'

    #layout.write("Sprial_tester.gds")

    SpiralCell.flatten(-1,True)
    Spiral_region = db.Region(SpiralCell.shapes(l_spiral))

    return Spiral_region,SpiralCell.name,tone,size,spacing,inner_r,outer_r,spacing,rampancy

def Horn_cell(name:str="Horn_Cell",tone:str="C",initial_size:float=0.2,step_size:float=0.01,power:float=1,spacing:float=1,cell_size:float=25,angle:float=45):

#### Function definition ####
    """
@brief Function for generating a cell containing a pair of Gabriel's horn structures.
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    initial_size -- Defines the initial width of the feature (in um).

    step_size -- Defines the distance to proceed before determining the new width (in um).

    power -- Defines the factor to multiply by at each step size to determine width. A higher power yields a horn with a steep curve.

    spacing -- Defines the stopping distance for the structure in relation to cell edges and the opposite horn (in um).

    cell_size -- Defines the size of the square cell area (in um).
    
    angle -- Defines the angle of the structure (in degrees).
\n
---
\n
Return definitions:

    Horn_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    Horn_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    initial_size -- Provides the initial feature width used (in um).
    
    spacing -- Provides the structure spacing limit from adjacent structures (in um).

    angle -- Provides the angle used (in degrees).

    power -- Provides the power factor applied.
    
    """
   
#### Setup ####

    #Initial tone and dimension checks
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    
    #Create layout
    layout = db.Layout()
    layout.dbu = 0.001 #um

    #Create Spiral cell and layer
    HornCell = layout.create_cell(f"Horn_Cell_{tone}_{initial_size}um_{power}power_{angle}_degrees")
    l_horn = layout.layer(1,0)

    #Setup initial conditions and parameters
    max_range = -spacing-((-cell_size/2)+spacing)
    max_steps = max_range/step_size
    x_current = (-cell_size/2)+spacing
    y_current = initial_size/2
    x_max = -spacing
    y_max = (cell_size/2)-spacing
    pts1=[]
    pts2=[]
    neg1=[]
    neg2=[]
    step_count=1
    pts1.append(db.DPoint(x_current,y_current))
    neg1.append(db.DPoint(x_current,-y_current))
    pts2.append(db.DPoint(-x_current,y_current))
    neg2.append(db.DPoint(-x_current,-y_current))

#### Generate the polygon points ####

    #While loop to fill the lists with polygon points

    while y_current < y_max and step_count<=max_steps:
           step_count+=1
           x_current+=step_size
           y_current+=step_size*power/(max_steps/(step_count))
           pts1.append(db.DPoint(x_current,y_current))
           neg1.append(db.DPoint(x_current,-y_current))
           pts2.append(db.DPoint(-x_current,y_current))
           neg2.append(db.DPoint(-x_current,-y_current))
                  
    #Reverse the negative lists
    neg1.reverse()
    neg2.reverse()

    #Add the negative lists to the positive ones to "complete" the polygon
    [pts1.append(neg1[i]) for i in range(len(neg1))]
    [pts2.append(neg2[i]) for i in range(len(neg2))]


    #Create the polygons
    poly1 = db.DPolygon(pts1)
    poly2 = db.DPolygon(pts2)
    poly_region = db.Region([1000*poly1,1000*poly2])

    #Apply rotation if desired
    t = db.ICplxTrans(1,angle,0,0,0)
    poly_region.transform(t)

    #Flip tone if tone is "C"
    if tone == "C":
        CellBox = db.DBox(-cell_size/2,-cell_size/2,cell_size/2,cell_size/2)
        CellRegion = db.Region(1000*CellBox)
        ClearHorns = CellRegion - poly_region
        HornCell.shapes(l_horn).insert(ClearHorns)
    else:
        HornCell.shapes(l_horn).insert(poly_region)
    
    HornCell.name = f'Horn_{tone}_{initial_size}um_{power}_power_{angle}_degrees'

    HornCell.flatten(-1,True)
    Horn_region = db.Region(HornCell.shapes(l_horn))

    #layout.write("Horn_tester.gds")

    return Horn_region,HornCell.name,tone,initial_size,spacing,angle,power

def StairStep_cell(name:str="StairStep_Cell",tone:str="D",size:float=0.100,steplength:float=0.100,stepheight:float=0.200,pitch:float=0.500,cell_size:float=25,uppercornerright:bool=True,metro_structure:bool=True,metro_spacing:float=8):
    
#### Function definition ####
    """
@brief Function for generating a cell containing line or space stepladder structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- Defines the cell name.
    
    tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Defines the width of the feature (in um).
    
    steplength -- Defines the step length of the stairs (in um).

    stepheight -- Defines the step length of the stairs (in um).

    pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.
    
    cell_size -- Defines the size of the square cell area (in um).
    
    uppercornerright -- Defines the upper corner of the stairs; true is right, false is left.
    
    metro_structure -- Determines whether metrology structure(s) are added to the cell.
    
    metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).
\n
---
\n
Return definitions:
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    angle -- Provides the angle used (in degrees).
    
    metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####
    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Create a layout for use
    layout = db.Layout()
    layout.dbu = 0.001 #um, database units

    #Define initial layers
    ly_stairstep = layout.layer(1,0) #line layer, sacrificial

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.05 #boolean

    #Determine naming based on density
    if iso:
        pitch_type = 'iso'
    else:
        pitch_type = f"{pitch}umPitch"

#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    StairStepperCell = layout.create_cell("Stepper")

    #Setting up figure variables and arraying directions
    #pts =[]
    starting_x = -cell_size+0.5
    starting_y = -cell_size+0.5
    #current_point = db.DPoint(starting_x,starting_y)
    #pts.append(current_point)
    xsteps = math.floor(2*(cell_size-0.5)/steplength)
    ysteps = math.floor(2*(cell_size-0.5)/stepheight)  
    xstepdir = xsteps>ysteps

    #Creates formatting regions for use later on
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)

    #Defining the stairstep shape and its positioning, and removes slivers
    StepBox = db.DBox(starting_x,starting_y,starting_x+steplength,starting_y+stepheight)
    StairStepperCell.shapes(ly_stairstep).insert(StepBox)

    current_step=1
    num_steps = max(xsteps,ysteps)
    while current_step<=num_steps:
        StepBox1=db.DBox(starting_x+current_step*steplength,starting_y+(current_step-1)*stepheight,starting_x+(current_step+1)*steplength,starting_y+current_step*stepheight)
        StairStepperCell.shapes(ly_stairstep).insert(StepBox1)
        StepBox2=db.DBox(starting_x+current_step*steplength,starting_y+(current_step)*stepheight,starting_x+(current_step+1)*steplength,starting_y+(current_step+1)*stepheight)
        StairStepperCell.shapes(ly_stairstep).insert(StepBox2)
        current_step+=1    

    shape_right = StairStepperCell.bbox().right
    shape_left = StairStepperCell.bbox().left
    shape_top = StairStepperCell.bbox().top
    shape_bottom = StairStepperCell.bbox().bottom
    StairStepperCell.transform(db.Trans(db.Trans.R0,-(shape_right+shape_left)/2,-(shape_top+shape_bottom)))


#### Generate the cell features ####

    StairArrayerCell = layout.create_cell(f"{size}um_stairstep_{steplength}um_x_{stepheight}um_y")

    #Checks density to determine how to build the cell
    if iso:
        #Create instance array of the iso line (1 feature) and instert into the TopCell
        stairstep_iso = db.DCellInstArray(StairStepperCell,db.DTrans(db.DTrans.R0,0,0))
        StairArrayerCell.insert(stairstep_iso)

    else:
        #Otherwise, assumes a dense pattern.            
        #Instances a left and right or up and down array of the cell to span more than the TopCell region.
        if xstepdir:
            stairstep_array_positive = db.DCellInstArray(StairStepperCell,db.DTrans(db.DTrans.R0,0,0),db.DVector(pitch,0),db.DVector(0,0),math.ceil(2*cell_size/pitch),0)
            stairstep_array_negative = db.DCellInstArray(StairStepperCell,db.DTrans(db.DTrans.R0,0,0),db.DVector(-pitch,0),db.DVector(0,0),math.ceil(2*cell_size/pitch),0)
        else:
            stairstep_array_positive = db.DCellInstArray(StairStepperCell,db.DTrans(db.DTrans.R0,0,0),db.DVector(0,pitch),db.DVector(0,0),math.ceil(2*cell_size/pitch),0)
            stairstep_array_negative = db.DCellInstArray(StairStepperCell,db.DTrans(db.DTrans.R0,0,0),db.DVector(0,-pitch),db.DVector(0,0),math.ceil(2*cell_size/pitch),0)
                
        StairArrayerCell.insert(stairstep_array_positive)
        StairArrayerCell.insert(stairstep_array_negative)


    StairStepFinal = db.DCellInstArray(StairArrayerCell,db.DTrans(db.DTrans.R0,0,0))
    TopCell.insert(StairStepFinal)

#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells in the TopCell
    if uppercornerright:
        pass
    else:
        t = db.DTrans(db.DTrans.M0,0,0)
        [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate resultant child cells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    sliver_checker = min(size/2,0.3/2) #defines sliver size based on minimum of feature size and a fixed value in um
    size_check = db.DBox(-sliver_checker,-sliver_checker,sliver_checker,sliver_checker)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(ly_stairstep).width()<size_check.bbox().width() or layout.cell(j).dbbox(ly_stairstep).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_UL2LR_{uppercornerright}_w_metro")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_UL2LR_{uppercornerright}")
    
    TopCell.prune_cell()

    #Flatten the structure to export as a region
    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(ly_stairstep))

    #Flips the tone if clear, and removes any resultant slivers based on cell size (this has room for improvement)

    sacrifice_cell = layout.create_cell("Sacrificial")
    sacrifice_cell.shapes(ly_stairstep).insert(output_region)
    no_sliver_shapes = sacrifice_cell.begin_shapes_rec_overlapping(ly_stairstep,((cell_size-4*size)/cell_size)*CellBox) #Using size to limit sliver formation
    output_region = db.Region(no_sliver_shapes)
    
    if tone == "C":
         output_region = CellBox_region - output_region
    else:
         output_region = CellBox_region & output_region
    
    sacrifice_cell.prune_cell()

    #Export GDS (can comment out if not testing)
    #layout.clear()
    #RLayer = layout.layer(1,0)
    #RCell = layout.create_cell("Region")
    #RCell.shapes(RLayer).insert(output_region)
    #layout.write("StairStep_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,metro_structure

def Polygon_cell(name:str="Polygon_Cell",tone:str="D",vertices:int=6,size:float=0.200,inner_r:float=1,pitch:float=0.500,cell_size:float=25,angle:float=0,hollow:bool=True):
    
#### Function definition ####
    """
@brief Function for generating a cell containing line or space stepladder structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    name -- String; Defines the cell name.
    
    tone -- String; Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    size -- Float; Defines the width of the feature (in um).
    
    inner_r -- Float; Defines the initial inner polygon radius (in um), from center to vertice.

    vertices -- Integer; Defines the integer number of polygon vertices. Values below 3 are invalid; values above 20 will default to a circle feature.

    pitch -- Float; Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure.
    
    cell_size -- Float; Defines the size of the square cell area (in um).

    angle -- Float; Determines the polygon angle (in degrees).
    
    hollow -- Boolean; determines if inner polygon is hollow or not
\n
---
\n
Return definitions:
    output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    tone -- Provides the tone used to create the cell.
    
    size -- Provides the feature size used (in um).
    
    pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    angle -- Provides the angle used (in degrees).
    
    metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####
    #Initial tone check
    if tone in ["D","C"]: pass
    else: raise TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Initial vertices check
    if vertices>2: pass
    else: raise TypeError("Error: Vertices must number greater than 2")

    #Initial pitch check
    if pitch>size: pass
    else: raise TypeError("Error: Pitch must be larger than size")

    #Create a layout for use
    layout = db.Layout()
    layout.dbu = 0.001 #um, database units

    #Define initial layers
    ly_polygon = layout.layer(1,0) #polygon layer, sacrificial

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.05 #boolean

    #Determine naming based on density
    if iso:
        pitch_type = 'iso'
    else:
        pitch_type = f"{pitch}umPitch"

    #Determine polygon or circle
    poly_check = vertices<=20

#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    if poly_check:
        PolygonCell = layout.create_cell(f"{size}um_{vertices}side_polygon_{inner_r}um_innerradius_{pitch}um_pitch")
    else:
        PolygonCell = layout.create_cell(f"{size}um_circle_{inner_r}um_innerradius_{pitch}um_pitch")

    #Creates formatting regions for use later on
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    CellBox_region = db.Region(1000*CellBox)


#### Generate the cell features and insert into the polygoncell ####

    #Define inner polygon and some internal variables
    if not poly_check:
        vertices=360
    
    inner_pts=[]

    inner_angle = (vertices-2)*(math.pi)/(vertices*2)
    inner_r_factor = math.sin(inner_angle)

    for i in range(0,vertices+2): #Plus 2 is to fully complete the border
        if hollow:
            inner_pts.append(db.DPoint(inner_r*math.cos(i*(360/vertices)*(math.pi/180)),inner_r*math.sin(i*(360/vertices)*(math.pi/180))))
            inner_poly = db.DPath(inner_pts,size)
        else:
            inner_pts.append(db.DPoint((1/inner_r_factor)*inner_r*math.cos(i*(360/vertices)*(math.pi/180)),(1/inner_r_factor)*inner_r*math.sin(i*(360/vertices)*(math.pi/180))))
            inner_poly = db.DPolygon(inner_pts,True)

    PolygonCell.shapes(ly_polygon).insert(inner_poly)

    #Corrects the pitch so that it applies the pitch from the polygon edge, not from the polygon vertex
    pitch_angle = (180*(vertices-2)/vertices)/2
    pitch_leg = pitch*math.sin((math.pi/180)*pitch_angle)
    pitch_scale = pitch/pitch_leg

    #Alter inner_r value based on hollow-ness, correcting for edge pitch instead of vertex pitch for non-hollow structure
    if hollow:     
        pass
    else:
        inner_r -= (size/2)/math.sin((math.pi/180)*pitch_angle)


    #Defines number of polygons to draw
    poly_draw_count=1
    poly_number_count= math.floor(((cell_size/2)-inner_r)/(pitch*pitch_scale))


    #Adds radiating polygon paths if not iso
    if not iso:
        while poly_draw_count<poly_number_count:
            poly_pts=[]
            for k in range(0,vertices+2):
                poly_pts.append(db.DPoint((inner_r+(poly_draw_count*(pitch*pitch_scale)))*math.cos(k*(360/vertices)*(math.pi/180)),
                                          (inner_r+(poly_draw_count*(pitch*pitch_scale)))*math.sin(k*(360/vertices)*(math.pi/180))))
            poly_poly = db.DPath(poly_pts,size)
            PolygonCell.shapes(ly_polygon).insert(poly_poly)
            poly_draw_count+=1
    
    #Centers the cell
    #shape_right = PolygonCell.bbox().right
    #shape_left = PolygonCell.bbox().left
    #shape_top = PolygonCell.bbox().top
    #shape_bottom = PolygonCell.bbox().bottom
    #PolygonCell.transform(db.Trans(db.Trans.R0,-(shape_right+shape_left)/2,-(shape_top+shape_bottom)))

    TopCell.insert(db.DCellInstArray(PolygonCell,db.DVector(0,0)))


#### Angle transformations, sliver removal, and output ####
    
    output_cell = SliverChecker(angle,layout,TopCell,CellBox,size,ly_polygon)

    #Rename new cell, prune old cell
    if poly_check:
        output_cell.name = (f"{name}_{tone}_{vertices}side_polygon_{inner_r}um_innerradius_{pitch_type}")
    else:
        output_cell.name = (f"{name}_{tone}_{size}um_circle_{inner_r}um_innerradius_{pitch_type}")
    
    TopCell.prune_cell()

    #Flatten the structure to export as a region
    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(ly_polygon))
    output_region.merge()

    output_region = CorrectToneOutput(layout,output_region,ly_polygon,cell_size,size,CellBox,CellBox_region,tone)

    #Export GDS (can comment out if not testing)
    layout.clear()
    RLayer = layout.layer(1,0)
    RCell = layout.create_cell("Region")
    RCell.shapes(RLayer).insert(output_region)
    layout.write("Polygon_Tester.oas")

    #return output_region,output_cell.name,tone,size,pitch_type,angle

#print("test")

#contact_cell("Test","C",0.04,0.0615,35,0,1,True,8,False,False,0.004,"Inside")
#LS_cell("LS_Test","C",0.04,0.04/0.3,35)
#Horn_cell("Horn test","D")
#StairStep_cell("StairStep_Cell","D",0.1,0.3,0.1,1,25,False,True,8)
Polygon_cell("Polygon_Cell","D",8,0.2,0.2/2,0.4,35,22.5,False)