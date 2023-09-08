#Import the needed extensions
import math
import klayout.db as db

def contact_cell(name:str="cont_Cell",tone:str="D",size:float=0.05,pitch:float=0.100,cell_size:float=25,angle:float=0,x2y:float=1,metro_structure:bool=True,metro_spacing:float=8,
                 stagger:bool=False,HH:bool=False,HH_amount:float=0.05):
    
#### Function definition ####
    """
@brief Function for generating a cell containing 2D dot or hole structure(s).
\n
Uses 'klayout.db' and 'math' Python modules. Returns design information to be placed into a 'klayout.db.Layout'.
\n
---
\n
Parameter definitions:

    @param name -- Defines the cell name.

    @param tone -- Defines the feature tone, either "D" (feature is polygon) or "C" (feature is empty space).

    @param size -- Defines the width of the feature (in um).

    @param pitch -- Defines the combined width of the feature (size) and the spacing to an adjacent feature (in um). The defined feature will be arrayed across the cell extents based on this value. A size:pitch < 0.05 will result in an isolated structure. A size:pitch > 0.75 will result in a 3-bar structure.

    @param cell_size -- Defines the size of the square cell area (in um).

    @param angle -- Defines the angle of the feature (in degrees). Note: Currently only accepts angles of multiples of 90 degrees. Other angles will be ignored.

    @param x2y -- Defines the ratio between X and Y dimensions. A '1' indicates equal X and Y dimensions. Changing this value will affect the X dimension only to satisfy the ratio.

    @param metro_structure -- Determines whether metrology structure(s) are added to the cell.

    @param metro_spacing -- Defines the distance from cell center that metro structure(s) will be added (in um).

    @param stagger -- Determines whether the array will be staggered.
\n      "False" arrays the features orthogonally.
\n      x _ x _ x
\n      x _ x _ x
\n      x _ x _ x
\n      "True" alternates or "staggers" the features.
\n      _ x _ x _
\n      x _ x _ x
\n      _ x _ x _
\n
    @param HH -- Determines if hammerhead OPC features will be added to the 2D structures.

    @param HH_amount -- Defines how large the hammerhead should be (in um). Hammerheads are currently centered on the left and right edges of the 2D structure.

---
\n
Return definitions:
    
    @return output_region -- Provides the region of polygons within the cell. For more information on regions see module info for 'klayout.db.Region'.
    
    @return output_cell.name -- Provides the formatted name of the cell based on the arguements provided to the function.
    
    @return tone -- Provides the tone used to create the cell.
    
    @return size -- Provides the feature size used (in um).
    
    @return pitch_type -- Provides the resulting pitch type: iso, dense, or donut.
    
    @return angle -- Provides the angle used (in degrees).

    @return x2y -- Provides the X:Y ratio used.
    
    @return metro_structure -- Provides whether or not metro structure(s) were included.

    """
#NOTE: Angled mode is currently configured up to 180 degrees, but metro structures do not currently work for angles besides 0 degrees!

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

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
    iso = pitch_check < 0.05 #boolean
    donut = pitch_check > 0.75 #boolean

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
         #print("hammer time")
         HHwidth = HH_amount*2
         HHheight = (2*HH_amount)+ySize
         LeftHH = db.DBox(c_left-HHwidth/2,-HHheight/2,c_left+HHwidth/2,HHheight/2)
         RightHH = db.DBox(c_right-HHwidth/2,-HHheight/2,c_right+HHwidth/2,HHheight/2)
         ContCell.shapes(l_cont).insert(LeftHH)
         ContCell.shapes(l_cont).insert(RightHH)
         hammer_region = db.Region(ContCell.shapes(l_cont))
         hammer_region.merged()
         ContCell.shapes(l_cont).clear()
         ContCell.shapes(l_cont).insert(hammer_region)


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
        #cont_donut_center = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0))
        #TopCell.insert(cont_donut_center)    
        cont_donut_ring = db.DCellInstArray(DonutCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_donut_ring)

    else:        
        #Instances the contact cell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
        #NOTE: This "functions" in its current form, but needs further adjusting, especially for holes, to get a good array of angled contacts
              
        #Define vector values for instance array for dense features
        V1x1 = xPitch
        V1y1 = 0
        V1x2 = 0
        V1y2 = yPitch

        V2x1 = -xPitch
        V2y1 = 0
        V2x2 = 0
        V2y2 = yPitch

        V3x1 = -xPitch
        V3y1 = 0
        V3x2 = 0
        V3y2 = -yPitch

        V4x1 = xPitch
        V4y1 = 0
        V4x2 = 0
        V4y2 = -yPitch

        #Edit vectors if staggered placement is desired (does not currently work with angles!!!)
        if stagger:
             V1x1 = xPitch*0.5
             V1y1 = yPitch
             V1x2 = xPitch*0.5
             V1y2 = -yPitch

             V2x1 = xPitch*0.5
             V2y1 = -yPitch
             V2x2 = -xPitch*0.5
             V2y2 = -yPitch

             V3x1 = -xPitch*0.5
             V3y1 = -yPitch
             V3x2 = -xPitch*0.5
             V3y2 = yPitch

             V4x1 = -xPitch*0.5
             V4y1 = yPitch
             V4x2 = xPitch*0.5
             V4y2 = yPitch


        cont_array1 = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(V1x1,V1y1),db.DVector(V1x2,V1y2),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        cont_array2 = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(V2x1,V2y1),db.DVector(V2x2,V2y2),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        cont_array3 = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(V3x1,V3y1),db.DVector(V3x2,V3y2),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        cont_array4 = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0),
                        db.DVector(V4x1,V4y1),db.DVector(V4x2,V4y2),2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        TopCell.insert(cont_array1)
        TopCell.insert(cont_array2)
        TopCell.insert(cont_array3)
        TopCell.insert(cont_array4)



