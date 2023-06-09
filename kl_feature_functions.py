# Import the needed extensions
import math
import klayout.db as db

#### SPC Cell Functions ####
def LS_cell(tone:str="D",size:float=0.100,pitch:float=0.500,cell_size:float=25,angle:float=0,x2y:float=1,metro_structure:bool = True):

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
    l_line = layout.layer(1,0) #line layer, sacrificial

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.1 #boolean
    bar3 = pitch_check > 0.75 #also boolean

    #Determine naming
    if iso:
        pitch_type = 'iso'
    elif bar3:
        pitch_type = '3bar'
    else:
        pitch_type = f"{pitch}umPitch"

    #Conver angle from degrees to radians
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
    TopCell = layout.create_cell(f"Initial_cell")
    LineCell = layout.create_cell(f"{size}um_line")

    #Define line dimensions (top and bottom 2x to provide extra length for angled cells)
    l_left = -size/2
    l_right = size/2
    l_2bottom = -cell_size
    l_2top = cell_size

    #Create the main feature shape and insert it into the LineCell cell
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_2bottom, l_right, l_2top))

    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    BigBox = db.DBox(-cell_size*1000,-cell_size*1000,cell_size*1000,cell_size*1000)
    BigBox_region = db.Region(BigBox)
    Bar3Line = db.DBox(-1000*1.5*size,-cell_size*1000,1000*1.5*size,cell_size*1000)
    Bar3Line_region = db.Region(Bar3Line)
    DenseLine = db.DBox(-1000*pitch/2,-1000*cell_size,1000*pitch/2,1000*cell_size)
    DenseLine_region = db.Region(DenseLine)


#### Generate the Cell ####

    if iso:
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            iso_region = db.Region(LineCell.shapes(l_line))
            clear_iso = iso_region ^ BigBox_region
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_iso)       
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)

    elif bar3:
        #Create the Bar3Cell
        Bar3Cell =  layout.create_cell(f"{size}um_3bar_structure")
        Bar3Cell.shapes(l_line).insert(db.DBox(-cell_size,-cell_size,3*l_left,cell_size))
        Bar3Cell.shapes(l_line).insert(db.DBox(3*l_right,-cell_size,cell_size,cell_size))
        
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            bar3_region = db.Region(LineCell.shapes(l_line))
            clear_bar3 = bar3_region ^ Bar3Line_region
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_bar3)
            Bar3Cell.clear_shapes()
        
        #Add all into the TopCell
        ls_3bar_line = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_line)    
        ls_3bar_edge = db.DCellInstArray(Bar3Cell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_3bar_edge)

    else:
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            dense_region = db.Region(LineCell.shapes(l_line))
            clear_dense = dense_region ^ DenseLine_region
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_dense)
        
        #Instance a left and right array of the LineCell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
        ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((pitch*math.cos(rad_angle)),-pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((-pitch*math.cos(rad_angle)),pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        TopCell.insert(ls_array_right)
        TopCell.insert(ls_array_left)


#### Add metro structures if applicable ####
    metro_spacing = 8 #um

    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        MetroShape = db.DBox(-size/2,-size/2,size/2,size/2)
        MetroCell.shapes(l_line).insert(MetroShape)

        if tone == "C":
             metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,-metro_spacing*math.sin(rad_angle),-metro_spacing*math.cos(rad_angle)),db.DVector(2*metro_spacing*math.sin(rad_angle),2*metro_spacing*math.cos(rad_angle)),db.DVector(0,0),2,0)
        else:
             sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
             extra_angle = -size/metro_spacing
             metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)

        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-size/2,-size/2,size/2,size/2)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(l_line).width()<size_check.bbox().width() or layout.cell(j).dbbox(l_line).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"LS_Array_{tone}_{size}umSize_{pitch_type}_{angle}degrees_w_metro")
    else:
        output_cell.name = (f"LS_Array_{tone}_{size}umSize_{pitch_type}_{angle}degrees")
    
    TopCell.prune_cell()

    #Export GDS
    #layout.write("LS_Tester.gds")

    return output_cell

