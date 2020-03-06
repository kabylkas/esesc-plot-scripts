## Overview
The `plot.py` will allow to generate a plot that is shown below:
### Normalized
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/mpki_comp/pl_st.png?raw=true)

### Absolute MPKI
![](https://github.com/kabylkas/esesc-plot-scripts/blob/master/mpki_comp/pl_st_abs.png?raw=true)


## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python plot.py report.list "Nice Title" plot.png 1`

There are 4 arguments that you need to provide:
* report.list - list of ESESC report files
* Title of the plot in quotes
* Output file name
* `0` if you want absolute MPKI values, `1` if normalized to 100%

## report.list file
Each line of this file contains two pieces of information:
1. path to the report file that was generated at the end of ESESC 
2. the name of the benchmark, this will be used in x-axis

Example contents:
```
./reports/esesc_noname.zWIHlM gzip
./reports/esesc_noname.zYfxEw bfs
./reports/esesc_noname.zZvmIK bzip
./reports/esesc_noname.zarugw bzip2
./reports/esesc_noname.zd3hst dhrystone
./reports/esesc_noname.zqIs14 dfs
./reports/esesc_noname.zrbNDx coremark
```
