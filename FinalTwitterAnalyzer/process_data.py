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

df1 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/CatholicNewsSVC-abortion.txt', header=None)
df2 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/OnlyMormons-abortion.txt', header=None)
df3 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/EvryDayFeminism-abortion.txt', header=None)
df4 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/LGBTfdn-abortion.txt', header=None)

dfs = [df1, df2, df3, df4]
for df in dfs:
    df.columns = ['date', 'sent']

# plt.hist([df['sent'] for df in dfs], bins=15, normed=False, color=['b', 'r', 'g', 'k'])
plt.hist([df1['sent'], df3['sent']], bins=15, normed=False, color=['b','g'])
plt.show()

plt.hist([sent1, sent2], bins=30, normed=False, color=['b', 'r'])
plt.show()
