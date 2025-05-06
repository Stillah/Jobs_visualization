import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json

salaries = []
print('Enter name of a file with salaries')
filename = input()
with open(filename, 'r') as f:
    for i in f:
        if i.strip() == 'null': continue
        x = json.loads(i)       
        min_salary = x['from']
        max_salary = x['to']
        
        if min_salary is None and max_salary is not None:
            min_salary = max_salary * 0.75
        elif max_salary is None and min_salary is not None:
            max_salary = min_salary * 1.25

        if x['currency'] == 'KZT':
            min_salary /= 6.3
            max_salary /= 6.3

        if x['currency'] == 'BYR':
            min_salary *= 27.33
            max_salary *= 27.33
        
        if x['currency'] == 'USD':
            min_salary *= 82
            max_salary *= 82

        if x['currency'] == 'EUR':
            min_salary *= 93
            max_salary *= 93
        salaries.append(int((min_salary + max_salary) // 2))


bin_size = 50000
max_salary = 500000
salaries.sort()
# Create bins up to max_bin, then one more for 500K+
bins = list(range(0, max_salary + bin_size, bin_size))
if len(salaries) > 0 and np.max(salaries) > max_salary:
    bins.append(np.inf)  # Add infinity as the last bin edge

# Generate bin labels
bin_labels = []
for i in range(len(bins)-1):
    if i == len(bins)-2 and bins[-1] == np.inf:
        bin_labels.append(f'500K+')
    else:
        bin_labels.append(f'{bins[i]//1000}K-{bins[i+1]//1000}K')

counts, _ = np.histogram(salaries, bins=bins)

cmap = LinearSegmentedColormap.from_list('count_cmap', ['#d4e6ff', '#0044cc'])
    
# Normalize counts for coloring (0 to max count)
norm = plt.Normalize(vmin=0, vmax=np.max(counts))
colors = cmap(norm(counts))
# Plotting
plt.figure(figsize=(12, 6))
bars = plt.bar(bin_labels, counts, color=colors)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')

# Chart formatting
plt.title('Salary Distribution for {}\nData from hh.ru for Russia, Belarus, Kazakhstan'.format(filename), fontsize=16)
plt.xlabel('Salary Range (RUB per month)', fontsize=12)
plt.ylabel('Number of vacancies', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