#### Add metro structures if applicable ####

    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        if iso or donut:
            MetroShape = db.DPolygon([db.DPoint(-0.5,0),db.DPoint(0,0.5),db.DPoint(0.5,0),db.DPoint(0,-0.5)])
            MetroCell.shapes(l_cont).insert(MetroShape)
            metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,0,-metro_spacing),
                                             db.DVector(0,2*metro_spacing),db.DVector(0,0),2,0)
            TopCell.insert(metro_insert)

        else:
            MetroShape = db.DPolygon([db.DPoint(-xPitch/2+xSize/2.2,-ySize/2),
                                      db.DPoint(-xPitch/2+xSize/2.2,ySize/2),
                                      db.DPoint(xPitch/2-xSize/2.2,ySize/2),
                                      db.DPoint(xPitch/2-xSize/2.2,-ySize/2)])
            MetroCell.shapes(l_cont).insert(MetroShape)
            MetroXCoord = (4*xPitch-xPitch/2)
            MetroYCoord = (4*yPitch)
            MetroXStep = -7*xPitch
            MetroYStep = -8*yPitch
            metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,MetroXCoord,MetroYCoord),
                                             db.DVector(MetroXStep,MetroYStep),db.DVector(0,0),2,2)
            TopCell.insert(metro_insert)




#### Angle transformations, sliver removal, and output ####


    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-xSize/2,-ySize/2,xSize/2,ySize/2)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(l_cont).width()<size_check.bbox().width() or layout.cell(j).dbbox(l_cont).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in output_cell.each_child_cell()]

    #Apply rotation only if orthogonal
    output_cell.flatten(-1,True)
    
    #if angle % 90 == 0:
    #    t = db.ICplxTrans(1,angle,0,0,0)
    #    output_cell.transform(t)

    #Rename new cell
    if HH:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees_stagger_{stagger}_{HH_amount}nm_HH_metro_{metro_structure}")
    else:
        output_cell.name = (f"{name}_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees_stagger_{stagger}_metro_{metro_structure}")
    
    output_region = db.Region(output_cell.shapes(l_cont))

    #Flip the tone if clear, with sliver check based on portion of cell size (room for improvement here...)
    if tone == "C" and not donut:
         sacrifice_cell = layout.create_cell("Sacrificial")
         sacrifice_cell.shapes(l_cont).insert(output_region)
         no_sliver_shapes = sacrifice_cell.begin_shapes_rec_touching(l_cont,((cell_size-min(4*size,1))/cell_size)*CellBox)
         output_region = db.Region(no_sliver_shapes)
         output_region = CellBox_region - output_region
         sacrifice_cell.prune_cell()
    elif tone == "D" and donut:
         output_region = CellBox_region - output_region

    #output_region.merged()


    #Export GDS (can comment out if not testing)
    layout.clear()
    RLayer = layout.layer(1,0)
    RCell = layout.create_cell("Region")
    RCell.shapes(RLayer).insert(output_region)
    layout.write("Cont_Tester.oas")

    return output_region,output_cell.name,tone,size,pitch_type,angle,x2y,metro_structure


contact_cell("Test","",0.2,0.5,25,30,3,True,8,True,True,0.004)