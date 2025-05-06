import numpy as np
import matplotlib.pyplot as plt

skills = []
print('Enter name of file a csv file with required skills')
filename = input()
with open(filename, 'r', encoding='utf-8') as f:
    for i in f:
        skills.append(list(i.split(',')[:-1]))

counter = dict()

for i in skills:
    for skill in i:
        s = skill.lower()
        counter[s] = counter.get(s, 0) + 1

labels = list(counter.keys())  # Skill names
sizes = list(counter.values())  # Counts of each skill

threshold = len(skills) // 20
others_count = 0
filtered_labels = []
filtered_sizes = []

for label, size in zip(labels, sizes):
    if size < threshold//2:
        continue
    if size > threshold:
        filtered_labels.append(label)
        filtered_sizes.append(size)
    else:
        others_count += size

if others_count > 0:
    filtered_labels.append('Others')
    filtered_sizes.append(others_count)



filtered_sizes, filtered_labels = zip(*sorted(zip(filtered_sizes, filtered_labels), reverse=True))

color_palette = plt.get_cmap('tab20', len(filtered_sizes))

# Generate colors for each slice
colors = [color_palette(i % len(filtered_sizes)) for i in range(0, len(filtered_sizes), 2)]
# Plot the pie chart
plt.figure(figsize=(10, 8))
wedges, texts = plt.pie(
    filtered_sizes,
    labels=None,
    autopct=None,
    startangle=90,
    radius=1,
    colors=colors
)

label_x = 2.0
label_y = -0.25
label_spacing = 0.08

# Draw labels and lines for the first 16 labels near the circle
for i, (wedge, label, size) in enumerate(zip(wedges, filtered_labels, filtered_sizes)):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x_line = wedge.r * np.cos(np.radians(angle))
    y_line = wedge.r * np.sin(np.radians(angle))

    percentage = (size / len(skills)) * 100

    if i < 16:
        # Draw the line from the edge of the pie slice to the label
        plt.plot([x_line, x_line * 1.22], [y_line, y_line * 1.22], color='black', linewidth=0.5)

        # Add the label near the circle with percentage
        plt.text(
            x_line * 1.39,
            y_line * 1.39,
            f"{label}\n({percentage:.1f}%)",
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=8
        )
    else:
        # Draw the line from the edge of the pie slice to the label in the top-right corner
        plt.plot([x_line, label_x], [y_line, label_y], color='black', linewidth=0.5)

        # Add the label in the top-right corner with percentage
        plt.text(
            label_x + 0.05,
            label_y,
            f"{label} ({percentage:.1f}%)",
            horizontalalignment='left',
            verticalalignment='center',
            fontsize=8
        )

        # Move the Y-coordinate for the next label in the top-right corner
        label_y += label_spacing

plt.text(
    -2.2, 1.75,  # -2.1, 1.40 for cyber security, (Position of the box)
    """
    Most required skills for data sciene related jobs
    Data is collected from hh.ru for Russia, Belarus, Kazakhstan
    Percentage represents number of jobs in the sample that require the skill
    """,
    fontsize=9,
    bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.5')
)
plt.axis('equal')
plt.show()