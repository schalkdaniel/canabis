**canape** - **C**ycle **ANA**lyzer of **PE**rformance :bicyclist:
================

`canape` is a lightweight software to read, process, and analyze `.gpx`
data from [Strava](https://strava.com). The `Ride` class allows to read
a file and converts it to a `pandas` data frame.

Importing the `Ride` class allows to read from Strave `*.gpx` files:

``` python
from canape import Ride

ride = Ride("data/After_Riccione.gpx")
ride.data[['ele', 'time', 'power', 'lon', 'lat', 'speed']].head()
```

    |████████████████████████████████████████| 15659/15659 [100%] in 24.9s (629.04/s) 

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ele</th>
      <th>time</th>
      <th>power</th>
      <th>lon</th>
      <th>lat</th>
      <th>speed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>847.0</td>
      <td>2023-04-08T08:12:38Z</td>
      <td>None</td>
      <td>11.518783</td>
      <td>46.601212</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>846.6</td>
      <td>2023-04-08T08:12:39Z</td>
      <td>None</td>
      <td>11.518810</td>
      <td>46.601257</td>
      <td>19.484201</td>
    </tr>
    <tr>
      <th>2</th>
      <td>846.2</td>
      <td>2023-04-08T08:12:40Z</td>
      <td>None</td>
      <td>11.518839</td>
      <td>46.601307</td>
      <td>21.545786</td>
    </tr>
    <tr>
      <th>3</th>
      <td>845.6</td>
      <td>2023-04-08T08:12:41Z</td>
      <td>0</td>
      <td>11.518862</td>
      <td>46.601372</td>
      <td>26.777532</td>
    </tr>
    <tr>
      <th>4</th>
      <td>845.2</td>
      <td>2023-04-08T08:12:42Z</td>
      <td>0</td>
      <td>11.518880</td>
      <td>46.601433</td>
      <td>24.915203</td>
    </tr>
  </tbody>
</table>
</div>

Helper functions allows to show a summary of relevant statistics like
the normalized power, average speed, or climbed meters:

``` python
ride.summary
```

    {'up': 2669.199999999857,
     'down': -2675.3999999999805,
     'distance': 89.02978956387291,
     'hours_total': 6.621111111111111,
     'hours_active': 4.342222222222222,
     'hours_paused': nan,
     'avg_speed': 20.503278046951284,
     'avg_power': 171.51008258114078,
     'np': 207,
     'vi': 1.2069261286844117}

Setting an FTP automatically calculates further statistics such as the
intensity factor or stress level:

``` python
ride.setFTP(250)
ride.summary
```

    {'up': 2669.199999999857,
     'down': -2675.3999999999805,
     'distance': 89.02978956387291,
     'hours_total': 6.621111111111111,
     'hours_active': 4.342222222222222,
     'hours_paused': nan,
     'avg_speed': 20.503278046951284,
     'avg_power': 171.51008258114078,
     'np': 207,
     'vi': 1.2069261286844117,
     'ftp': 250,
     'if': 0.828,
     'tss': 297.695808}

Plotting is done with plotly as backend:

``` python
ride.plotData('power').show()
```

![](README_files/plolty-power.png)
