#Import the needed extensions
import math
import klayout.db as db

#### SPC Cell Functions ####
def MRC_LS_E2E_cell(name:str="LS_Cell",tone:str="D",size:float=0.100,cell_size:float=15,edge_size:float=1,spacing_buffer:float=0.500,E2E_range:list=[0.001, 0.002, 0.003],horizontal:bool=False):
    
#### Function definition ####
    """
@brief Function for generating a cell containing line or space structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:
    @param name -- Defines the cell name.
    
    @param tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).
    
    @param size -- Defines the width of the feature (in um).
       
    @param cell_size -- Defines the length of the cell (in um).

    @param edge_size -- Defines the width of the fixed edge feature (in um).
    
    @param spacing_buffer -- Defines the spacing between adjacent features (in um).
    
    @param E2E_range -- Determines which E2E spacing values to step across for the cell (in um).
    
    @param horizontal -- Boolean to determine if the lines are vertical (False) or horizontal (True).
\n
---
\n
Return definitions:
    @return output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    @return output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    @return tone -- Provides the tone used to create the cell.
    
    @return size -- Provides the feature size used (in um).
    
    @return pitch_type -- Provides the resulting pitch type: iso, dense, or 3bar.
    
    @return angle -- Provides the angle used (in degrees).
    
    @return metro_structure -- Provides whether or not metro structure(s) were included.
    """

#### Setup ####
    #Initial checks
    if tone in ["D","C"]: pass
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")
    if edge_size<(cell_size/2): pass
    else: return TypeError("Error: Edge Size too large for the provided Cell Size")

    #Create a layout for use
    layout = db.Layout()
    layout.dbu = 0.001 #um, database units

    #Define initial layers
    l_line = layout.layer(1,0) #line layer, sacrificial

    #Check the number of spacing combinations to use and the range of those combinations
    spacing_steps = len(E2E_range)
    spacing_min = min(E2E_range)
    spacing_max = max(E2E_range)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    StructureCell = layout.create_cell(f"{edge_size}um_edge_{size}um_outerline")
    LineCell = layout.create_cell(f"{size}um_innerline")

    #Create the fixed structures and place in the StructureCell
    edge_left = -(size+spacing_buffer)/2
    edge_bottom = -cell_size/2
    edge_right = -edge_left
    edge_top = edge_bottom+edge_size
    edge_box = db.DBox(edge_left,edge_bottom,edge_right,edge_top)
    
    oline_left = -size/2
    oline_right = -oline_left
    oline_top = cell_size/2
    oline_bottom = oline_top - ((oline_top-(spacing_min+spacing_max+edge_size))/2)
    oline_box = db.DBox(oline_left,oline_bottom,oline_right,oline_top)

    StructureCell.shapes(l_line).insert(edge_box)
    StructureCell.shapes(l_line).insert(oline_box)

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
        MetroShape = db.DBox(-size/1.9,-size/2,size/1.9,size/2)
        MetroCell.shapes(l_line).insert(MetroShape)
        sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
        extra_angle = -size/metro_spacing
        metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)
        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells in the TopCell
    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate resultant child cells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-size/2,-size/2,size/2,size/2)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(l_line).width()<size_check.bbox().width() or layout.cell(j).dbbox(l_line).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees_w_metro")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{angle}degrees")
    
    TopCell.prune_cell()

    #Flatten the structure to export as a region
    output_cell.flatten(-1,True)
    output_region = db.Region(output_cell.shapes(l_line))

    #Flips the tone if clear, and removes any resultant slivers based on cell size (this has room for improvement)
    if tone == "C":
         sacrifice_cell = layout.create_cell("Sacrificial")
         sacrifice_cell.shapes(l_line).insert(output_region)
         no_sliver_shapes = sacrifice_cell.begin_shapes_rec_touching(l_line,((cell_size-min(4*size,1))/cell_size)*CellBox)
         output_region = db.Region(no_sliver_shapes)
         output_region = CellBox_region - output_region
         sacrifice_cell.prune_cell()

    #Export GDS (can comment out if not testing)
    #layout.clear()
    #RLayer = layout.layer(1,0)
    #RCell = layout.create_cell("Region")
    #RCell.shapes(RLayer).insert(output_region)
    #layout.write("LS_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,angle,metro_structure
