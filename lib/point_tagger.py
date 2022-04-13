import sys
import os

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

def main( argc, argv ):
	cdir = __file__.split(os.path.sep)[1:]
	datapath = ""
	for i in range(0,len(cdir)-2): # go up 1 directory
		datapath += os.path.sep + cdir[i]

	datapath += os.path.sep + "data"

	raw_plygons = open(datapath + os.path.sep + "polygons.txt", "r").read()
	raw_plygons = raw_plygons[raw_plygons.index("urn:ogc:def:crs:OGC:1.3:CRS84"):]

	ngh_polygons = []

	while(True):
		if ("name" not in raw_plygons or "coordinates" not in raw_plygons):
			break

		namei = raw_plygons.index("name")
		cordi = raw_plygons.index("coordinates")

		name = raw_plygons[namei+8:]
		name = name[:name.index(",")-1]

		eofshape = raw_plygons.index("] ] ]")+1
		shape_cords = raw_plygons[cordi+20:eofshape]

		rays = []
		while(True):
			if "," not in shape_cords:
				break

			brack1 = shape_cords.index("]")+1

			if "," not in shape_cords[brack1:]:
				break

			brack2 = brack1 + shape_cords[brack1:].index("]")+1

			rays.append(Ray(shape_cords[:brack2]))
			# shape_cords = shape_cords[brack2+1:]
			shape_cords = shape_cords[brack1+1:] # each point should have a ray begining and ending there

		raw_plygons = raw_plygons[eofshape+6:]

		if len(rays) == 0 :
			#print( "%s EMPTY:\n%s" % (name, shape_cords))
			continue

		ngh_polygons.append(Polygon(name,rays))

	# for plygn in ngh_polygons:
	#     print(plygn)

	print("Interactive testing mode: seperate N,E with a single comma")
	while(True):
		cords = input()
		c = cords.replace(" ", "").split(",")
		x = float(c[1])
		y = float(c[0])
		if ( x is None or y is None ) :
			continue

		found = False
		for polygon in ngh_polygons:
			if ( falls_in(x, y, polygon) ):
				print("%f, %f is in %s" % (x,y, polygon.name ) )
				found=True

		if not found:
			print("Coordinates unmatched.")

def falls_in(x, y, polygon):
	if not isinstance(polygon, Polygon):
		raise TypeError

	if not inrange(x,y, polygon) :
		return False

	icount = 0

	for polygon_edge in polygon.rays:
		line = Line(x, y, 0)
		int = intersect(polygon_edge, line ) # Horizontal line check
		if isinstance(int, tuple):
			icount += 1
			#print( "line %s intersects polygon %s at (%f, %f) for the %i time" % (line, polygon, int[1], int[2], icount) )

	return ( ( icount % 2 ) == 1)

def intersect( ray, line ):
	if not isinstance(ray, Ray) or not isinstance(line, Line):
		raise TypeError

	# If same line, check for pt falls on edge
	if (ray.m == line.m ):
	# if ( ( ray.m is not None and line.m is not None ) and ( (ray.m - line.m) < .00001 ) and ( (ray.m - line.m) > -.00001 ) ):
		#print( "Line %s and ray %s have the same slope" % ( line , ray ) )
		if ( (ray.yint == line.yint) and inrange(line.x, line.y, ray) ) :
			return (1, line.x , line.y )
			#return True
		else:
			return 0
	# else find intersection pt
	if ( ray.yint is None ): # handle vertical lines
		int_x = ray.x1
		int_y = ( int_x * line.m ) + line.yint
	elif ( line.yint is None ) :
		int_x = line.x
		int_y = ( int_x * ray.m ) + ray.yint
	else:
		int_x = ( ray.yint - line.yint ) / ( line.m - ray.m)
		int_y = (int_x * ray.m) + ray.yint
		# optional check
		int_precision = abs(int_y - ( (int_x * line.m) + line.yint))
		if ( int_precision > .00001 ):
			#print("Line %s intersects ray %s
			print("Intersection at (%f, %f) checked with line %s failed : found (%f, %f ) " \
				% ( int_x, int_y, line, int_x, (int_x * line.m) + line.yint) )
			raise ArithmeticError

	# Check if intersection point is within ray bounds
	if inrange(int_x, int_y, ray) and ( int_x >= line.x ) :
		return (1, int_x, int_y)

	return 0

def inrange( x, y, has_range ):
	if not (isinstance(has_range, Ray) or isinstance(has_range, Polygon) ) :
		raise TypeError
	return ( (x >= has_range.xrange[0]) and (x <= has_range.xrange[1]) and (y >= has_range.yrange[0]) and (y <= has_range.yrange[1]) )

if __name__ == "__main__":
	#__test__()
	main( len(sys.argv), sys.argv )
