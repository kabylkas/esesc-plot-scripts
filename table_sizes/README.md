## Overview
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/table_sizes/lor_p.png?raw=true)

## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python3 plot.py plot.cfg

## Example of plot.cfg
```
path:/soe/akashsridhar/build_esesc_riscv/trace_data/run
list:report_list_pref.txt
output:lor_p
target:1.005
main_line_label:Normalized average MPKI
target_line_label:5% MPKI increase
plot_label:LOR table
xlabel:x-label
ylabel:y-label
```

## Format of report list file:
I suggest to create a serarate list for each table type. This directory contains example list for prefetcher table. For the script to work properly, the list should be complete. This means that for each benchmark, the reports for all 6 runs should be present in the list. The name of the reports should also comply with naming convension that we agreed upon (sorry, this script is very fragile).

![format](https://github.com/kabylkas/esesc-plot-scripts/blob/master/table_sizes/docs/report_list.png?raw=true)
