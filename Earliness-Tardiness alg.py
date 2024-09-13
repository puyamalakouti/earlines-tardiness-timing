import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import itertools

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

jobs = {'1': {'Slopes at infinity': 1, 'Abscissa of the breakpoints': [0, 2], 'Modifiers': [math.inf, 3]},
        '2': {'Slopes at infinity': 1, 'Abscissa of the breakpoints': [0, 1], 'Modifiers': [math.inf, 2]},
        '3': {'Slopes at infinity': 2, 'Abscissa of the breakpoints': [0, 8, 12, 14], 'Modifiers': [math.inf, 1, 1, 3]},
        '4': {'Slopes at infinity': 1, 'Abscissa of the breakpoints': [0, 13], 'Modifiers': [math.inf, 2]},
        '5': {'Slopes at infinity': 3, 'Abscissa of the breakpoints': [0, 7, 9], 'Modifiers': [math.inf, 2, 2]}}

output = pd.DataFrame(columns= ['Iteration', 'Sequence'])

last_idx = {}
for j in jobs.keys():
    last_idx[j] = -1
timeline = []

for idx in jobs.keys():
    output.loc[int(idx), 'Iteration'] = int(idx)
    sigma = jobs[idx]['Slopes at infinity']
    f = int(idx)
    j = int(idx)
    (t_e, m_e) = jobs[idx]['Abscissa of the breakpoints'][last_idx[idx]], jobs[idx]['Modifiers'][last_idx[idx]]
    while sigma >= 0:
        event = (t_e, j, j, m_e)
        timeline.append(event)
        top_event = max(timeline, key=lambda x: x[0])
        timeline.remove(top_event)
        sigma -= top_event[3]
        f = min(event[2], top_event[2])
        if sigma >= 0:
            (t_e, m_e) = jobs[str(top_event[1])]['Abscissa of the breakpoints'][last_idx[str(top_event[1])]], jobs[str(top_event[1])]['Modifiers'][last_idx[str(top_event[1])]]
        last_idx[str(top_event[1])] -= 1
        j = top_event[1]
    timeline.append((top_event[0], top_event[1], f, -sigma))
    output.loc[int(idx), 'Sequence'] = sorted(timeline, key=lambda x: x[0])

i = len(jobs)
x = [0] * i
while i > 0:
    (t, j, f, m) = output.iloc[i - 1, -1][-1]
    while i >= f:
        x[i - 1] = t
        i -= 1

outputStyler = output.style.set_properties(subset=["Iteration"],**{'text-align': 'center'})
outputStyler = output.style.set_properties(subset=["Sequence"],**{'text-align': 'left'})

# Paper Plot
y_values = [entry[0] for entry in output.values]
seq = [entry[1] for entry in output.values]

x_values = {}
for i in y_values:
    x_values[i] = []
    for event in seq[i-1]:
        x_values[i].append(event[0])

points = []
for x, y in x_values.items():
    for y_ in y:
        points.append((x, y_))
        
y, x = zip(*points)
plt.scatter(x, y, color='black', label='points')

for _ in y:
    plt.axhline(_, color= 'black', xmax= 2)

# plot the result
plt.xlabel('t', fontdict={'fontsize': 9, 'fontweight': 'normal', 'family': 'serif'})
plt.ylabel('Iteration', fontdict={'fontsize': 9, 'fontweight': 'normal', 'family': 'serif'})
plt.xlim(-0.5, 16)
plt.ylim(0.6, 5.4)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_ylim(ax.get_ylim()[::-1])
ax.tick_params(axis='both', which='both', length=0)
ax.tick_params(axis='x', labelsize=7)
ax.set_yticklabels([])
plt.title('State of the heap at the end of each iteration', fontdict={'fontsize': 10, 'fontweight': 'normal', 'family': 'sans-serif'})