def contact_cell(tone:str="D",size:float=0.100,pitch:float=0.100,cell_size:float=25,angle:float=60,x2y:float=2,metro_structure:bool = True):

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

    #Check pitch of the contact array
    pitch_check = size/pitch
    iso = pitch_check < 0.1 #boolean
    donut = pitch_check > 0.75 #also boolean

    #Determine X and Y pitches, based on x2y value (applies to X-pitch only, Y-pitch is untouched)
    xPitch = (size*x2y) + (pitch-size)
    yPitch = pitch
    xSize = (size*x2y)
    ySize = size

    #Determine naming
    if iso:
        pitch_type = 'iso'
    elif donut:
        pitch_type = 'donut'
    else:
        pitch_type = f"{pitch}umPitch"

    #Convert angle from degrees to radians
    rad_angle = angle * (math.pi)/(180)


#### Cell creation and shape assignment ####

    #Create the topcell and subsidiary cells
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

    #Creates formatting regions for later use
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)
    BigBox = db.DBox(-cell_size*1000,-cell_size*1000,cell_size*1000,cell_size*1000)
    BigBox_region = db.Region(BigBox)
    LittleDonut = db.DBox(-1500*(xSize),-1500*(ySize),1500*(xSize),1500*(ySize))
    LittleDonut_region = db.Region(LittleDonut)
    DonutBox = BigBox_region-LittleDonut_region
    DonutBox.break_(4,1)
    DenseCont = db.DBox(-1000*xPitch/2,-1000*yPitch/2,1000*xPitch/2,1000*yPitch/2)
    DenseCont_region = db.Region(DenseCont)


#### Generate the Cell ####

    if iso:
        #Checks tone and adjusts if needed, then instances a single cell into the TopCell
        if tone == "C":
            iso_region = db.Region(ContCell.shapes(l_cont))
            clear_iso = BigBox_region-iso_region
            clear_iso.break_(4,1)
            ContCell.clear_shapes()
            ContCell.shapes(l_cont).insert(clear_iso)       
        cont_iso = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_iso)

    elif donut:
        #Create the DonutCell
        DonutCell = layout.create_cell(f"{size}um_donut_structure")
        DonutCell.shapes(l_cont).insert(DonutBox)
        
        #Checks tone and adjusts if needed
        if tone == "C":
            donut_region = db.Region(ContCell.shapes(l_cont))
            little_donut = donut_region ^ LittleDonut_region
            ContCell.clear_shapes()
            ContCell.shapes(l_cont).insert(little_donut)
            DonutCell.clear_shapes()
        
        #Add all into the TopCell
        cont_donut_center = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_donut_center)    
        cont_donut_ring = db.DCellInstArray(DonutCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(cont_donut_ring)

    else:
        #Checks tone and adjusts if needed
        if tone == "C":
            dense_region = db.Region(ContCell.shapes(l_cont))
            clear_dense = dense_region ^ DenseCont_region
            clear_dense.break_(4,1)
            ContCell.clear_shapes()
            ContCell.shapes(l_cont).insert(clear_dense)
        
        #Instances the contact cell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
        #NOTE: This "functions" in its current form, but needs further adjusting, especially for holes, to get a good array of angled contacts
        
        if angle <= 90:
            x_origin = -cell_size+cell_size*2*math.sin(rad_angle)*math.cos(rad_angle)
            y_origin = -cell_size-cell_size*math.sin(rad_angle)*math.cos(rad_angle)
        elif angle <=180:
            x_origin = cell_size-cell_size*math.sin(rad_angle)*math.cos(rad_angle)
            y_origin = -cell_size-cell_size*2*math.cos(rad_angle)*math.sin(rad_angle)
        else:
            return ValueError("Choose an angle between 0 and 180")
        cont_array = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,x_origin,y_origin),
                        db.DVector(xPitch*math.cos(rad_angle),xPitch*math.sin(rad_angle)),db.DVector(-yPitch*math.sin(rad_angle),yPitch*math.cos(rad_angle)),
                        2*math.ceil(cell_size/xPitch),2*math.ceil(cell_size/yPitch))
        TopCell.insert(cont_array)


