import numpy as np
import matplotlib.pyplot as plt
from matplotlib.style import use
use('ggplot')
import pandas as pd

f1 = open('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/BiochemSoc-trump.txt', 'r')
sent1 = f1.read().split(',')[:-1]
sent1 = [float(s) for s in sent1]
f2 = open('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/PetroleumEcon-trump.txt', 'r')
sent2 = f2.read().split(',')[:-2]
sent2 = [float(s) for s in sent2]

df1 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/CatholicNewsSVC-abortion.txt', )
df2 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/OnlyMormons-abortion.txt', )


np.mean(df1['sent'])
np.mean(df2['sent'])

plt.hist([df1['sent'], df2['sent']], bins=30, normed=True)
plt.show()

plt.hist([sent1, sent2], bins=30, normed=True)
plt.show()
