import os
import sys
from polygon import Ray
from polygon import Line
from polygon import Polygon

# def load_polygons_pef(filepath):
# 	raw_plygons = open(filepath, "r").read() #.split("}")
# 	ray_list = []
#
# 	while ( "{" in raw_plygons ):
# 		eos = raw_plygons.index("}")
# 		polygon = raw_plygons[:eos]
# 		polygon = polygon.split("{")
# 		name = polygon[0]
# 		rays = polygon[1]
#
# 		while ( "[" in rays ):
# 			ray = rays[rays.index("["):rays.index("\n")]
# 			print(ray)
# 			ray_list.append(Ray(ray))
# 			rays = rays[:rays.index("\n")+1]
#
# 		raw_plygon = raw_plygon[:eos+1]
#
# 	return ray_list

def load_polygons_leg(filepath):
	raw_plygons = open(filepath, "r").read()
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

	return ngh_polygons

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
