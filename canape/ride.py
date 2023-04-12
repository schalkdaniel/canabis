# For all kinds of formulas see: https://medium.com/critical-powers/formulas-from-training-and-racing-with-a-power-meter-2a295c661b46

from gpx_reader import readStravaGPX
from math import floor
import plotly.graph_objs as go
import numpy as np

def prettyTime(t):
    hours = floor(t)
    if hours < 1:
        minutes = 60 * (t % 1)
    else:
        minutes = 60 * (t % hours)
    if minutes < 1:
        seconds = 60 * (minutes % 1)
    else:
        seconds = 60 * (minutes % floor(minutes))
    return str(hours).zfill(2) + ":" + str(floor(minutes)).zfill(2) + ":"\
           + str(floor(seconds)).zfill(2) + " h"


class Ride:
    def __init__(self, file):
        df = readStravaGPX(file)
        self.data = df
        meta = {'up': sum(df.updown[df.updown > 0]),
               'down': sum(df.updown[df.updown < 0]),
               'distance': sum(df.meters),
               'hours_total': sum(df.seconds_interval[1:]) / 60**2,
               'hours_active': sum(df.seconds_interval[df.active]) / 60**2,
               'hours_paused': sum(df.seconds_interval[~df.active]) / 60**2,
               'avg_speed': sum(df.meters) / (sum(df.seconds_interval[df.active]) / 60**2), 
               'avg_power': df.power[df.active].mean(),
               'np': Ride.np(self)}
        meta['vi'] = meta['np'] / meta['avg_power']
        self.summary = meta
    
    def summarize(self):
        print(f"{round(self.summary['distance'], 2)} km - "\
            + f"{prettyTime(self.summary['hours_active'])} - "\
            + f"{round(self.summary['up'])} m climbed\n"\
            + f"  - Avg. power: {round(self.summary['avg_power'], 2)}\n"\
            + f"  - Normalized power: {self.summary['np']}\n"\
            + f"  - Avg. speed: {round(self.summary['avg_speed'], 2)}\n"\
            + f"  - Total time: {prettyTime(self.summary['hours_total'])}")
    
    def np(self, window = 30):
        dfactive = self.data[self.data.active].copy()
        dfactive['power_ma'] = dfactive['power'].rolling(window = window).mean()
        return round((dfactive['power_ma']**4).mean()**(1/4))
    
    def setFTP(self, ftp):
        self.summary['ftp'] = ftp
        self.summary['if'] = self.summary['np'] / ftp
        seconds_active = self.summary['hours_active'] * 60**2
        self.summary['tss'] = (seconds_active * self.summary['if'] * self.summary['np']) / (ftp * 36)
    
    def plotData(self, cname, bname = 'ele', nxintervals = 30 * 60):
        dfactive = self.data[self.data.active].copy()
        dfactive.seconds = dfactive.seconds_interval.cumsum()
        nxticks = floor(dfactive.seconds[dfactive.shape[0]] / nxintervals)
        tvals = np.linspace(start=1, stop=nxticks, num=nxticks) * nxintervals
        tlabs = []
        for t in tvals:
            tlabs.append(prettyTime(t / 60**2))
        
        dfactive['bscaled'] = (dfactive[bname] - dfactive[bname].min()) / (dfactive[bname].max() - dfactive[bname].min()) * dfactive[cname].max()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = dfactive['seconds'], y = dfactive['bscaled'],
                                 fill = 'tonexty', name = bname, showlegend = False))
        fig.add_trace(go.Scatter(x = dfactive['seconds'], y = dfactive[cname], 
                                 mode = "lines", name = cname, showlegend = False))
        fig.update_layout(
            yaxis = dict(
                title = cname),
            xaxis = dict(
                title = None,
                tickmode = 'array',
                tickvals = tvals,
                ticktext = tlabs)
            )
        return fig

# dat = readStravaGPX("../data/After_Riccione.gpx")

# ride = Ride("../data/After_Riccione.gpx")
# ride.data
# ride.summary
# ride.setFTP(280)
# ride.summary
# ride.summarize()
# ride.plotData('power').show()
# ride.plotData('speed').show()
# ride.plotData('hr').show()
# ride.plotData('hr', 'power').show()
