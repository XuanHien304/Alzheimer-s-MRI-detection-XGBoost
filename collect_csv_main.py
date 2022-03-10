from conver_stat_to_csv import collect_csv
import os
import subprocess
import pandas as pd


if __name__ == '__main__':
    path_stats = '/mnt/data_lab513/xhien/stats/CN'
    df = collect_csv(path_stats)
    df.to_csv('CN.csv')