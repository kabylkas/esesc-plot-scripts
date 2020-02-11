## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python3 plot.py --path /soe/akashsridhar/build_esesc_riscv/trace_data/run --date feb8_2020 --label "Nice title" --output plot`

There are 4 arguments that you need to provide:
* --path expects path to the directory with bunch of report files
* --date expects the date in the file name. The scripts essentially greps for this date
* --label expects title of the plot
* --output expects prefix for the plots that will be generated

Note that oracle files should be in the same directory.

## The script will generate
* `<prefix>.png` - plot of absolute mpki values
* `<prefix>_reduction.png` - plot of the mpki reduction from the baseline
* `<prefix>_speedup.png` - plot of the IPC increase from the baseline
* `<prefix>_speedup_oracle.png` - plot of the IPC increase from the baseline (oracle only)

