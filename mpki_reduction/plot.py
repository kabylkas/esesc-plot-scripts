import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

report_list_file = sys.argv[1]
plot_title = sys.argv[2]
plot_output = sys.argv[3]

def parse_args():
  usage = "usage: %prog --path [path to the directory with reports] --date [when the reports were generated] --label [plot label] --output [output plot name]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option('--path', action="store", dest="path")
  parser.add_option('--date', action="store", dest="date")
  parser.add_option('--output', action="store", dest="output")
  parser.add_option('--label', action="store", dest="label")

  options, remainder = parser.parse_args()

  if options.path == None or options.date == None or options.output == None or options.label == None:
    print(usage)
    return None
  
  return options

def gen_plot():
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
  # Convert data to pandas DataFrame.
  df = pd.DataFrame(data, index=data_labels)

  # Plot
  df = df.rename(columns={0: "TAGE", 1: "LDBP"})
  print(df)
  ax = df.plot(kind='bar', rot=30)

  ax.set_ylabel("MPKI")
  ax.set_title(plot_title)
  plt.savefig(plot_output)

def main():
  args = parse_args()
  if args != None:
    gen_plot(args.path, args.date, args.label, args.output)
