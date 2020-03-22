from utils import read_data

raw = read_data()

df = raw[['Country', 'State']]

#df = df.set_index('Country')
df = df.groupby('Country').apply(lambda x: x.to_dict('list'))

regions = {k: v['State'] for k, v in df.items()}

for k,v in regions.items():
    if len(regions[k]) == 1:
        regions[k]=['All']

#.reset_index(drop=True).to_dict()
