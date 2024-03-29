#Import the needed modules
import klayout as kl
import klayout.db as db
import pya
import pandas as pd
from tqdm import tqdm #For timing execution of the loop
import math as math

#Define the function
def rough_positional_data_biasing(bias_file:str='NCAR_Universal_SPC_EBeam_Full.oas', mesh:str='Test_Mesh.csv', target_layer:int=1,output_file:str='Test RDP.oas'):
    #bias_file is the input gds, and mesh is the matrix of data biasing to be applied, target_layer is the specific layer to be biased
    #LL is the lower left corner of the layer to be edited that contains structures, UR is the upper right corner (in um)
    #Will hardcode these for now for testing purposes

    #Import the .gds
    layout = pya.Layout()
    layout.read(bias_file)
    
    #Sets the database units as 1nm
    layout.dbu = 0.001

    #Hard coding layer levels (this can be improved in the future...)
    copy_lyr_index = 41
    bias_lyr_index = 42
    final_lyr_index = 43

    #Create copy layer, copy structures over from the desired layer for biasing.
    #This copy layer will be mauled by the bias layer so that the original target layer is untouched.
    copy_lyr = layout.layer(copy_lyr_index,0,'Copy Layer ')
    layout.copy_layer(target_layer,copy_lyr)

    #Create bias layer for eventual use
    bias_lyr = layout.layer(bias_lyr_index,0,'Initial Biasing Layer ')

    #Create final bias layer
    final_lyr = layout.layer(final_lyr_index,0,'Final Biased Layer ')

    #Import the mesh
    pdb = pd.read_csv(mesh, index_col=0)
    
    #Determine mesh columns
    col_len = len(pdb.columns)+1
    columns = range(1,col_len)

    #Determine mesh rows
    row_len = len(pdb)+1
    rows = range(1,row_len)

    #Define layer extents
    target_layer_extents = layout.top_cell().dbbox_per_layer(target_layer)

    #Determine layer sizing
    x_size = target_layer_extents.width()
    y_size = target_layer_extents.height()

    #Define size of meshing
    mesh_x = x_size / (len(columns))
    mesh_y = y_size / (len(rows))

    #Calls the top cell (assumes(!) there is one top cell and it contains all the constituent cells)
    top_cell = layout.top_cell()

    #Loop across the mesh, define the regions in the copy layer to copy into the bias layer, then resize the features in the bias layer based on the mesh input
    for i in tqdm(rows):
        for j in tqdm(columns):
                #Define the edges of the mesh at each location
                l_edge = target_layer_extents.left+mesh_x*(j-1)
                b_edge = target_layer_extents.top-mesh_y*i
                r_edge = target_layer_extents.left+mesh_x*j
                t_edge = target_layer_extents.top-mesh_y*(i-1)

                #Define the biasing at each location
                new_j = str(j)
                biasing = pdb[new_j][i]

                #Takes polygons from the copy layer in a given search region to keep in the "touching" pya.Region 
                search_region = pya.DBox(l_edge,b_edge,r_edge,t_edge)
                touching = pya.Region(top_cell.begin_shapes_rec_touching(copy_lyr, search_region))
                top_cell.shapes(copy_lyr).insert(touching)

                #Biases "touching" and copies it into the top cell in the bias layer
                touch_up = touching.sized(int(biasing))
                top_cell.shapes(bias_lyr).insert(touch_up)
                
    
    #Merges any overlapping polygons and places the final biased data onto the "final" layer
    bias_merge = pya.Region(top_cell.begin_shapes_rec_touching(bias_lyr,target_layer_extents))
    bias_merge.merge()
    top_cell.shapes(final_lyr).insert(bias_merge)


    return layout.write(output_file)