#### Add metro structures if applicable ####
    metro_spacing = 8 #um

    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        if iso:
             MetroShape = db.DPolygon([db.DPoint(-0.5,0),db.DPoint(0,0.5),db.DPoint(0.5,0),db.DPoint(0,-0.5)])
             MetroCell.shapes(l_cont).insert(MetroShape)
             metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,metro_spacing*math.sin(rad_angle),-metro_spacing*math.cos(rad_angle)),db.DVector(-2*metro_spacing*math.sin(rad_angle),2*metro_spacing*math.cos(rad_angle)),db.DVector(0,0),2,0)

             if tone == "C":
                  MetroShape1 = (db.DPolygon([db.DPoint(-500,metro_spacing*1000),db.DPoint(0,500+metro_spacing*1000),db.DPoint(500,metro_spacing*1000),db.DPoint(0,1000*metro_spacing-500)]))
                  MetroShape2 = (db.DPolygon([db.DPoint(-500,-metro_spacing*1000),db.DPoint(0,500-metro_spacing*1000),db.DPoint(500,-metro_spacing*1000),db.DPoint(0,-1000*metro_spacing-500)]))
                  MShape1_Reg = db.Region(MetroShape1)
                  MShape2_Reg = db.Region(MetroShape2)
                  clear_iso = BigBox_region-iso_region
                  new_clear_cont_temp = clear_iso - MShape1_Reg
                  new_clear_cont = new_clear_cont_temp-MShape2_Reg
                  new_clear_cont.break_(5,2)
                  MetroCell.prune_cell()
                  ContCell.shapes(l_cont).clear()
                  ContCell.shapes(l_cont).insert(new_clear_cont)
             else:
                 TopCell.insert(metro_insert)

        
        elif not donut:
             if angle>0:
                 print("No metro structure for angled contact array at this time")
             else:
                if tone == "D":
                    Dense_Metro = 1000*db.DBox((-2*xPitch)+xSize/2,(-2*yPitch)-size/2,(-xPitch)-xSize/2,(-2*yPitch)+size/2)
                    Dense_Metro_Region = db.Region(Dense_Metro)
                    TopCell.shapes(l_cont).insert(Dense_Metro_Region)
                else:
                    Dense_Metro = 1000*db.DBox((-2*xPitch)-xSize/2,(-2*yPitch)-size/2,(-2*xPitch)+xSize/2,(-2*yPitch)+size/2)
                    Dense_Metro_Region = db.Region(Dense_Metro)
                    TopCell.shapes(l_cont).insert(Dense_Metro_Region)


             MetroCell.prune_cell()




#### Angle transformations, sliver removal, and output ####


    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,-angle,False,0,0)
    [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-size/2,-size/2,size/2,size/2)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(l_cont).width()<size_check.bbox().width() or layout.cell(j).dbbox(l_cont).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"Cont_Array_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees_w_metro")
    else:
        output_cell.name = (f"Cont_Array_{tone}_{size}umSize_{pitch_type}_{x2y}to1_x2y_{angle}degrees")
    
    TopCell.prune_cell()

    #Export GDS
    #layout.write("Cont_Tester.gds")

    return output_cell

def SRAF_cell(tone:str="C",size:float=0.300,pitch:float=8.500,cell_size:float=25,angle:float=45,sraf_size:float=0.05,sraf_step:float=0.2,sraf_num:int=4,metro_structure:bool = True):

#NOTE:Angle support only for iso structure, No Metro structures needed

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
    BigBox = db.DBox(-cell_size,-cell_size,cell_size,cell_size)


#### Generate the Cell ####

    #Create sraf sub-instances
    if sraf_num>1:
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

        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell       
        if tone == "C":
            LineCell.flatten(-1,True)
            iso_region = db.Region(LineCell.shapes(l_line))
            clear_iso = db.Region(1000*BigBox) - iso_region
            clear_iso.break_(4,1)
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_iso)       
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)

    else:
        #Create array
        LineArray1 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)
        LineArray2 = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector(-pitch,0),db.DVector(0,0),math.ceil(num_lines/2),0)

        TopCell.insert(LineArray1)
        TopCell.insert(LineArray2)
        
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            TopCell.flatten(-1,True)
            dense_region = db.Region(TopCell.shapes(l_line))
            clear_dense = db.Region(CellBox*1000) - dense_region
            clear_dense.break_(4,1)
            TopCell.clear_shapes()
            TopCell.shapes(l_line).insert(clear_dense)


#No metro structure for this feature type


