# KLayout
Photomask SPC design

## SPC Toolbox

### Objective
Design a program to generate control structures for photomask SPC.
Provide cell structures that can be arrayed for linearity, through pitch, and other monitoring strategies (create PCells for these)
Provide framework for generating SPC cell based on user input
Uses KLayout to output a .gds file for use

### Design

GUI (not implemented)
|
v
User inputs (not implemented)
|
v
Wrapper script  -----> .gds output
|           ^
v           |
Control structures

#### Control structures
Create functions to generate the following feature types.
Returns structure(s) back to the wrapper script to be placed in layout.

Note: Metro mark(s) (Y/N) to be available for all features --> Done
Note: Will have option (Y/N) for printed text adjacent to cell/array describing cell structure --> not implemented
Note: PEC window information will be passed from the wrapper script, to define the overall size of these cells --> not implemented
Note: Will have option (Y/N) for MFX generation --> done in wrapper script

- Line/space
    - Orientation (H/V)
    - Tone (C/D)
    - Feature size
    - Pitch (iso, variable pitches, 3-bar)
    - Angle
- Hole/dot
    - Orientation (H/V)
    - Tone (C/D)
    - Feature size
    - Pitch (iso, variable pitches, donut)
    - Array (ortho, staggered)
    - Aspect Ratio (1:1, 1:2, 1:3)
- Line/space w/ scatter bars
    - Orientation (H/V)
    - Tone (C/D)
    - Feature size
    - Angle
    - number of scatter bars
    - scatter bar placement
    - scatter bar size
- Hole/dot w/ assist features
    - Orientation (H/V)
    - Tone (C/D)
    - Feature size
    - aspect ratio (1:1, 1:2, 1:3)
    - number of h/d assists
    - h/d assist placement
    - h/d assist size
    - number of l/s assists
    - l/s assist placement
    - l/s assist size
- Curvilinear spiral
    - Tone (C/D)
    - Feature size
    - Pitch
- Line ends
    - Orientation (H/V)
    - Tone (C/D)
    - Feature size
    - L/S pitch
    - Line end separation
- Polygons (Corner rounding) --> not implemented
    - Tone (C/D)
    - Feature size
    - Pitch (iso outline, 1:1, full)
    - Verticies (3 to 12)
- Polygon array --> not implemented
    - Tone (C/D)
    - Feature size
    - Pitch
    - Verticies (3 to 12)

#### Wrapper Script
This will...
- Pull from user inputs (including PEC window to define the size of each cell)
- Pass inputs to cell functions, which return cell geometries
- Place cells in a defined array
- Output .gds file

Inputs are:
- SPC Area
- PEC window --> not implemented
- Edge margins
- Cell margins (if applicable)
- Cell requests (to pass to control structures functions)
- Cell placement(s)

#### User inputs
Inputs are...
- Wrapper script inputs in list format


## Positional Data Biasing (PDB)

### Objective
Create a function that can be fed a mesh with data bias values, and then apply those biasing values to the structures within each mesh cell throughout a given design.
