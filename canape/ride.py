from math import floor
from gpx_reader import readStravaGPX
import plotly.express as px
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
        smr = {'up': sum(df.updown[df.updown > 0]),
               'down': sum(df.updown[df.updown < 0]),
               'distance': sum(df.meters),
               'hours_total': sum(df.seconds_interval[1:]) / 60**2,
               'hours_active': sum(df.seconds_interval[df.active]) / 60**2,
               'hours_paused': sum(df.seconds_interval[~df.active]) / 60**2,
               'avg_speed': sum(df.meters) / (sum(df.seconds_interval[df.active]) / 60**2), 
               'avg_power': df.power[df.active].mean()}
        self.summary = smr
    
    def summarize(self):
        print(f"{round(self.summary['distance'], 2)} km - "\
            + f"{prettyTime(self.summary['hours_active'])} - "\
            + f"{round(self.summary['up'])} m climbed\n"\
            + f"  - Avg. power: {round(self.summary['avg_power'], 2)}\n"\
            + f"  - Avg. speed: {round(self.summary['avg_speed'], 2)}\n"\
            + f"  - Total time: {prettyTime(self.summary['hours_total'])}")
    
    def plotData(self, nxintervals = 30 * 60):
        dfactive = self.data[self.data.active].copy()
        dfactive.seconds = dfactive.seconds_interval.cumsum()
        fig = px.line(dfactive, x = "seconds", y = "power")
        nxticks = floor(dfactive.seconds[dfactive.shape[0]] / nxintervals)
        tvals = np.linspace(start=1, stop=nxticks, num=nxticks) * nxintervals
        tlabs = []
        for t in tvals:
            tlabs.append(prettyTime(t / 60**2))
        fig.update_layout(
            xaxis = dict(
                title = None,
                tickmode = 'array',
                tickvals = tvals,
                ticktext = tlabs
                )
            )
        return fig


ride = Ride("../data/After_Riccione.gpx")
# ride.data
# ride.summarize()
ride.plotData().show()
