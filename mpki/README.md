## Overview
The `plot.py` will allow to generate a plot that is shown below:
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/mpki/plot.png?raw=true)

## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python plot.py report.list`

## `report.list` file
Each line of this file contains two pieces of information:
1. path to the report file that was generated at the end of ESESC 
2. the name of the benchmark, this will be used in x-axis

Example:
```
./reports/esesc_noname.zWIHlM gzip
./reports/esesc_noname.zYfxEw bfs
./reports/esesc_noname.zZvmIK bzip
./reports/esesc_noname.zarugw bzip2
./reports/esesc_noname.zd3hst dhrystone
./reports/esesc_noname.zqIs14 dfs
./reports/esesc_noname.zrbNDx coremark
```
