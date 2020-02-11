import os
import sys
import optparse
import pandas as pd
import matplotlib.pyplot as plt

def percent(base, offset):
  return float((base-offset)/base/1.0*100)

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

def gen_plot(path, date, plot_title, plot_output):
  # get list of file to parse
  os.system("ls {} | grep {} > report_list.txt".format(path, date))
  # get data
  data = []
  data_labels = []
  mpkis = {}
  with open("report_list.txt", "r") as report_list:
    for rl in report_list:
      rl = rl.strip().split()

      # path to file
      file_name = rl[0]
      report = "{}/{}".format(path, file_name)

      #get label from file name
      file_name_bd = file_name.split("_")
      label = "{}_{}".format(file_name_bd[1], file_name_bd[2])
      bp_type = "{}_{}".format(file_name_bd[3], file_name_bd[4], file_name_bd[5])

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

              if bp_type not in mpkis[label]:
                mpkis[label][bp_type] = []

              mpkis[label][bp_type].append(float(info[len(info) - 1]))


  # format data for the plot: absolute mpki
  for k, v in mpkis.items():
    x = []
    x.append(v["imli_256K"][0])
    x.append(v["imli_1M"][0])
    x.append(v["ldbp_256K"][1])
    x.append(v["ldbp_1M"][1])

    data.append(x)
    data_labels.append(k)

  print("Plotting Absolute MPKI into file: {}.png".format(plot_output))

  # Convert data to pandas DataFrame.
  df = pd.DataFrame(data, index=data_labels)

  # Plot
  df = df.rename(columns={0: "IMPI-256K", 1: "IMLI-1M", 2: "LDBP+IMLI-256K", 3: "LDBP+IMLI-1M"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("MPKI")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}.png".format(plot_output))

  # format data for plot: mpki reduction percentage
  data = []
  for k, v in mpkis.items():
    x = []
    base = v["imli_256K"][0]
    x.append(percent(base, v["imli_1M"][0]))
    x.append(percent(base, v["ldbp_256K"][1]))
    x.append(percent(base, v["ldbp_1M"][1]))

    data.append(x)

  print("Plotting MPKI reduction into file: {}_reduction.png".format(plot_output))

  # Convert data to pandas DataFrame.
  df = pd.DataFrame(data, index=data_labels)

  # Plot
  df = df.rename(columns={0: "IMLI-1M", 1: "LDBP+IMLI-256K", 2: "LDBP+IMLI-1M"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("MPKI reduction in %")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}_redution.png".format(plot_output))

def main():
  args = parse_args()
  if args != None:
    gen_plot(args.path, args.date, args.label, args.output)

main()
