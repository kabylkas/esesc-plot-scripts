## Requirements
Make sure you have `pandas` package

* `pip install pandas --user`

## Example usage:
* `export ESESC_REPORT_PL=/soe/nkabylka/projs/esesc-masc/conf/scripts/report.pl`
* `python3 plot.py [plot title] [plot output name] [normalize?]`

Script expects `report_list.txt` file. This repo contains example. Also, three arguments required:
* [plot title]
* [plot output name]
* [normalize?] - 0: will generate absolute values 1: will generate plot normalized to 1

