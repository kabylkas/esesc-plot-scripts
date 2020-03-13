## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python3 plot.py --path /soe/akashsridhar/build_esesc_riscv/trace_data/run --list report_list_pref.txt --label "LOR table" --output lor_p`

There are 4 arguments that you need to provide:
* --path expects path to the directory with bunch of report files
* --list expects the list of files to be processed
* --label expects title of the plot
* --output expects prefix for the plots that will be generated


## Format of report list file:

