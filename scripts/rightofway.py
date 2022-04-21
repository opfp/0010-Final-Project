import pandas as pd

data = pd.read_csv('RIght of Way Permits.csv')

data.pop('id')
data.pop('sequence')
data.pop('open_date')
data.pop('from_date')
data.pop('to_date')
data.pop('restoration_date')
data.pop('address')
data.pop('street_or_location')
data.pop('type')
data.pop('from_street')
data.pop('to_street')
data.pop('business_name')
data.pop('license_type')
data.pop('council_district')
data.pop('ward')
data.pop('tract')
data.pop('public_works_division')
data.pop('address_lat')
data.pop('address_lon')
data.pop('from_lat')
data.pop('from_lon')
data.pop('to_lat')
data.pop('to_lon')

dict = {}
for ind in data.index:
    if data['neighborhood'][ind] not in dict:
        dict[data['neighborhood'][ind]] = 0 
    dict[data['neighborhood'][ind]] += 1

for key, value in dict.items() :
    print (key, value)

finaldf = pd.DataFrame(dict.items(), columns=['neighborhood', 'right of way permits'])
print (finaldf)

finaldf.to_csv('/Users/abjures/Desktop/final_right_of_way_permits.csv')