#Import Needed Extensions
import klayout.db as db
import klayout.lib as lib

##########################################################

#Define parameters

line_width = 5 #um
notch_length = 50 #um
notch_width = 5 #um
notch_step_size = 50 #um
notch_number = 100
line_length = notch_step_size*(notch_number+1) #Line length defined by number of notches and the defined step size
text_offset = 60 #um
notch_half_width = notch_width/2
notch_half_length = notch_length/2

##########################################################

# Create layout for use
layout=db.Layout()
layout.dbu=0.001 #um, database units
TopCell = layout.create_cell("TopCell")

#Define layers
l_line=layout.layer(1,0)
l_notch=layout.layer(2,0)
l_numbers=layout.layer(3,0)

#Construct ruler line
l_left=0
l_right=line_length-notch_step_size
l_top=line_width/2
l_bottom=-line_width/2
TopCell.shapes(l_line).insert(db.DBox(l_left,l_bottom,l_right,l_top))

#Array notches and text
x = 0
notch_text=0
notch_top=notch_half_length
notch_bottom=-notch_half_length
twister=1

for i in range(notch_number+1):
    #Add text
    num_text = f"{notch_text}"
    parameters = {
        "layer": db.LayerInfo(l_numbers+1,0),
        "text": f"{num_text}",
        "mag": 25.0
        }
    
    TextCell = layout.create_cell("TEXT","Basic",parameters)
    bbox=TextCell.bbox()
    transform1=bbox.right/2
    transform2=bbox.top/2
    TopCell.insert(db.CellInstArray(TextCell.cell_index(),db.DTrans(180,False,1000*(x)-transform1,(twister*(1000*text_offset))-transform2)))

    #Add notch
    notch_left=x-notch_half_width
    notch_right=x+notch_half_width
    TopCell.shapes(l_notch).insert(db.DBox(notch_left,notch_bottom,notch_right,notch_top))

    #Iterate step
    x += notch_step_size
    notch_text += notch_step_size
    twister*=-1


#Write the layout for review
layout.write("Ruler_tester.oas")