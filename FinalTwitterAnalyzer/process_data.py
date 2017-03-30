import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.style import use
use('ggplot')


def load_sent(name):
    # df = pd.read_csv(filepath_or_buffer='./measurements/sentiment/' + name + '.csv', header=None)
    # sent = df[1]
    path = './measurements/sentiment/' + name + '.csv'
    f = open(file=path, mode='r')
    sent = []
    for line in f.readlines():
        line = line.split(',')
        sent.append(float(line[1]))
    return sent

def get_proportion(name):
    df = pd.read_csv(filepath_or_buffer='./measurements/sentiment/' + name + '.csv', header=None)
    # df = pd.read_csv(filepath_or_buffer='./measurements/sentiment/' + name + '.txt', header=None)
    sent = df[1]
    l = len(sent)
    p = [0,0]
    for j in range(l):
        if sent[j] < 0.5:
            p[0] += 1/l
        else:
            p[1] += 1/l
    return p
# get_proportion('CatholicNewsSVC-abortion-2')
# get_proportion('EvryDayFeminism-abortion-2')

def hist(names, legends, keyword, colors=['b', 'r', 'g', 'c', 'y'], num_bins=30, normed=False, out_name=None, exp=4):
    plt.clf()

    data = []
    for name in names:
        sent = load_sent(name)
        data.append(sent)

    if normed == True:
        weights = [np.ones_like(array)/float(len(array)) for array in data]
        plt.hist(x=data, bins=num_bins, color=colors[:len(data)], label=legends, weights=weights)
        plt.ylabel(r'Proportion of tweets')

    else:
        plt.hist(x=data, bins=num_bins, color=colors[:len(data)], label=legends)
        plt.ylabel(r'Number of tweets [$10^{}$]'.format(exp))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.legend(loc=2)
    plt.title('Keyword: {}'.format(keyword))
    plt.xlabel('Sentiment')


    if out_name == None:
        plt.show()
    else:
        path = '/Users/Jakub/MEGA/Work/SOC/SOC/Images/' + out_name
        plt.savefig(path, dpi=500)









"""
hist(names=['CatholicNewsSVC-abortion-2', 'OnlyMormons-abortion-2', 'LGBTfdn-abortion-2', 'abortion-3'],
     legends=['CatholicNewsSVC', 'OnlyMormons', 'LGBTfdn', 'Twitter'],
     colors = ['b', 'm', 'g', 'c', 'y'],
     keyword='abortion',
     exp=3,
     normed=False, num_bins=15,
     out_name='abortion-3groups.png')

hist(names=['CatholicNewsSVC-abortion-2', 'EvryDayFeminism-abortion-2'],
     legends=['CatholicNewsSVC', 'EvryDayFeminism'],
     keyword='abortion',
     normed=False,
     exp=5,
     out_name='feminismXcatholic.png')

hist(names=['CatholicNewsSVC-abortion-2', 'EvryDayFeminism-abortion-2'],
     legends=['CatholicNewsSVC', 'EvryDayFeminism'],
     keyword='abortion',
     normed=True,
     out_name='feminismXcatholic-normed.png')

hist(names=['BiochemSoc-trump-3', 'PetroleumEcon-trump-3', 'trump-3'],
     legends=['BiochemSoc', 'PetroleumEcon', 'Twitter'],
     keyword='Trump', num_bins=20,
     out_name='biochem_petroleum-trump.png')

hist(names=['StandingRockST-trump-4', 'trump-4'],
     legends=['StandingRockST', 'Twitter'],
     keyword='Trump', num_bins=30,
     out_name='indiani-trump.png')
"""
