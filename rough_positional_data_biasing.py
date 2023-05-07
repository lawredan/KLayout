#Import the needed modules
import klayout as kl
import klayout.db as db
import pya
import pandas as pd

#Define the function
def rpdb(gds_file:str = 'Poly_tester.gds', mesh:str = 'Test_Mesh.csv', target_layer:int = 0, LL:list=(-5,-10), UR:list=(388,323),output_file:str = 'Test RDP.gds'):
    #gds is the input gds, and mesh is the matrix of data biasing to be applied, target_layer is the specific layer to be biased
    #LL is the lower left corner of the layer to be edited that contains structures, UR is the upper right corner (in um)
    #Will hardcode these for now for testing purposes

    #Import the .gds
    gds = pya.Layout()
    gds.read(gds_file)
    
    #Sets the database units as 1nm
    gds.dbu = 0.001

    #Hard coding layer levels (this can be improved in the future...)
    copy_lyr_index = 41
    bias_lyr_index = 42
    final_lyr_index = 43

    #Create copy layer, copy structures over from the desired layer for biasing.
    #This copy layer will be mauled by the bias layer so that the original target layer is untouched.
    copy_lyr = gds.layer(copy_lyr_index,0,'Copy Layer')
    gds.copy_layer(target_layer,copy_lyr)

    #Create bias layer for eventual use
    bias_lyr = gds.layer(bias_lyr_index,0,'Initial Biasing Layer')

    #Create final bias layer
    final_lyr = gds.layer(final_lyr_index,0,'Final Biased Layer')

    #Import the mesh
    pdb = pd.read_csv(mesh, index_col=0)
    
    #Determine mesh columns
    col_len = len(pdb.columns)+1
    columns = range(1,col_len)

    #Determine mesh rows
    row_len = len(pdb)+1
    rows = range(1,row_len)

    #Determine layer sizing
    x_size = UR[0] - LL[0]
    y_size = UR[1] - LL[1]

    #Define size of meshing
    mesh_x = x_size / (len(columns))
    mesh_y = y_size / (len(rows))

    #Calls the top cell (assumes(!) there is one top cell and it contains all the constituent cells)
    top_cell = gds.top_cell()

    #Loop across the mesh, define the regions in the copy layer to copy into the bias layer, then resize the features in the bias layer based on the mesh input
    for i in rows:
        for j in columns:
                #Define the edges of the mesh at each location
                l_edge = LL[0]+mesh_x*(j-1)
                b_edge = UR[1]-mesh_y*i
                r_edge = LL[0]+mesh_x*j
                t_edge = UR[1]-mesh_y*(i-1)

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
                

                print(f"Finished row {i} and column {j}")
    
    #Merges any overlapping polygons and places the final biased data onto the "final" layer
    bias_merge = pya.Region(top_cell.begin_shapes_rec_touching(bias_lyr,pya.DBox(LL[0],LL[1],UR[0],UR[1])))
    bias_merge.merge()
    top_cell.shapes(final_lyr).insert(bias_merge)


    return gds.write(output_file)

rpdb()