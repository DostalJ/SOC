import numpy as np
import matplotlib.pyplot as plt
from matplotlib.style import use
use('ggplot')

f1 = open('./test.txt', 'r')
sent1 = f1.read().split(',')[:-1]
sent1 = [float(s) for s in sent1]
f2 = open('./test2.txt', 'r')
sent2 = f2.read().split(',')[:-2]
sent2 = [float(s) for s in sent2]


plt.hist(sent1, 100, normed=True)
plt.hist(sent2, 100, normed=True)
plt.show()
