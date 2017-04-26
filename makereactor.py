import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
from reactor_oop import ReactorComponents
components = ReactorComponents()
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")
import math
pi = math.pi;

componentsdict = { 
					'tank' : components.MakeTank, 
					'inlet' : components.MakeInlet,
					'rci_rectangle' : components.MakeRCIRectangle, 
					'rci_circular' : components.MakeRCICircular, 
					'anchor_rectangle' : components.MakeAnchorRectangle, 
					'anchor_circular' : components.MakeAnchorCircular, 
					'pbt' : components.MakePBT,
					'rushton' : components.MakeRushton,
					'smith' : components.MakeSmith,
					'hydrofoil' : components.MakeHydrofoil,
					'propeller' : components.MakePropeller
}


#rci = chemglass.MakeAnchorRectangle(0.024, 0.0065, 0.002, 0.06)
#rci = chemglass.MakePBT(6, 0.05, 0.02, 0.002, 45)
#rci = chemglass.MakeRushton(6, 0.1, 0.06, 0.004, 0.05, 0.002, 0.02)
#rci = chemglass.MakeSmith(8, 0.1, 0.06, 0.004, 0.05, 0.02, 0.002)
rci = components.MakePropeller(3, 1, 0.02, 0.333)


id_tank = geompy.addToStudy(rci,"Tank")
gg.createAndDisplayGO(id_tank)

