import pef_polygon_interface as pefpi

ngh_polygons = pefpi.load_polygons_leg("/Users/owen/cs/dev/0010/ignore/polygons.txt")

# for polygon in ngh_polygons:
# 	for ray in polygon.rays:
# 		print(ray)

print("Interactive testing mode: seperate N,E with a single comma. * to quit.")
while(True):
	cords = input()
	if ( "*" in cords ):
		break

	c = cords.replace(" ", "").split(",")
	x = float(c[1])
	y = float(c[0])
	if ( x is None or y is None ) :
		continue

	found = False
	for polygon in ngh_polygons:
		if ( pefpi.falls_in(x, y, polygon) ):
			print("%f, %f is in %s" % (x,y, polygon.name ) )
			found=True

	if not found:
		print("Coordinates unmatched.")
