**canape** - **C**ycle **ANA**lyzer of **PE**rformance :bicyclist:
================

`canape` is a lightweight software to read, process, and analyze `.gpx`
data from [Strava](https://strava.com). The `Ride` class allows to read
a file and converts it to a `pandas` data frame.

``` python
from canape import Ride

ride = Ride("data/After_Riccione.gpx")
ride.data.head
```

    |████████████████████████████████████████| 15659/15659 [100%] in 29.1s (538.85/s) 

    <bound method NDFrame.head of          ele                  time power  temp   hr  cad        lat  \
    0      847.0  2023-04-08T08:12:38Z  None    20  147    0  46.601212   
    1      846.6  2023-04-08T08:12:39Z  None    20  147    0  46.601257   
    2      846.2  2023-04-08T08:12:40Z  None    20  147    0  46.601307   
    3      845.6  2023-04-08T08:12:41Z     0    20  147    0  46.601372   
    4      845.2  2023-04-08T08:12:42Z     0    20  147    0  46.601433   
    ...      ...                   ...   ...   ...  ...  ...        ...   
    15654  840.8  2023-04-08T14:49:50Z     0    13  164    0  46.600647   
    15655  840.8  2023-04-08T14:49:51Z     0    13  164    0  46.600647   
    15656  840.8  2023-04-08T14:49:52Z     0    13  164    0  46.600647   
    15657  840.8  2023-04-08T14:49:53Z     0    13  164    0  46.600647   
    15658  840.8  2023-04-08T14:49:54Z  None    13  164    0  46.600647   

                 lon  seconds    meters  active  updown  seconds_interval  \
    0      11.518783      0.0  0.000000   False     NaN               NaN   
    1      11.518810      1.0  0.005412    True    -0.4               1.0   
    2      11.518839      2.0  0.005985    True    -0.4               1.0   
    3      11.518862      3.0  0.007438    True    -0.6               1.0   
    4      11.518880      4.0  0.006921    True    -0.4               1.0   
    ...          ...      ...       ...     ...     ...               ...   
    15654  11.518337  23832.0  0.000968    True     0.0               1.0   
    15655  11.518337  23833.0  0.000000    True     0.0               1.0   
    15656  11.518338  23834.0  0.000076    True     0.0               1.0   
    15657  11.518338  23835.0  0.000000    True     0.0               1.0   
    15658  11.518338  23836.0  0.000000    True     0.0               1.0   

               speed  
    0            NaN  
    1      19.484201  
    2      21.545786  
    3      26.777532  
    4      24.915203  
    ...          ...  
    15654   3.485200  
    15655   0.000000  
    15656   0.275039  
    15657   0.000000  
    15658   0.000000  

    [15659 rows x 14 columns]>
