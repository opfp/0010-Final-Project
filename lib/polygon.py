class Line:
	def __init__(self, x, y, m):
		self.x = float(x)
		self.y = float(y)
		self.m = float(m)
		self.yint = self.y - ( self.x * self.m )

	def __str__(self):
		return "y = " + str(self.m) + " x + " + str(self.yint) + " : (" + str(self.x) \
			+ " , " + str(self.y) + ")"

class Ray:
	def __init__(self, cords):
		if isinstance(cords, list):
			self.x1 = float(cords[0])
			self.y1 = float(cords[1])
			self.x2 = float(cords[2])
			self.y2 = float(cords[3])
		elif isinstance(cords, str):
			self.x1 = float(cords[cords.index("[")+2:cords.index(",")])
			cords = cords[cords.index(",")+1:]
			self.y1 = float(cords[:cords.index("]")-1])
			cords = cords[cords.index("]")+5:]
			self.x2 = float(cords[:cords.index(",")])
			cords = cords[cords.index(",")+2:]
			self.y2 = float(cords[:cords.index("]")-1])

		if ( (self.x2 - self.x1) == 0 ):
			self.m = None # None means vertical line
			self.yint = None
		else:
			self.m = ( self.y2 - self.y1 ) / ( self.x2 - self.x1 )
			self.yint = self.y1 - (self.m * self.x1 )
		# Keeping track of these ranges helps keep intersection checking efficent
		if ( self.x1 < self.x2 ):
			self.xrange = (self.x1, self.x2)
		else:
			self.xrange = (self.x2, self.x1)

		if ( self.y1 < self.y2 ):
			self.yrange = (self.y1, self.y2)
		else:
			self.yrange = (self.y2, self.y1)

	def __str__(self):
		if self.m is None:
			sl = "VERT"
			xi = "DNE"
		else:
			sl = str(self.m)
			xi = str(self.yint)

		x1 = str(self.x1)
		y1 = str(self.y1)
		x2 = str(self.x2)
		y2 = str(self.y2)

		return "y = " + sl + " x + " + xi + " : [ ( " + x1 + " , " + y1 + " ) ( " +\
			x2 + " , " + y2 + " ) ]"

class Polygon:
	def __init__(self, name, rays):
		self.name = name

		if rays is None or len(rays) == 0:
			print( "Error: %s cannot be empty" % (name) )
			raise TypeError

		self.rays = rays

		# again, keeping track of range for efficency
		self.xrange = list(rays[0].xrange)
		self.yrange = list(rays[0].yrange)
		for ray in rays:
			if (ray.xrange[0] < self.xrange[0]):
				self.xrange[0] = ray.xrange[0]
			if (ray.xrange[1] > self.xrange[1]):
				self.xrange[1] = ray.xrange[1]
			if (ray.yrange[0] < self.yrange[0]):
				self.yrange[0] = ray.yrange[0]
			if (ray.yrange[1] > self.yrange[1]):
				self.yrange[1] = ray.yrange[1]

	def __str__(self):
		return self.name + " :  X: " + str(self.xrange[0]) + " -- " + str(self.xrange[1]) \
			+ " Y: " + str(self.yrange[0]) + " -- " + str(self.yrange[1])
