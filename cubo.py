import math
from tkinter import *
import matrix
import random



class Simulation:
	''' Coordiante-system: Right-handed, Matrices are column-major ones '''

	WIDTH = 640.0
	HEIGHT = 640.0

	RATE = 1
	SPEED = 0.2

	def __init__(self, root):
		self.root = root
		self.graph = Canvas(self.root, width = 75, height = 75, bg = 'gray10', highlightbackground = "gray10")
		self.graph.place(x = 1, y = 1)

		#The vectors of the Coordinate System (CS)
		self.cs = [
			matrix.Vector3D(0.0, 0.0, 0.0), #Origin
			matrix.Vector3D(0.5, 0.0, 0.0), #X
			matrix.Vector3D(0.0, 0.5, 0.0), #Y
			matrix.Vector3D(0.0 ,0.0, 0.5), #Z
			]

		#Let these be in World-coordinates (worldview-matrix already applied)
		#In right-handed, counter-clockwise order
		size = 0.05
		self.cube = [
			matrix.Vector3D(-size,size,-size),
			matrix.Vector3D(size,size,-size),
			matrix.Vector3D(size,-size,-size),
			matrix.Vector3D(-size,-size,-size),
			matrix.Vector3D(-size,size,size),
			matrix.Vector3D(size,size,size),
			matrix.Vector3D(size,-size,size),
			matrix.Vector3D(-size,-size,size)
        	]

		self.dotx = matrix.Vector3D(-0.5, 0.0, 0.0)
		self.doty = matrix.Vector3D(0.0, -0.5, 0.0)
		self.dotz = matrix.Vector3D(0.0, 0.0, -0.5)


		# Define the vertices that compose each of the 6 faces. These numbers are
		# indices to the vertices list defined above.
		self.cubefaces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)] 

		self.ang = [0.0, 0.0, 0.0] # phi(x), theta(y), psi(z)
		self.trans = [0.0, 0.0, 0.0] # translation (x, y, z) (e.g. if want to move the Camera to (0, 0, 2) then (0, 0, -2) need to be entered)

		#The matrices (Scale, Shear, Rotate, Translate) apply to the View/Camera

		#The Scale Matrix
		self.Scale = matrix.Matrix(4, 4)
		Scalex = 1.0
		Scaley = 1.0
		Scalez = 1.0
		self.Scale[(0,0)] = Scalex
		self.Scale[(1,1)] = Scaley
		self.Scale[(2,2)] = Scalez

		#The Shear Matrix
		self.Shearxy = matrix.Matrix(4, 4)
		self.Shearxy[(0,2)] = 0.0
		self.Shearxy[(1,2)] = 0.0
		self.Shearxz = matrix.Matrix(4, 4)
		self.Shearxz[(0,1)] = 0.0
		self.Shearxz[(2,1)] = 0.0
		self.Shearyz = matrix.Matrix(4, 4)
		self.Shearyz[(1,0)] = 0.0
		self.Shearyz[(2,0)] = 0.0
		self.Shear = self.Shearxy*self.Shearxz*self.Shearyz

		#The Rotation Matrices
		self.Rotx = matrix.Matrix(4,4)
		self.Roty = matrix.Matrix(4,4)
		self.Rotz = matrix.Matrix(4,4)

		#The Translation Matrix (will contain xoffset, yoffset, zoffset)
		self.Tr = matrix.Matrix(4, 4)	

		#The Projection Matrix
		self.Proj = matrix.Matrix(4, 4)	
		#foc controls how much of the screen is viewed
		fov = 90.0 #between 30 and 90 ?
		zfar = 100.0
		znear = 0.1
		S = 1/(math.tan(math.radians(fov/2)))
#1st version (Perspective Projection)
		self.Proj[(0,0)] = S
		self.Proj[(1,1)] = S
		self.Proj[(2,2)] = -zfar/(zfar-znear)
		self.Proj[(3,2)] = -1.0
		self.Proj[(2,3)] = -(zfar*znear)/(zfar-znear)


		self.lctrl_pressed = False

		self.root.bind("<Motion>", self.dragcallback)
		self.root.bind("<ButtonRelease-1>", self.releasecallback)
		self.root.bind("<Key>", self.keycallback)
		self.root.bind("<KeyRelease>", self.keyreleasecallback)

		self.cnt = Simulation.RATE
		self.prevmouseX = 0.0
		self.prevmouseY = 0.0

		self.update()
		mainloop()

	def toScreenCoords(self, pv):
