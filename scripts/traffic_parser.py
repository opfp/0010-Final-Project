import pef_polygon_interface as pefpi

ngh_uids = {}

raw_uids = open("/Users/owen/cs/dev/0010/data/ngh_uids.txt", "r").read().split("\n")

for ngh in raw_uids:
    if ( ":" not in ngh ):
        continue
    ngh = ngh.split(":")
    ngh_uids[ngh[1].replace(" ", "")] = int(ngh[0])

ngh_polygons = pefpi.load_polygons_leg("/Users/owen/cs/dev/0010/data/polygons.txt")

ngh_count = {}

for ngh in ngh_polygons:
    ngh_count[ngh] = 0

pacc_stops = open("/Users/owen/cs/dev/0010/data/paac_stops.csv", "r").read().split("\n")[1:]

for stop in pacc_stops:
    if "," not in stop:
        continue
    cords = stop.split(",")
    x = float(cords[0])
    y = float(cords[1])

    for ngh in ngh_polygons:
        if pefpi.falls_in(x,y, ngh):
            ngh_count[ngh] += 1
            break

outlines = []
outfile = open("/Users/owen/cs/dev/0010/data/paac_stops_by_ngh.txt", "w+")

for ngh in ngh_polygons:
    uid = ngh_uids[ngh.name.replace(" ","")]
    outlines.append(str(uid) + " : " + str(ngh_count[ngh]) + "\n")
    #print( "%s (%i) has %i PAAC stops" % (ngh.name, uid, ngh_count[ngh] ) )

for line in outlines:
    outfile.write(line)

outfile.close()