def rpdb(mode:str="rpdb",bias_type:str="flatten",bias_file:str='NCAR_Universal_SPC_EBeam_Full.oas',correction_file:str='Test_Mesh.csv',target_layer:int=1,
         coarse_mesh:float=30,fine_mesh:float=15,output_file:str='TesterRDP.oas'):
    """
    Biases the features in a layout positionally, either by global position on the mask, or by local density.

    @mode = Whether biasing by position (rpdb) or by proximity (PECdb).
    @bias_type = How the bias is applied; "flatten" for non-hierarcical, "clip" for preserving local hierarchies.
    @bias_file = The file to be biased.
    @correction_file = The file detailing the conditions of the biasing. A mesh file should be used for "rpdb", a density to bias list for "PECdb".
    @target_layer = The layer from the bias_file to be biased; use -1 to apply to all layers.
    @output_file = The name of the file used to write the biased layout.
    """

    #Import the .gds
    layout = db.Layout()
    layout.read(bias_file)
    print(f'File read: {bias_file}')

    #Sets the database units as 1nm
    layout.dbu = 0.001
    
    #Create bias layer for eventual use
    bias_lyr = layout.layer('Initial Biasing Layer')

    #Calls the top cell (assumes(!) there is one top cell and it contains all the constituent cells) and stores index of all called cells
    top_cell = layout.top_cell()
    top_cell_index = top_cell.cell_index()
    called_cells = top_cell.called_cells()
    
    #Determines layout size
    layout_bounding = top_cell.dbbox()
    left = layout_bounding.left
    bottom = layout_bounding.bottom
    right = layout_bounding.right
    top = layout_bounding.top
    width = right-left
    height = top-bottom

    print(f'{left},{bottom},{right},{top}')
    
    #Determine layer sizing
    x_size = right - left
    y_size = top - bottom

    #Create new top cell
    New_Top = layout.create_cell("NewTop")
    New_Top_Index = New_Top.cell_index()

    if mode=="rpdb":
        #Import the mesh
        pdb = pd.read_csv(correction_file, index_col=0)
        print(f'Mesh read: {correction_file}')

        #Determine maximum absolute bias applied, in order to size up the cell regions
        mesh_max = pdb.max().max()
        mesh_min = pdb.min().min()
        if abs(mesh_max) >= abs(mesh_min):
             bias_max = mesh_max/1000 #to get in units of um
        else:
             bias_max = abs(mesh_min) #to get in units of um

        #Determine mesh columns
        col_len = len(pdb.columns)+1
        columns = range(1,col_len)
        print(f'There are {col_len} columns in the mesh')

        #Determine mesh rows
        row_len = len(pdb)+1
        rows = range(1,row_len)
        print(f'There are {row_len} rows in the mesh')
    
        #Define size of meshing
        mesh_x = x_size / (len(columns))
        mesh_y = y_size / (len(rows))
        print(f'Mesh X is {mesh_x}um')
        print(f'Mesh Y is {mesh_y}um')


        #Loop across the mesh, define the regions in the copy layer to copy into the bias layer, then resize the features in the bias layer based on the mesh input
        for i in tqdm(rows):
            for j in columns:
                #Define the edges of the mesh at each location
                l_edge = left+(mesh_x*(j-1)-bias_max)
                b_edge = top-(mesh_y*i+bias_max)
                r_edge = left+(mesh_x*j+bias_max)
                t_edge = top-(mesh_y*(i-1)-bias_max)

                #Define the biasing at each location
                new_j = str(j)
                biasing = pdb[new_j][i]
                #print(f'This is the bias value: {biasing}')


                #Clips mesh area from the polygon, preserving hierarchy, and names it
                clip = layout.clip(top_cell,db.DBox(l_edge,b_edge,r_edge,t_edge))
                clip.name= f'Mesh_Cell_{i}_{j}'
                
                if bias_type=="clip":                
                    #Copies the cell tree from the clip into a new bias cell
                    bias_cell = layout.create_cell(f'bias_cell_{i}_{j}')
                    bias_tree = bias_cell.copy_tree(clip)

                    #Goes through the hierarchy of each clip and biases by the appropriate value, and inserts into the bias layer
                    for k in bias_cell.called_cells():
                        copy_cell = layout.cell(k)
                        search_region = db.Region(copy_cell.bbox(target_layer))
                        shapes_region = db.Region(copy_cell.shapes(target_layer))
                        touching = search_region & shapes_region
                        bias_apply = touching.sized(int(biasing))
                        copy_cell.shapes(bias_lyr).insert(bias_apply)
                    
                    #Insert the new bias tree into the New Top Cell, and prune the clip and bias cell                                                                
                    New_Top.copy_tree(bias_cell)
                    bias_cell.prune_cell()
                    clip.prune_cell()   

                elif bias_type=="flatten":
                    clip.flatten(-1,True)
                    clip_region = db.Region(clip.shapes(target_layer))
                    bias_clip_region=clip_region.sized(int(biasing))
                    New_Top.shapes(bias_lyr).insert(bias_clip_region)
                    clip.prune_cell()

        print("Finished Mesh Loop")

    if mode=="PECdb":
         
         #Calculate the mesh values and placement
         x_mesh_count = math.ceil(width/fine_mesh)
         mesh_width = x_mesh_count*fine_mesh
         width_delta = mesh_width-width
         new_left = left-(width_delta/2)
         new_right = right+(width_delta/2)

         y_mesh_count = math.ceil(height/fine_mesh)
         mesh_height = y_mesh_count*fine_mesh
         height_delta = mesh_height-height
         new_top = top+(height_delta/2)
         new_bottom = bottom-(height_delta/2)

         #Define locations for density calculations
         initial_center_x = new_left + fine_mesh/2
         initial_center_y = new_top - fine_mesh/2
         mesh_coords = []

         print(f'X count = {x_mesh_count}; Y count = {y_mesh_count}')

         for i in range(0,x_mesh_count-1):
              for j in range(0,y_mesh_count-1):
                   mesh_coords.append([initial_center_x+fine_mesh*i,initial_center_y-fine_mesh*j])
        
         #Define mesh regions
         fine_mesh_box = db.DBox(-fine_mesh/2,-fine_mesh/2,fine_mesh/2,fine_mesh/2)
         fine_mesh_region = db.Region(fine_mesh_box)
         coarse_mesh_box = db.DBox(-coarse_mesh/2,-coarse_mesh/2,coarse_mesh/2,coarse_mesh/2)
         coarse_mesh_region = db.Region(coarse_mesh_box)

         #need to use polygons to get actual area


    #Remove the old top cell
    top_cell.prune_cell()

    #Writes the new file
    print("Writing file...")
    return layout.write(output_file)

#rough_positional_data_biasing()
rpdb("PECdb")