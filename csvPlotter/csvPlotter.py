import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from reader import Reader

dataframe = pd.read_csv('Reading Diaries - Sheet 7.csv')
target = 10
readers = [Reader(dataframe['Sarv'], target), Reader(dataframe['Ashish'], target), Reader(dataframe['Ankit'], target)]
names = []
total_pages = []
mean_pages = []
violations = []
eff_violations = []
fines = []

for r in readers:
    r.process()
    names.append(r.name)
    total_pages.append(r.total_pages)
    mean_pages.append(r.mean_pages)
    violations.append(r.violations)
    eff_violations.append(r.eff_violations)
    fines.append(r.fines)

plt.close('all')

fig = plt.figure(1)
fig.clf()
for r in readers:
    plt.plot(dataframe['Date'], getattr(r, 'data'), '-o', label=getattr(r, 'name'))
plt.plot(dataframe['Date'], target * np.ones(dataframe['Date'].size), linestyle = '--', label = 'Target')
plt.xlabel('Date')
plt.ylabel('Pages/day')
plt.title('Reading diaries')
plt.legend()
#plt.grid()

def plot_data(fig_num, x_labels, y_label, data, grid_type = 'major'): # use 'both' for fine grid lines
    fig = plt.figure(fig_num)
    fig.clf()
    y_pos = np.arange(len(x_labels))
    plt.bar(y_pos, data, align='center')
    plt.xticks(y_pos, x_labels)
    plt.ylabel(y_label)
    plt.grid(b=True, which=grid_type)
    plt.minorticks_on()

plot_data(2, names, 'Violations', violations)
plot_data(3, names, 'Effective violations', eff_violations)
plot_data(4, names, 'Fines', fines)
plot_data(5, names, 'Total pages', total_pages)
plot_data(6, names, 'Mean pages', mean_pages)

print(dataframe)

pdf = PdfPages("Sprint7Results.pdf")
for fig in plt.get_fignums(): ## will open an empty extra figure :(
    pdf.savefig(fig)
pdf.close()
plt.show()
