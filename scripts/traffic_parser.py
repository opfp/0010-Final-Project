import pef_polygon_interface as pefpi

ngh_uids = {}

raw_uids = open("ngh_uids.txt", "r").read().split("\n")

for ngh in raw_uids:
    if ( ":" not in ngh ):
        continue
    ngh = ngh.split(":")
    ngh_uids[ngh[1].replace(" ", "")] = int(ngh[0])

ngh_polygons = pefpi.load_polygons_leg("/Users/owen/cs/dev/0010/data_raw/polygons.txt")

ngh_count = {}

for ngh in ngh_polygons:
    ngh_count[ngh] = []

raw_traffic_data = open("traffic_count.txt", "r").read()

while( "average_daily_car_traffic" in raw_traffic_data ):
    s = raw_traffic_data.index("average_daily_car_traffic") + 28
    raw_camera = raw_traffic_data[s:]
    # raw_camera = raw_camera[:raw_camera.index("Point")]

    raw_vol = raw_camera[:raw_camera.index(",")]
    if ( "null" in raw_vol ):
        raw_traffic_data = raw_traffic_data[s:]
        continue
    volume = int(raw_vol[:raw_vol.index(".")])

    raw_cords = raw_camera[raw_camera.index("coordinates")+15:].replace("\n", "").split(",")
    x = float(raw_cords[0])
    y = float(raw_cords[1])

    for ngh in ngh_polygons:
        if pefpi.falls_in(x,y, ngh):
            ngh_count[ngh].append(volume)
            break

    raw_traffic_data = raw_traffic_data[s:]

outlines = []
outfile = open("/Users/owen/cs/dev/0010/data_parsed/car_volume_by_ngh.txt", "w+")

for ngh in ngh_polygons:
    uid = ngh_uids[ngh.name.replace(" ","")]
    cams = len(ngh_count[ngh])
    if ( cams == 0 ):
        continue
    av = sum(ngh_count[ngh]) / cams
    # print( "%s (%i) has an average of %i cars per day (%i cameras)" \
    #     % (ngh.name, uid, av , cams ) )

    outlines.append(str(uid) + " : " + str(av) + "\n")

for line in outlines:
    outfile.write(line)

outfile.close()
