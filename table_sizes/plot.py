import os
import sys
import optparse
import pandas as pd
import matplotlib.pyplot as plt

def percent(base, offset, rev = 0):
  if rev == 0:
    return float((base-offset)/base/1.0*100) 
  else:
    return float((offset-base)/base/1.0*100)
    

def parse_args(cfg_file):
  options = {}
  with open(cfg_file, "r") as infile:
    for line in infile:
       kv = line.strip().split(":")
       k = kv[0]
       v = kv[1]
       options[k] = v
  
  return options

def gen_plot_mpki(path, r_list, plot_output, target, mll, tll, pl, xl, yl):
  # get data
  data = []
  data_labels = []
  mpkis = {}
  sizes = []
  target = float(target)
  with open(r_list, "r") as report_list:
    for rl in report_list:
      rl = rl.strip().split()

      # path to file
      file_name = rl[0]
      report = "{}/{}".format(path, file_name)

      #get label from file name
      file_name_bd = file_name.split("_")
      label = "{}_{}".format(file_name_bd[1], file_name_bd[2])
      if "256K" in file_name:
        size = 512
      else:
        size = int(file_name_bd[4])

      if size not in sizes:
        sizes.append(size)

      os.system("$ESESC_REPORT_PL {0} > temp".format(report))

      state = "search_mpki"
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
              if "--------" in line:
                continue
              info = line.split()
              if label not in mpkis:
                mpkis[label] = {}

              if size not in mpkis[label]:
                mpkis[label][size] = []

              mpkis[label][size].append(float(info[len(info) - 1]))

  # format data for the plot: absolute mpki
  sizes.sort()
  indices = sizes
  indices_s = []
  for k, v in mpkis.items():
    print(k,v)
  for index in indices:
    indices_s.append(str(index))

  avg = []
  for index in indices:
    s = 0
    d = 0
    for k, v in mpkis.items():
      d += 1
      s += v[index][1]

    avg.append(float(s/d/1.0))

  data = []
  base = avg[len(indices)-1]
  print(base)
  for i in range(len(indices)-1):
    comp = avg[i]
    data.append([float(comp/base/1.0), target])

  data.append([1, target])


  print("Data ready: ")
  print(data)
  print(avg)
  print("Plotting average MPKI vs size into file: {}.png".format(plot_output))

  # Convert data to pandas DataFrame.
  s = ["bx-", "r--"]
  df = pd.DataFrame(data, index=indices_s, columns=[mll, tll])

  ax = df.plot(kind='line', rot=64, lw=1, style=s)
  ax.set_ylabel(yl)
  ax.set_xlabel(xl)
  ax.set_title(pl)
  plt.tight_layout()
  plt.savefig("{}.png".format(plot_output))

def main():
  cfg_file = sys.argv[1]
  args = parse_args(cfg_file)
  if args != None:
    gen_plot_mpki(args["path"], \
                  args["list"], \
                  args["output"], \
                  args["target"], \
                  args["main_line_label"], \
                  args["target_line_label"], \
                  args["plot_label"], \
                  args["xlabel"], \
                  args["ylabel"])

main()
