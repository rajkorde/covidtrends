import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


CONFIRMED_FILE = 'confirmed.csv'

def read_data():
    raw = pd.read_csv(CONFIRMED_FILE)

    raw = raw.drop(['Lat', 'Long'], axis=1)
    cols = raw.columns
    raw = raw.rename(columns={cols[0]: "State", cols[1]: "Country"})
    return raw


def get_data(data, state, country, include_feb=False):
    assert country is not None, 'country cannot be empty'
    if state == 'All':
        df = data.query('Country == @country')
    else:
        df = data.query('(State == @state) & (Country == @country)')
    
    assert df.shape[0] == 1, 'more than 1 rows found'
    
    df = df.drop(['State', 'Country'], axis=1).transpose().reset_index()
    df.columns = ('Date', 'Value')
    
    if include_feb:
        df = df.query('Date > "2/1/20"')
    else:
        df = df.query('Date > "3/1/20"')
        
    df.loc[:, 'Date'] = pd.to_datetime(df.Date.astype('str')).dt.strftime('%m/%d')
    
    return df

def get_regions(data):

    df = data[['Country', 'State']]
    df = df.groupby('Country').apply(lambda x: x.to_dict('list'))

    regions = {k: v['State'] for k, v in df.items()}

    for k, v in regions.items():
        if len(regions[k]) == 1:
            regions[k]=['All']
    
    return regions