#### Angle transformations, sliver removal, and output ####
    
    if iso:
        #Apply angle rotation for all cells
        t = db.ICplxTrans(1,angle,0,0,0)
        [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    output_cell.name = (f"Line_w_SRAF_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{sraf_num}SRAFs_{sraf_size}um_size_{sraf_step}um_apart")
    
    TopCell.prune_cell()

    #Export GDS
    #layout.write("SRAF_Tester.gds")

    return output_cell

def LEnd_cell(tone:str="C",size:float=0.500,pitch:float=0.600,cell_size:float=25,angle:float=40,end_spacing:float=0.2,metro_structure:bool = True):

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
    l_line = layout.layer(1,0) #line layer

    #Check pitch of the LS array
    pitch_check = size/pitch
    iso = pitch_check < 0.1 #boolean
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
    BigBox = db.DBox(-cell_size*1000,-cell_size*1000,cell_size*1000,cell_size*1000)
    BigBox_region = db.Region(BigBox)
    DenseLine = db.DBox(-1000*pitch/2,-1000*cell_size,1000*pitch/2,1000*cell_size)
    DenseLine_region = db.Region(DenseLine)


#### Generate the Cell ####

    if iso:
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            iso_region = db.Region(LineCell.shapes(l_line))
            clear_iso = iso_region ^ BigBox_region
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_iso)       
        ls_iso = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0))
        TopCell.insert(ls_iso)


    else:
        #Checks tone and adjusts if needed, then instances a single LineCell into the TopCell
        if tone == "C":
            dense_region = db.Region(LineCell.shapes(l_line))
            clear_dense = dense_region ^ DenseLine_region
            LineCell.clear_shapes()
            LineCell.shapes(l_line).insert(clear_dense)
        
        #Instance a left and right array of the LineCell to span the TopCell region. Trigonometry used to calculate step sizes to preserve pitch for angled arrays.
        ls_array_right = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((pitch*math.cos(rad_angle)),-pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        ls_array_left = db.DCellInstArray(LineCell,db.DTrans(db.DTrans.M0,0,0),db.DVector((-pitch*math.cos(rad_angle)),pitch*math.sin(rad_angle)),db.DVector(0,0),math.ceil(cell_size/pitch),0)
        TopCell.insert(ls_array_right)
        TopCell.insert(ls_array_left)


#### Add metro structures if applicable ####
    metro_spacing = 8 #um

    if metro_structure:
        MetroCell = layout.create_cell(f"{size}um_line_metro_structure")
        MetroShape = db.DBox(-size/2,-size/2,size/2,size/2)
        MetroCell.shapes(l_line).insert(MetroShape)

        if tone == "C":
             metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,-metro_spacing*math.sin(rad_angle),-metro_spacing*math.cos(rad_angle)),db.DVector(2*metro_spacing*math.sin(rad_angle),2*metro_spacing*math.cos(rad_angle)),db.DVector(0,0),2,0)
        else:
             sqrt_calc = math.sqrt(((size)**2)+(metro_spacing**2))
             extra_angle = -size/metro_spacing
             metro_insert = db.DCellInstArray(MetroCell,db.DTrans(db.DTrans.M0,sqrt_calc*math.sin(rad_angle+extra_angle),sqrt_calc*math.cos(rad_angle+extra_angle)),db.DVector(-2*metro_spacing*math.sin(rad_angle),-2*metro_spacing*math.cos(rad_angle)),db.DVector(2*size*math.cos(rad_angle),-2*size*math.sin(rad_angle)),2,2)

        TopCell.insert(metro_insert)


#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    [layout.cell(i).transform(t) for i in TopCell.each_child_cell()]

    #Clip a new cell that covers just the extents of the defined cell size, and eliminate subcells that contain slivers
    output_cell = layout.clip(TopCell,CellBox)
    listicle = []
    size_check = db.DBox(-size/2,-size/2,size/2,size/2)
    [listicle.append(j) for j in output_cell.each_child_cell() if layout.cell(j).dbbox(l_line).width()<size_check.bbox().width() or layout.cell(j).dbbox(l_line).height()<size_check.bbox().height()]
    [layout.cell(k).prune_cell() for k in listicle]

    #Rename new cell, prune old cell
    if metro_structure:
        output_cell.name = (f"LEnd_Array_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{end_spacing}um_spacing_w_metro")
    else:
        output_cell.name = (f"LEnd_Array_{tone}_{size}umSize_{pitch_type}_{angle}degrees_{end_spacing}um_spacing")
    
    TopCell.prune_cell()

    #Export GDS
    #layout.write("LEnd_Tester.gds")

    return output_cell

def Spiral_cell(tone:str="C",size:float=0.2,inner_r:float=1,outer_r:float=12,spacing:float=0.2,cell_size:float=25,rampancy:bool=False):
    
    #Credit to (https://www.youtube.com/watch?v=2e6DuFj0Xws), approached it from creating a PCell in KLayout for this shape,
    #but I followed the general framework turn this into a function that outputs a spiral cell.

