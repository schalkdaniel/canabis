from math import radians, cos, sin, asin, sqrt
from xml.dom import minidom
import pandas as pd
from datetime import datetime
from alive_progress import alive_bar

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def nodeListToDict(nl):
    out = {'ele': None, 'time': None, 'power': None, 'temp': None, 'hr': None,
           'cad': None}
    for i in nl:
        if i.nodeName != '#text':
            if i.nodeName == 'ele':
                out[i.nodeName] = [float(i.childNodes[0].data)]
            elif i.nodeName == 'time':
                out[i.nodeName] = [i.childNodes[0].data]
            elif i.nodeName == 'gpxtpx:atemp':
                out['temp'] = [int(i.childNodes[0].data)]
            elif i.nodeName == 'gpxtpx:hr':
                out['hr'] = [int(i.childNodes[0].data)]
            elif i.nodeName == 'gpxtpx:cad':
                out['cad'] = [int(i.childNodes[0].data)]
            elif i.nodeName == 'extensions':
                if i.childNodes[1].nodeName == "power":
                    out['power'] = [int(i.childNodes[1].childNodes[0].data)]
                    dmerge = nodeListToDict(i.childNodes[3].childNodes)
                else:
                    out['power'] = None
                    dmerge = nodeListToDict(i.childNodes[1].childNodes)
                for key in ['temp', 'hr', 'cad']:
                    out[key] = dmerge[key]
    return out

def toDateTime(tstring, timeformat = '%Y-%m-%dT%H:%M:%SZ'):
    return datetime.strptime(tstring, timeformat)

# 'data/After_Riccione.gpx'
def readStravaGPX(file) -> pd.DataFrame:
    dom = minidom.parse(file)
    elements = dom.getElementsByTagName('trkpt')
    
    lat = []
    lon = []
    seconds = []
    meters = [0]
    active = [False]
    df = pd.DataFrame()
    t0 = toDateTime(nodeListToDict(elements[0].childNodes)['time'][0])
    with alive_bar(elements.length) as bar:
        for element in elements:
            n = len(df.index)
            rowmeta = pd.DataFrame.from_dict(nodeListToDict(element.childNodes))
            difft = toDateTime(rowmeta.time[0]) - t0
            difft = difft.total_seconds()
            seconds.append(difft)
            lat.append(float(element.attributes.items()[0][1]))
            lon.append(float(element.attributes.items()[1][1]))
            if n > 0:
                meters.append(haversine(lon[n], lat[n], lon[n-1], lat[n-1]))
                if seconds[n] - seconds[n-1] <= 1: # Label if an interval lasts longer than 1 second (probably a break).
                    active.append(True)
                else:
                    active.append(False)
            df = pd.concat([df, rowmeta], ignore_index = True)
            bar()
    
    df['lat'] = lat
    df['lon'] = lon
    df['seconds'] = seconds
    df['meters'] = meters
    df['active'] = active
    df['updown'] = df.ele.diff()
    df['seconds_interval'] = df.seconds.diff()
    
    return df
