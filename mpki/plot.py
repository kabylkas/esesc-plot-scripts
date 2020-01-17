import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

report_list_file = sys.argv[1]

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
          else:
            info = line.split()
            mpkis.append(float(info[len(info) - 1]))

    data.append(mpkis)
    data_labels.append(label)

# plot data
print("Parsed reports... Plotting...")
print(data)
print(data_labels)
# Convert data to pandas DataFrame.
df = pd.DataFrame(data, index=data_labels).T

# Plot.
pd.concat([df.mean().rename('average'), df.min().rename('min'), df.max().rename('max')], axis=1).plot(kind='bar', rot=30)
plt.savefig('output.png')
