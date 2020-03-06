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
    

def parse_args():
  usage = "usage: %prog --path [path to the directory with reports] --table [table name to filter] --label [plot label] --output [output plot name]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option('--path', action="store", dest="path")
  parser.add_option('--table', action="store", dest="table")
  parser.add_option('--output', action="store", dest="output")
  parser.add_option('--label', action="store", dest="label")

  options, remainder = parser.parse_args()

  if options.path == None or options.table == None or options.output == None or options.label == None:
    print(usage)
    return None
  
  return options

def gen_plot_mpki(path, table, plot_title, plot_output):
  # get list of file to parse
  os.system("ls {} | grep {} | grep esesc_ | grep feb22 | grep -v _ldbp_1M_ > report_list.txt".format(path, table))
  os.system("ls {} | grep esesc_ | grep 256K | grep feb22 >> report_list.txt".format(path))

  # get data
  data = []
  data_labels = []
  mpkis = {}
  benchmarks = ["gap_tc", "gap_cc", "gap_pr", "gap_bfs", "spec06_astar", "spec06_hmmer"]
  #benchmarks = ["gap_tc", "gap_pr", "gap_bfs", "spec06_astar", "spec06_hmmer"]
  #benchmarks = ["gap_tc", "gap_cc", "gap_pr", "spec06_astar", "spec06_hmmer"]
  sizes = []
  with open("report_list.txt", "r") as report_list:
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

      if label not in benchmarks:
        continue

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

  perc = []
  base = avg[len(indices)-1]
  print(base)
  for i in range(len(indices)-1):
    comp = avg[i]
    perc_diff = (comp-base)/base/1.0*100
    perc.append([100 - perc_diff, 95])

  perc.append([100, 95])


  print("Data ready: ")
  print(perc)
  print(avg)
  print("Plotting average MPKI vs size into file: {}.png".format(plot_output))

  # Convert data to pandas DataFrame.
  df = pd.DataFrame(perc, index=indices_s, columns=['Percentage reduction', 'Target size'])

  ax = df.plot(kind='line', rot=64, lw=1)
  ax.set_ylabel("Average MPKI")
  ax.set_xlabel("Table size")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}.png".format(plot_output))

def main():
  args = parse_args()
  if args != None:
    gen_plot_mpki(args.path, args.table, args.label, args.output)

main()
