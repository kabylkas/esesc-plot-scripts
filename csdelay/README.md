## Overview
The script generates the following plots:
#### Normalize average MPKI
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/csdelay/2.png?raw=true)

#### Absolute average MPKI
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/csdelay/3.png?raw=true)

## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python3 plot.py [plot title] [plot output name] [normalize?] [y_min] [y_max]`

Script expects `report_list.txt` file. This repo contains example. Also, three arguments required:
* [plot title]
* [plot output name]
* [normalize?] - 0: will generate absolute values 1: will generate plot normalized to 1
* y-axis limits: [y_min] and [y_max] this controls the range of y-axis to be shown on the plot

