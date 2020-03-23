import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

report_list_file = sys.argv[1]
plot_title = sys.argv[2]
plot_output = sys.argv[3]

# get data
data = []
data_labels = []
with open(report_list_file, "r") as report_list:
  for rl in report_list:
    rl = rl.strip().split()
    report = rl[0]
    label = rl[1]

    os.system("$ESESC_REPORT_PL {0} > temp".format(report))

    state = "search_mpki"
    mpkis = []
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
          elif count != 1:
            info = line.split()
            mpkis.append(float(info[len(info) - 1]))

    data.append(mpkis)
    data_labels.append(label)

# plot data
print("Parsed reports... Plotting...")
print(data)
print(data_labels)

data_to_plot = []
for d in data:
  data_to_plot.append(d[1]/d[0])

# Convert data to pandas DataFrame.
df = pd.DataFrame({'Normalized MPKI (baseline IMLI)': data_to_plot}, index=data_labels)

print(df)
ax = df.plot(kind='bar', rot=30)

ax.set_ylabel("Normalized MPKI")
ax.set_title(plot_title)
plt.savefig(plot_output)
