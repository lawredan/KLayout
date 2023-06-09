import klayout.db as db
import math
import kl_feature_functions as kl

layout = db.Layout()
layout.dbu=0.001 #um

TopCell = layout.create_cell("TopCell")
c1 = kl.LS_cell("D",0.1,0.5,25,0,1,True)
c2 = kl.LS_cell("C",0.1,0.5,25,0,1,True)

c1_inst = db.DCellInstArray(c1,db.DVector(0,0))
c2_inst = db.DCellInstArray(c2,db.DVector(0,50))

TopCell.insert(c1_inst)
TopCell.insert(c2_inst)

layout.write("Wrapper.gds")