# from .ride import Ride
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

# ride = canape.Ride('data/After_Riccione.gpx')

# df = ride.data[ride.data['active'].values & np.invert(ride.data['power'].isnull().values)]
# p = sns.lineplot(data = df, x = 'seconds', y = 'power')
# p.fill_between(x = df['seconds'].values, y1 = df['power'].values, color = 'gray', alpha = 0.2)
# plt.show()
