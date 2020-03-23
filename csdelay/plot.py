import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

plot_title = sys.argv[1]
plot_output = sys.argv[2]
normalize = int(sys.argv[3])

# get data
data = {}
data_labels = []
with open("report_list.txt", "r") as report_list:
  for rl in report_list:
    report = rl.strip()
    file_name = report.split("/").pop()

    d = file_name.split("_")
    label = d[4]
    bench = "{}_{}".format(d[1], d[2])

    os.system("$ESESC_REPORT_PL {0} > temp".format(report))

    state = "search_mpki"
    mpki = 0
    with open("temp", "r") as report_file:
      for line in report_file:
        if state == "search_mpki":
          if "MPKI" in line:
            state = "get_next_three"
            count = 0

        elif state == "get_next_three":
          count += 1
          if count > 3:
            break
          elif count == 3:
            mpki = float(line.split().pop())

    if label not in data:
      data[label] = []
    else:
      data[label].append(mpki)

data_labels = []
for k, v in data.items():
  data_labels.append(int(k))

data_labels.sort()

avg = []
for data_label in data_labels:
  l = data[str(data_label)]
  avg.append(float(sum(l)/len(l)/1.0))

l = "Average MPKI"
if normalize>0:
  n = avg[0]
  l = "Normalized average MPKI"
  for i in range(len(avg)):
    avg[i] = avg[i]/n

df = pd.DataFrame({l: avg}, index=data_labels)
# plot data
print("Parsed reports... Plotting...")
print(avg)
print(data_labels)
# Convert data to pandas DataFrame.

ax = df.plot(kind='line', lw=1, style=["bx-"], ylim=(0,1.5))
ax.set_ylabel(l)
ax.set_xlabel("Code Slice Delay")
ax.set_title(plot_title)
plt.tight_layout()
plt.savefig("{}.png".format(plot_output))
