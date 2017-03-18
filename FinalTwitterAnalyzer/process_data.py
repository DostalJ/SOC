import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.style import use
use('ggplot')


df1 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/CatholicNewsSVC-abortion.txt', header=None)
df2 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/OnlyMormons-abortion.txt', header=None)
df3 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/EvryDayFeminism-abortion.txt', header=None)
df4 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/LGBTfdn-abortion.txt', header=None)
df5 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/BiochemSoc-trump.txt', header=None)
df6 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/PetroleumEcon-trump.txt', header=None)

df7 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/trump.txt', header=None)

df8 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/BiochemSoc-trump-2.txt', header=None)
df9 = pd.read_csv('/Users/Jakub/MEGA/Work/SOC/FinalTwitterAnalyzer/measurements/sentiment/trump-2.txt', header=None)


dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9]
for df in dfs:
    df.columns = ['date', 'sent']
dfs = {'CatholicNewsSVC_abortion': df1['sent'],
       'OnlyMormons_abortion': df2['sent'],
       'EvryDayFeminism_abortion': df3['sent'],
       'LGBTfdn_abortion': df4['sent'],
       'BiochemSoc_trump': df5['sent'],
       'PetroleumEcon_trump': df6['sent'],
       'Twitter_trump': df7['sent'],
       'BiochemSoc_trump-2': df8['sent'],
       'Twitter_trump-2': df9['sent']}

def hist(names, legends, keyword, colors=['b', 'r', 'g', 'k'], num_bins=30, out_path=None):

    data = []
    for name in names:
        data.append(dfs[name])

    plt.hist(x=data, bins=num_bins, normed=False, color=colors[:len(data)], label=legends)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(loc=2)
    plt.title('Keyword: {}'.format(keyword))
    plt.xlabel('Sentiment')
    plt.ylabel(r'Number of tweets [$10^4$]')
    plt.show()

# hist(names=['LGBTfdn_abortion', 'OnlyMormons_abortion'],
#      legends=['LGBTfdn', 'OnlyMormons'],
#      keyword='abortion')
# hist(names=['BiochemSoc_trump', 'PetroleumEcon_trump'],
#      legends=['BiochemSoc', 'PetroleumEcon'],
#      keyword='Trump')
hist(names=['Twitter_trump-2', 'BiochemSoc_trump-2'],
     legends=['Twitter', 'BiochemSoc'],
     keyword='Trump',)
