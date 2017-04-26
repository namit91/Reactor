import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")
import math
pi = math.pi;

	

class ReactorComponents(object):
		
		origin = geompy.MakeVertex(0.  , 0.  , 0.  )
		px = geompy.MakeVertex(100., 0.  , 0.  )
		py = geompy.MakeVertex(0.  , 100., 0.  )
		pz = geompy.MakeVertex(0.  , 0.  , 100.)
		
		def __init__(self):
			self.ShapeTypeFace = geompy.ShapeType["FACE"]
			self.ShapeTypeEdge = geompy.ShapeType["EDGE"]
		
		def __repr__(self):
			return "Class to Make a reactor"
			
		def vec(self,direction):
			dir = geompy.MakeVector(self.origin, direction)
			return dir
		
		def MakeTank(self, r_tank, h_tank, base_type = "ASME"):	
			c_arc = h_tank-2.0*r_tank;
			h_line = math.sqrt(3)*r_tank; 
			if base_type is not "ASME":
				r_fillet = 0.1*2.0*r_tank;
			else: 
				r_fillet = 0.06*2.0*r_tank;
			
			p_line = geompy.MakeVertex( r_tank,   0.,   0.)
			p_intersection = geompy.MakeVertex( r_tank, 0.,   -(c_arc+h_line))
			p_bottom = geompy.MakeVertex(   0., 0.,   -h_tank)
			p_arc_center = geompy.MakeVertex(0., 0., -c_arc)
			line = geompy.MakeLineTwoPnt(p_line,p_intersection) #create line
			arc = geompy.MakeArcCenter(p_arc_center,p_bottom,p_intersection) #create arc
			wire = geompy.MakeWire([line,arc]) #create wire because only wires can be filleted
			fillet_1d = geompy.MakeFillet1D(wire, r_fillet, []) #fillet wire
			tank = geompy.MakeRevolution(fillet_1d, self.vec (self.pz) , 2.0*pi) #create revolution
			return tank, r_tank
		
		def MakeInlet(self, r_inlet):
				inlet = geompy.MakeDiskPntVecR (self.origin, self.vec(slf.pz), r_inlet)
				return inlet
		
		def MakeBladeRotation(self, obj, n_blades):
			rotation = [];
			for i in xrange(n_blades):
				rotation.append(geompy.MakeRotation(obj,self.vec(self.pz),2.*i/n_blades*pi))
			blades = geompy.MakeFuseList(rotation)
			return blades
			
		def MakeStub(self, r_stub, h_stub):
			stub = geompy.MakeCylinder(self.origin, self.vec(self.pz), r_stub, h_stub)
			stub = geompy.TranslateDXDYDZ(stub, 0., 0., -h_stub/2.)
			return stub 
			
		def MakeRCIRectangle(self, n_blades , r_blades, w_blade, h_blade = None, angle_blade = None, blade_fillet = None ):
			
			if h_blade is None:
				h_blade = w_blade
			if angle_blade is None:
				angle_blade = 0
				
			blade_base = geompy.MakeFaceObjHW(self.vec(self.py),h_blade,w_blade) #blade base
			#create extrusion 
			p_arc_center = geompy.MakeVertex(r_blades, 0.  , 0  )
			p_arc_end =geompy.MakeVertex(r_blades/2.0, math.sqrt(3)*r_blades/2.0  , 0 )
			blade_path = geompy.MakeArcCenter(p_arc_center,self.origin,p_arc_end)
			blade = geompy.MakePipe(blade_base,blade_path)
			
			if blade_fillet is not None:
				blade_faces = geompy.SubShapeAll(blade, self.ShapeTypeFace)
				b_ind = geompy.GetSubShapeID(blade, blade_faces[-1])
				blade = geompy.MakeFillet(blade, blade_fillet, self.ShapeTypeFace, [b_ind])
			
			blade_rotate = geompy.MakeRotation(blade, self.vec (self.px), pi/180.0*angle_blade) #rotate blade			
			blades = self.MakeBladeRotation(blade_rotate, n_blades)#create copies and fuse
			shaft = self.MakeStub(0.2*r_blades, 1.5*h_blade)
			rci = geompy.MakeFuseList([blades,shaft])
			return rci
			
		def MakeRCICircular (self, n_blades , r_blades, w_blade, h_blade, angle_blade = None, blade_fillet = None):		
			
			if angle_blade is None:
				angle_blade = 0
			
			p_center_1 = geompy.MakeVertex(0., 0., (h_blade-w_blade)/2.)
			p_center_2 = geompy.MakeVertex(0., 0., -(h_blade-w_blade)/2.)
			blade_rect = geompy.MakeFaceObjHW(self.vec(self.py),h_blade-w_blade,w_blade) #blade base
			blade_circle_1 = geompy.MakeDiskPntVecR(p_center_1, self.vec(self.py), w_blade/2.)
			blade_circle_2 = geompy.MakeDiskPntVecR(self.origin, self.vec(self.py), w_blade/2.)
			blade_circle_3 = geompy.MakeDiskPntVecR(p_center_2, self.vec(self.py), w_blade/2.)
			blade_base = geompy.MakeFuseList([blade_circle_1,blade_circle_2, blade_circle_3],1,1)
			blade_base = geompy.MakeFuseList([blade_base, blade_rect],1,1)
			#create extrusion 
			p_arc_center = geompy.MakeVertex(r_blades, 0., 0.)
			p_arc_end =geompy.MakeVertex(r_blades/2.0, math.sqrt(3)*r_blades/2.0  , 0 )
			blade_path = geompy.MakeArcCenter(p_arc_center,self.origin,p_arc_end)
			blade = geompy.MakePipe(blade_base,blade_path)
			
			if blade_fillet is not None:
				blade_faces = geompy.SubShapeAll(blade, self.ShapeTypeFace)
				b_ind = geompy.GetSubShapeID(blade, blade_faces[-1])
				blade = geompy.MakeFillet(blade, blade_fillet, self.ShapeTypeFace, [b_ind])
			
			blade_rotate = geompy.MakeRotation(blade, self.vec (self.px), pi/180.0*angle_blade) #rotate blade			
			blades = self.MakeBladeRotation(blade_rotate, n_blades)#create copies and fuse
			shaft = self.MakeStub(0.2*r_blades, 1.5*h_blade)
			rci = geompy.MakeFuseList([blades,shaft])
			return rci
		
		def MakeAnchor(self, r_blades, h_blades, base_type):
			
			if base_type == "ASME":
				r_fillet = 0.06*2.0*r_blades;
			else: 
				r_fillet = 0.1*2.0*r_blades;
			
			h_line = h_blades - 2. * r_blades+math.sqrt(3) * r_blades
			p_line_right = geompy.MakeVertex(r_blades, 0., h_blades)
			p_line_left = geompy.MakeVertex(-r_blades, 0., h_blades)
			p_arc_right = geompy.MakeVertex(r_blades, 0., h_blades-h_line)
			p_arc_left = geompy.MakeVertex(-r_blades, 0., h_blades-h_line)
			line_right = geompy.MakeLineTwoPnt(p_line_right, p_arc_right)
			line_left = geompy.MakeLineTwoPnt(p_line_left, p_arc_left)
			arc = geompy.MakeArc(p_arc_right, self.origin, p_arc_left)
			wire = geompy.MakeWire([line_left, arc, line_right])
			anchor = geompy.MakeFillet1D(wire, r_fillet,[])
			return anchor
		
		def MakeAnchorRectangle(self, r_blades, w_blade, t_blade, h_blade, base_type = None):
			blade_base = geompy.MakeFaceObjHW(self.vec(self.px),w_blade,t_blade)
			blade_path = self.MakeAnchor(r_blades, h_blade, base_type)
			blade = geompy.MakePipe(blade_base,blade_path)
			cylinder_right = geompy.MakeCylinder(geompy.MakeVertex(r_blades, -t_blade/2., h_blade), self.vec(self.py), w_blade/2., t_blade)
			cylinder_left = geompy.MakeCylinder(geompy.MakeVertex(-r_blades, -t_blade/2., h_blade), self.vec(self.py), w_blade/2., t_blade)
			shaft = self.MakeStub(0.2*r_blades, 1.5*w_blade)
			anchor = geompy.MakeFuseList([blade,shaft, cylinder_left, cylinder_right],1,1)
			return anchor
			
		def MakeAnchorCircular(self, r_blades, t_blade, h_blade, base_type = None):
			blade_base = geompy.MakeDiskPntVecR(self.origin, self.vec(self.px),t_blade/2.)
			blade_path = self.MakeAnchor(r_blades, h_blade, base_type)
			blade = geompy.MakePipe(blade_base,blade_path)
			sphere_right = geompy.MakeSphere(r_blades, 0., h_blade, t_blade/2.)
			sphere_left = geompy.MakeSphere(-r_blades, 0., h_blade, t_blade/2.)
			shaft = self.MakeStub(0.2*r_blades, 1.5*t_blade)
			anchor = geompy.MakeFuseList([blade,sphere_left, sphere_right, shaft ],1,1)#sphere_left, sphere_right
			return anchor
			
		def MakePBT(self, n_blades, r_blades, w_blade, t_blade, alpha, beta = None, gaama = None):	
			
			if beta is None:
				beta = alpha
			if gaama is None:
				gaama = alpha
				
			p_line_1 = geompy.MakeVertex(0., w_blade/2., 0.)
			p_line_2 = geompy.MakeVertex(0., -w_blade/2., 0.)
			line_1 = geompy.MakeLineTwoPnt (p_line_1, p_line_2)
			line_2 = geompy.MakeTranslationVectorDistance (line_1, self.vec(self.px), r_blades/2., 1)
			line_3 = geompy.MakeTranslationVectorDistance (line_1, self.vec(self.px), r_blades, 1)
			line_1 = geompy.MakeRotation (line_1, self.vec(self.px), pi/180.*alpha)
			line_2 = geompy.MakeRotation (line_2, self.vec(self.px), pi/180.*gaama)
			line_3 = geompy.MakeRotation (line_3, self.vec(self.px), pi/180.*beta)
			blade_base = geompy.MakeFilling( [line_1, line_2, line_3], 2, 5, 0.001, 0.001, 0)
			blade_base = geompy.Thicken(blade_base, t_blade)
			blades = self.MakeBladeRotation(blade_base, n_blades)#create copies and fuse
			shaft = self.MakeStub(0.2*r_blades, 1.5*w_blade)
			pbt = geompy.MakeFuseList([blades, shaft ],1,1)	
			return pbt
			
		def MakeRushton(self, n_blades, r_blades, r_disc, h_disc, l_blade, w_blade, t_blade, alpha = None):
			
			if alpha is None:
				alpha = 0
			blade_base = geompy.MakeBoxDXDYDZ(l_blade, w_blade, t_blade)
			blade_base = geompy.TranslateDXDYDZ(blade_base, r_blades-l_blade, -w_blade/2., -t_blade/2.)
			blade_base = geompy.MakeRotation(blade_base, self.vec(self.px), pi/180.*alpha)
			blades = self.MakeBladeRotation (blade_base, n_blades)
			disc = geompy.MakeCylinder (self.origin, self.vec(self.pz), r_disc, h_disc)
			disc = geompy.TranslateDXDYDZ(disc, 0., 0., -h_disc/2.)
			shaft = self.MakeStub(0.2*r_disc,  t_blade)
			rushton = geompy.MakeFuseList([blades, disc, shaft],1,1)
			return rushton
			
		def MakeSmith(self, n_blades, r_blades, r_disc, h_disc, l_blade, w_blade, t_blade):
			p_arc_1 = geompy.MakeVertex(0., 0., w_blade/2.)
			p_arc_2 = geompy.MakeVertex(0., w_blade/2., 0.)
			p_arc_3 = geompy.MakeVertex(0., 0., -w_blade/2.)
			arc = geompy.MakeArc(p_arc_1, p_arc_2, p_arc_3)
			arc = geompy.MakePrismVecH(arc, self.vec(self.px), l_blade, -1.)
			blade_base = geompy.Thicken(arc, t_blade)
			blade_base = geompy.TranslateDXDYDZ(blade_base, r_blades-l_blade, 0.,  -t_blade/2.)		
			blades = self.MakeBladeRotation (blade_base, n_blades)
			disc = geompy.MakeCylinder (self.origin, self.vec(self.pz), r_disc, h_disc)
			disc = geompy.TranslateDXDYDZ(disc, 0., 0., -h_disc/2.)
			shaft = self.MakeStub(0.2*r_disc,  w_blade)
			smith = geompy.MakeCompound([disc, shaft, blades])					
			return smith
			
		def MakeHydrofoil (self, n_blades, l_blade, w_blade, t_blade, d1_inner, d2_inner, d1_outer=0, d2_outer = 0, alpha = 0):
			if alpha is None:
				alpha = 0
			if d2_outer is None:
				d2_outer = d1_outer
			if d1_outer is None:
				d1_outer = 0
				d2_outer =0
			p1 = geompy.MakeVertex(-t_blade, w_blade, 0)
			p2 = geompy.MakeVertex(-t_blade, -w_blade, 0)
			line_1 = geompy.MakeLineTwoPnt(p1,p2)
			line_2 = geompy.MakeTranslation(line_1, 1.1*l_blade, 0., 0.)
			line_1 = geompy.MakeRotation(line_1, self.vec(self.px), pi/180.*alpha)
			foil_base = geompy.MakeFilling([line_1,line_2],2,5,0.001,0.001,10)
			foil_base = geompy.Thicken(foil_base, t_blade)
			
			
			box = geompy.MakeBoxDXDYDZ(l_blade, w_blade, t_blade*50)			
			box_edge = geompy.SubShapeAll(box, self.hapeTypeEdge)
			b_ind_1 = geompy.GetSubShapeID(box, box_edge[0])
			b_ind_2 = geompy.GetSubShapeID(box, box_edge[4])
			chamfer_inner = geompy.MakeChamferEdges(box, d1_inner, d2_inner, [b_ind_1])
			chamfer_outer = geompy.MakeChamferEdges(box, d1_outer, d2_outer, [b_ind_2])		
			chamfer_box = geompy.MakeCommon(chamfer_inner, chamfer_outer,1)
			chamfer_box = geompy.MakeTranslation(chamfer_box,0.,  -w_blade/2., -t_blade*25)	
			
			blade_base = geompy.MakeCommon(foil_base, chamfer_box,1)
			blade = self.MakeBladeRotation(blade_base, n_blades)
			shaft = self.MakeStub(0.1*l_blade, 1.5*w_blade)
			hydrofoil = geompy.MakeFuseList([blade, shaft],1,1)
			return hydrofoil

		def MakePropeller(self, n_blades, r_blades, t_blade, r_fillet, alpha =45):
			#if alpha is None: 
				#alpha = -45
			sector_origin = geompy.MakeVertex(0., 0., -25*t_blade)
			sector = geompy.MakeCylinderA(sector_origin, self.vec(self.pz), r_blades, 50*t_blade, 60/180.*pi)		
			sector = geompy.MakeRotation(sector, self.vec(self.pz), -30/180.*pi)
			sector_edges = geompy.SubShapeAll(sector, self.ShapeTypeEdge)
			s_ind_1 = geompy.GetSubShapeID(sector, sector_edges[1])
			s_ind_2 = geompy.GetSubShapeID(sector, sector_edges[3])
			fin = geompy.MakeFillet(sector, r_fillet, self.ShapeTypeEdge, [s_ind_1, s_ind_2])
			
			p1 = geompy.MakeVertex(-t_blade, r_blades, 0.)
			p2 = geompy.MakeVertex(-t_blade, -r_blades, 0.)
			line_1 = geompy.MakeLineTwoPnt(p1,p2)
			line_2 = geompy.MakeTranslation(line_1, r_blades+2.*t_blade, 0.,0.)
			line_1 = geompy.MakeRotation (line_1, self.vec(self.px), alpha/180.*pi)
			foil = geompy.MakeFilling([line_1, line_2], 2,5, 0.001, 0.001, 10)
			
			foil = geompy.Thicken (foil, t_blade)		
			blade_base = geompy.MakeCommon(fin, foil)
			blades = self.MakeBladeRotation(blade_base, n_blades)			
			shaft = self.MakeStub(0.2*r_blades,  10*t_blade)
			propeller = geompy.MakeCompound([blades, shaft])		
			
			return propeller

			
	
