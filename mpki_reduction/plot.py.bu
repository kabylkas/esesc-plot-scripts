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

def gen_plot_speedup(path, date, plot_title, plot_output):
  # get list of file to parse
  os.system("ls {} | grep {} > report_list.txt".format(path, date))
  os.system("ls {} | grep oracle | grep feb >> report_list.txt".format(path, date))

  # get data
  data = []
  data_labels = []
  cycles = {}
  with open("report_list.txt", "r") as report_list:
    for rl in report_list:
      rl = rl.strip().split()

      # path to file
      file_name = rl[0]
      report = "{}/{}".format(path, file_name)

      #get label from file name
      file_name_bd = file_name.split("_")
      label = "{}_{}".format(file_name_bd[1], file_name_bd[2])
      if "oracle" in file_name:
        bp_type = "oracle"
      else:
        bp_type = "{}_{}".format(file_name_bd[3], file_name_bd[4])

      os.system("$ESESC_REPORT_PL {0} > temp".format(report))

      state = "search_cycle"
      with open("temp", "r") as report_file:
        for line in report_file:
          if state == "search_cycle":
            if "IPC" in line:
              state = "get_next"
              count = 0

          elif state == "get_next":
            info = line.split()
            if label not in cycles:
              cycles[label] = {}

            if bp_type not in cycles[label]:
              cycles[label][bp_type] = 0

            cycles[label][bp_type] = float(info[1])
            break

  for k, v in cycles.items():
    if len(v) != 5:
      continue

    x = []
    base = v["imli_256K"]
    x.append(percent(base, v["imli_1M"], 1))
    x.append(percent(base, v["ldbp_256K"], 1))
    x.append(percent(base, v["ldbp_1M"], 1))

    data.append(x)
    data_labels.append(k)

  print("Plotting speedup: {}_speedup.png".format(plot_output))

  # Convert data to pandas DataFrame.
  df = pd.DataFrame(data, index=data_labels)

  # Plot
  df = df.rename(columns={0: "IMLI_1M", 1: "IMLI_256K+LDBP", 2: "IMLI_1M+LDBP", 3: "oracle"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("IPC increase in %")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}_speedup.png".format(plot_output))

  data = []
  for k, v in cycles.items():
    if len(v) != 5:
      continue

    x = []
    base = v["imli_256K"]
    x.append(percent(base, v["oracle"], 1))

    data.append(x)

  print("Plotting oracle speedup: {}_speedup_oracle.png".format(plot_output))

  # Convert data to pandas DataFrame.
  df = pd.DataFrame(data, index=data_labels)

  # Plot
  df = df.rename(columns={0: "oracle"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("IPC increase in %")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}_speedup_oracle.png".format(plot_output))

def gen_plot_mpki(path, date, plot_title, plot_output):
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
  df = df.rename(columns={0: "IMPI_256K", 1: "IMLI_1M", 2: "IMLI_256K+LDBP", 3: "IMLI_1M+LDBP"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("MPKI")
  ax.set_title(plot_title)
  ax.set_ylim(0, 100)
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
  df = df.rename(columns={0: "IMLI_1M", 1: "IMLI_256K+LDBP", 2: "IMLI_1M+LDBP"})
  ax = df.plot(kind='bar', rot=64)
  ax.set_ylabel("MPKI reduction in %")
  ax.set_title(plot_title)
  plt.tight_layout()
  plt.savefig("{}_redution.png".format(plot_output))

def main():
  args = parse_args()
  if args != None:
    gen_plot_mpki(args.path, args.date, args.label, args.output)
    gen_plot_speedup(args.path, args.date, args.label, args.output)

main()
