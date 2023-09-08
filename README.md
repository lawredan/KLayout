# KLayout
Photomask SPC design

## SPC Toolbox

### Objective
Design a program to generate control structures for photomask SPC.
Provide cell structures that can be arrayed for linearity, through pitch, and other monitoring strategies.
Provide framework for generating SPC cell based on user input.
Uses KLayout to output a .oasis file for use.

### Design

Wrapper script  -----> .oasis output
|           ^
v           |
Array functions
|           ^
v           |
Feature creation functions

#### Control structures
Create functions to generate the following feature types.
Returns structure(s) back to the wrapper script to be placed in layout.

Note: Metro mark(s) (Y/N) to be available for all features --> Implemented
Note: Will have option (Y/N) for printed text adjacent to cell/array describing cell structure --> Implemented
Note: PEC window information will be passed from the wrapper script, to define the overall size of these cells --> Implemented
Note: Will have option (Y/N) for MFX generation --> Done in wrapper script

- Line/space
    - Tone (C/D)
    - Feature size
    - Pitch (iso, variable pitches, 3-bar)
    - Angle
    - Metro structures
- Hole/dot
    - Tone (C/D)
    - Feature size
    - Pitch (iso, variable pitches, donut)
    - Array (ortho, staggered)
    - Aspect Ratio (1:1, 1:2, 1:3)
    - Angle
    - Metro structures
    - Hammer-head OPC
- Line/space w/ scatter bars
    - Tone (C/D)
    - Feature size
    - Angle
    - Number of scatter bars
    - Scatter bar placement
    - Scatter bar size
- Curvilinear
    - Spiral and Horn
    - Tone (C/D)
    - Feature size
    - Angle
    - Degree of curvature
- Line ends
    - Tone (C/D)
    - Feature size
    - L/S pitch
    - Line end separation
    - Angle
- Program Defects
    - Tone (C/D)
    - Defect types
    - Defect sizes

#### Wrapper Script
- Pulls from user inputs
- Pass inputs to cell functions, which returns cell geometries
- Places cells in a defined array
- Output .oasis file

#### User inputs
Inputs are...
- Wrapper script inputs in list format


## Positional Data Biasing (PDB)

### Objective
Create a function that can be fed a mesh with data bias values, and then apply those biasing values to the structures within each mesh cell throughout a given design.