#		print str(pv)
		#Projection will project to [-1; 1] so the points need to be scaled on screen
		px = min(((pv.x+1)*0.5*Simulation.WIDTH), Simulation.WIDTH-1) - 280
		#Reflect the Y-coordinate because the screen it goes downwards
		py = min(((1-(pv.y+1)*0.5)*Simulation.HEIGHT), Simulation.HEIGHT-1) - 280

		return matrix.Vector3D(int(px), int(py), 1)

	def update(self):
		# Main simulation loop.
		self.graph.delete(ALL)

		self.Rotx[(1,1)] = math.cos(math.radians(self.ang[0]))
		self.Rotx[(1,2)] = -math.sin(math.radians(self.ang[0]))
		self.Rotx[(2,1)] = math.sin(math.radians(self.ang[0]))
		self.Rotx[(2,2)] = math.cos(math.radians(self.ang[0]))

		self.Roty[(0,0)] = math.cos(math.radians(self.ang[1]))
		self.Roty[(0,2)] = math.sin(math.radians(self.ang[1]))
		self.Roty[(2,0)] = -math.sin(math.radians(self.ang[1]))
		self.Roty[(2,2)] = math.cos(math.radians(self.ang[1]))

		self.Rotz[(0,0)] = math.cos(math.radians(self.ang[2]))
		self.Rotz[(0,1)] = -math.sin(math.radians(self.ang[2]))
		self.Rotz[(1,0)] = math.sin(math.radians(self.ang[2]))
		self.Rotz[(1,1)] = math.cos(math.radians(self.ang[2]))

		#The Rotation matrix
		self.Rot = self.Rotx*self.Roty*self.Rotz

		self.Tr[(0,3)] = self.trans[0]
		self.Tr[(1,3)] = self.trans[1]
		self.Tr[(2,3)] = self.trans[2]

		#The Transformation matrix
		self.Tsf = self.Scale*self.Shear*self.Rot*self.Tr

		inviewingvolume = False

		#First draw the lines of the CS
		tvs = [] #transformed vectors
		for v in self.cs:
			r = self.Tsf*v
			ps = self.Proj*r
			tvs.append(self.toScreenCoords(ps))

			#if only one vertex is in the screen (x[-1,1], y[-1,1], z[-1,1]) then we draw the whole CS 
			if (-1.0 <= ps.x <= 1.0) and (-1.0 <= ps.y <= 1.0) and (-1.0 <= ps.z <= 1.0):
				inviewingvolume = True

		inviewingvolume = False

		#Cube
		for i in range(len(self.cubefaces)):
			inviewingvolume = False
			poly = [] #transformed polygon
			for j in range(len(self.cubefaces[0])):
				v = self.cube[self.cubefaces[i][j]]

				# Scale, Shear, Rotate the vertex around X axis, then around Y axis, and finally around Z axis and Translate.
				r = self.Tsf*v

				# Transform the point from 3D to 2D
				ps = self.Proj*r

				# Put the screenpoint in the list of transformed vertices
				p = self.toScreenCoords(ps)
				x = int(p.x)
				y = int(p.y)
				poly.append((x, y))

				#if only one vertex is in the screen (x[-1,1], y[-1,1], z[-1,1]) then draw the whole polygon
				if (-1.0 <= ps.x <= 1.0) and (-1.0 <= ps.y <= 1.0) and (-1.0 <= ps.z <= 1.0):
					inviewingvolume = True

			if inviewingvolume:
				r = lambda: random.randint(20,255)
				for k in range(len(poly)-1):
					self.graph.create_line(poly[k][0], poly[k][1], poly[k+1][0], poly[k+1][1], fill = 'dark turquoise', width = 1.5) #, fill='#%02X%02X%02X' % (r(),r(),r()))

				self.graph.create_line(poly[len(poly)-1][0], poly[len(poly)-1][1], poly[0][0], poly[0][1], fill='white', width = 1.5) 

		inviewingvolume = False
		return self.graph


	def dragcallback(self, event):
#		It's also possible to use the angle calculated from the mousepos-change from the center of the screen:
#		dx = event.x - Simulation.WIDTH/2
#		dy = event.y - Simulation.HEIGHT/2
#		ang = math.degrees(math.atan2(dy, dx))


		self.cnt -= 1
		if self.cnt == 0:
			self.cnt = Simulation.RATE
			diffX = (event.x-self.prevmouseX)
			diffY = (event.y-self.prevmouseY)

			if not self.lctrl_pressed:
				self.ang[0] += diffY*Simulation.SPEED
				self.ang[1] += diffX*Simulation.SPEED

				if self.ang[0] >= 360.0:
					self.ang[0] -= 360.0
				if self.ang[0] < 0.0:
					self.ang[0] += 360.0
				if self.ang[1] >= 360.0:
					self.ang[1] -= 360.0
				if self.ang[1] < 0.0:
					self.ang[1] += 360.0

			else:
				self.ang[2] += diffX*Simulation.SPEED
				if self.ang[2] >= 360.0:
					self.ang[2] -= 360.0
				if self.ang[2] < 0.0:
					self.ang[2] += 360.0

			self.update()

		self.prevmouseX = event.x
		self.prevmouseY = event.y


	def releasecallback(self, event):
		self.cnt = Simulation.RATE
		self.prevmouseX = 0.0
		self.prevmouseY = 0.0


	def keycallback(self, event):
#		print event.char
#		print event.keycode
#		print event.keysym
		if event.keysym == "Control_L":
			self.lctrl_pressed = True


	def keyreleasecallback(self, event):
		if event.keysym == "Control_L":
			self.lctrl_pressed = False


if __name__ == "__main__":
	root = Tk()
	root.resizable(False, False)
	root.title('3D')
	left = (root.winfo_screenwidth() - Simulation.WIDTH) / 2
	top = (root.winfo_screenheight() - Simulation.HEIGHT) / 2
	root.geometry('%dx%d+%d+%d' % (Simulation.WIDTH, Simulation.HEIGHT, left, top))
	graph = Canvas(root, width=10, height=10, background='black')
	graph.pack()
	Simulation(root)



