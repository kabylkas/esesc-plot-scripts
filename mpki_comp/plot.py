import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

report_list_file = sys.argv[1]
plot_title = sys.argv[2]
plot_output = sys.argv[3]
normalize = int(sys.argv[4])

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

    os.system("grep _prof_ {0} > temp".format(report))
    count = 0
    branch_info = {}
    with open("temp", "r") as report_file:
      for line in report_file:
        count += 1
        profs = line.split(":")
        for prof in profs:
          if "=" not in prof:
            continue
          kv = prof.split("=")
          k = kv[0]
          v = kv[1]
          if "on_time_tl" in k or "no_tl" in k or "late_tl" in k:
            if k in branch_info:
              branch_info[k] += int(v)
            else:
              branch_info[k] = int(v)
    for k, v in branch_info.items():
      branch_info[k] = float(v/count)

    if normalize == 1:
      x = mpkis[0]
      y = mpkis[1]
      mpkis[0] = 100
      mpkis[1] = y/x*100

    perc = branch_info["late_tl"]/(branch_info["late_tl"]+branch_info["no_tl"])
    a = mpkis[0]-mpkis[1]
    b = mpkis[1]*perc
    c = mpkis[1]-b
    data.append([c,b,a])
    data_labels.append(label)

    
# plot data
print("Parsed reports... Plotting...")
print(data)
print(data_labels)
# Convert data to pandas DataFrame.
df = pd.DataFrame(data, index=data_labels)

# Plot
df = df.rename(columns={0: "Not predictable", 1: "Predictable but late", 2: "LDBP impact"})
print(df)
ax = df.plot(kind='bar', rot=30, stacked=True)

ylabel = "MPKI"
if normalize == 1:
  ylabel += " (in %)"

ax.set_ylabel(ylabel)
ax.set_title(plot_title)
plt.tight_layout()
plt.savefig(plot_output)
