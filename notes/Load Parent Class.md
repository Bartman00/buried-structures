# Load Parent Class

## Inputs they all share

1. center: Point_3D. Center of the load. For infit
2. magnitude: float. Units may vary

## Class level variables

1. load_type: str. Name of the load type

## Methods they all share

### Stresses

1. stress_x
2. stress_y
3. stress_z
4. displacement_x
5. displacement_y
6. displacement_z

These and any other stress functions will always take in a point. They may require additional inputs, if a load class doesn't have one for some reason, it must be defined and raise a NotImplementedError.

OR???? Should I have a single stress function and include a direction as an input? This would allow for more flexibilitiy and less functions. Things like radial stress could be quickly included only when needed. The stress and displacement functions would mostly be a dictionary pointing to other functions or raises a NotImplemented error if isn't found.

### Descriptions & Strings

1. reference. Where did it come from?
2. description. Written out description explaining what this represents, additional inputs, any extra functions that the parent class doesn't have.
3. markdown. Markdown description with all formulas written out with latex formulas. Try to generate diagrams using html with svg as well.

## Dunder

1. __eq__ Includes a type 
2. __init__ Include NotImplemented for the parent class.
3. __str__ Printout of description with applicable inputs.

## Example from Boussinesq Problem

center = coordinates of the load. Raises an error if z != 0.
magnitude = Concentrated load magnitude. Raises an error if P <= 0
poisson = Poisson's ratio. Default to 0.50 (conservative for most applications).

Cylindrical stresses are defined in P&D so x & y would use some trigonometry to convert back to cartesian.

Would include stress outputs for the r and theta directions.

reference: "Poulose and Davis, ...., Section 2.1"

description: "Vertical load where positive is downward at a point. Poisson's ratio used for horizontal loads. Includes radial and tangental load outputs and radial displacement in cylindrical coordinates."

markdown: "## Boussinesq problem

svg of coordinate system

latex of stress and displacement equations

Stresses in the x & y direction are calculated by converting from the cylindrical coordinates defined in P&D

latex of stress_x, stress_y"

## Naming Convention for Children

Options:

1. Name after title in P&D
2. Name after description. Too long.
