'''
設備異常
    pH連續3點無變化
    導電度為0或超過5,000 μS/cm以 上（偵測極限）
水質異常
    離群值條件（時間）：導電度連 續3點超出80或低於20分位
    離群值條件（空間）：上下游測 站溫度同時超出80或低於20分位
    法規限值條件：pH低於6或高於9
    離群值條件可以用GMM處理
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv_file/water_potability.csv')
df = df.dropna() # drop nan
print(df.info())
print(df.head())

# plot ph values and distribution using histogram and scatter plot

ph = df.ph
# if ph > 9 or ph < 6 label = 1 else label = 0
ph_label = np.where(ph > 9, 1, np.where(ph < 6, 1, 0))

## using the label to plot the error
plt.plot(ph_label)


# plt.subplot(1,2,1)
# plt.hist(ph, bins=20)
# plt.subplot(1,2,2)
# plt.plot(ph)
# plt.show()

# # plot Hardness values and distribution using histogram and scatter plot
# Hardness = df.Hardness
# std_hardness = np.std(Hardness)
# mean_hardness = np.mean(Hardness)
# plt.subplot(1,2,1)
# plt.hist(Hardness, bins=20)
# plt.subplot(1,2,2)
# plt.plot(Hardness)



# # draw mean values and show values
# plt.axhline(y=mean_hardness, color='g', linestyle='-')
# plt.text(0, mean_hardness, 'mean:'+str(mean_hardness))

# # fill color red to the date bigger than outliers(+-3*std) and show values
# plt.axhspan(mean_hardness+3*std_hardness, Hardness.max(), facecolor='r', alpha=0.5)
# plt.axhspan(mean_hardness-3*std_hardness, Hardness.min(), facecolor='r', alpha=0.5)

# plt.axhline(y=mean_hardness+3*std_hardness, color='r', linestyle='-')
# plt.axhline(y=mean_hardness-3*std_hardness, color='r', linestyle='-')

# plt.text(0, mean_hardness+3*std_hardness, 'outliers')
# plt.text(0, mean_hardness-3*std_hardness, 'outliers')

plt.show()