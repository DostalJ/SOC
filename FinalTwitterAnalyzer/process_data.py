import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.style import use
use('ggplot')


def load_sent(name, keyword):

    # df = pd.read_csv(filepath_or_buffer='./Data/sentiment/' + name + '.csv', header=None)
    # sent = df[1]

    path = './Data/sentiment/' + keyword + '-' + name + '.csv'
    f = open(file=path, mode='r')
    sent = []
    for line in f.readlines():
        line = line.split(',')
        sent.append(float(line[1]))
    return sent

def get_proportion(name, keyword):
    df = pd.read_csv(filepath_or_buffer='./Data/sentiment/' + keyword + '-' + name + '.csv', header=None)
    sent = df[1]
    l = len(sent)
    p = [0,0]
    for j in range(l):
        if sent[j] < 0.5:
            p[0] += 1/l
        else:
            p[1] += 1/l
    return p

pages = ['PPact', 'EvrydayFeminism', 'Students4LifeHQ', 'AmenditUSA']
for page in pages:
    print(page, get_proportion(page, 'abortion'))


def hist(names, legend, keyword, colors=['b', 'r', 'g', 'c', 'y', 'm'], num_bins=30, normed=False, out_name=None, exp=4):
    plt.clf()

    data = []
    for name in names:
        sent = load_sent(name, keyword)
        data.append(sent)

    if normed == True:
        weights = [np.ones_like(array)/float(len(array)) for array in data]
        plt.hist(x=data, bins=num_bins, color=colors[:len(data)], label=legend, weights=weights)
        plt.ylabel(r'Proportion of tweets')

    else:
        plt.hist(x=data, bins=num_bins, color=colors[:len(data)], label=legend)
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
hist(names=['PPact', 'EvrydayFeminism',
            'Students4LifeHQ', 'AmenditUSA'],
     legend=['Planned Parenthood (Pro)', 'Everyday Feminism (Pro)',
             'Students for Life (Proti)', 'Abolish Abortion USA (Proti)'],
     keyword='abortion',
     exp=2,
     normed=False, num_bins=5,
     out_name='abortion.png')

hist(names=['PPact', 'EvrydayFeminism',
            'Students4LifeHQ', 'AmenditUSA'],
     legend=['Planned Parenthood (Pro)', 'Everyday Feminism (Pro)',
             'Students for Life (Proti)', 'Abolish Abortion USA (Proti)'],
     keyword='abortion',
     exp=2,
     normed=True, num_bins=5,
     out_name='abortion-normed.png')

"""