#### Setup ####

    #Initial tone and dimension checks
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")
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

    #layout.write("Sprial_tester.gds")

    return SpiralCell

def Horn_cell(tone:str="C",initial_size:float=0.2,step_size:float=0.01,power:float=1,spacing:float=1,cell_size:float=25,angle:float=45):
    
#### Setup ####

    #Initial tone and dimension checks
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    
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


    #layout.write("Horn_tester.gds")

    return HornCell


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
    if defect_num >5 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Feature, 2-Half Missing Feature, 3-Small Extension, 4-Corner Extension, 5-Bridged Feature")

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
    LL_point = math.ceil(((cell_size-2*spacing)/2)/pitch)*-pitch


#### Generate the Cell ####
        
    cont_array = db.DCellInstArray(ContCell,db.DTrans(db.DTrans.M0,LL_point,LL_point),
                 db.DVector(pitch,0),db.DVector(0,pitch), 2*math.ceil((cell_size-2*spacing)/pitch),2*math.ceil((cell_size-2*spacing)/pitch))
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

    #Flip the tone if needed
    if tone == "C":
         Cell_shapes = db.Region(TopCell.shapes(l_cont))
         Clear_region = CellRegion - Cell_shapes
         TopCell.shapes(l_cont).clear()
         TopCell.shapes(l_cont).insert(Clear_region)

    
    TopCell.name = (f"Cont_Array_{tone}_{size}umSize_{pitch}pitch_w_{defecttype}")

    #Export GDS
    #layout.write("Cont_PDM.gds")

    return TopCell

def LS_PDM(tone:str="D",size:float=0.260,pitch:float=0.520,cell_size:float=20,horiz:bool=False,defect_num:int=5,spacing:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >5 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Line, 2-Half Missing Feature, 3-Small Extension, 4-Bridged Line, 5-Combination Defect")

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
    else: defecttype="Control"

    if horiz:
        angle=0
    else:
        angle=90

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
    l_bottom = -(cell_size-2*spacing)/2
    l_top = (cell_size-2*spacing)/2

    #Create the main feature shape and insert it into the LineCell cell
    LineCell.shapes(l_line).insert(db.DBox(l_left, l_bottom, l_right, l_top))

    #Creates formatting regions
    CellBox = db.DBox((-cell_size/2),-cell_size/2,(cell_size/2),cell_size/2)

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


#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    TopCell.transform(t)


    TopCell.name = (f"LS_Array_{tone}_{size}umSize_{angle}degrees_w_{defecttype}")
    
    #Export GDS
    #layout.write("LS_PDM.gds")

    return TopCell

def SRAF_PDM(tone:str="D",size:float=0.260,pitch:float=1.880,cell_size:float=20,horiz:bool=False,sraf_size:float=0.050,sraf_step:float=0.26,sraf_num:int=2,defect_num:int=5,spacing:float=1):

#### Setup ####

    #Initial tone check
    if tone == "D":
            tone = "D"
    elif tone == "C":
            tone = "C"
    else: return TypeError("Error: Tone must be (D)ark or (C)lear)")

    #Defect number check
    if defect_num >5 or defect_num<0:
        return TypeError(f"Error: Choose an appropriate defect number:0-Control Cell, 1-Missing Line, 2-Half Missing Feature, 3-Small Extension, 4-Bridged Line, 5-Combination Defect")

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
    l_bottom = -(cell_size-2*spacing)/2
    l_top = (cell_size-2*spacing)/2

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

#### Angle transformations, sliver removal, and output ####
    
    #Apply angle rotation for all cells
    t = db.ICplxTrans(1,angle,0,0,0)
    TopCell.transform(t)

    TopCell.name = (f"Line_w_SRAF_{tone}_{size}umSize_{angle}degrees_{sraf_num}SRAFs_{sraf_size}um_size_w_{defecttype}")

    #Export GDS
    #layout.write("SRAF_PDM.gds")

    return TopCell

def FullField_PDM(tone:str="C",size:float=0.520,cell_size:float=20,defect_num:int=2,spacing:float=1):

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
    while current_size > 0.06:
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

    TopCell.name = (f"FullField_{tone}_{size}umSize_w_{defecttype}")

    #Export GDS
    #layout.write("FullField_PDM.gds")

    return TopCell
