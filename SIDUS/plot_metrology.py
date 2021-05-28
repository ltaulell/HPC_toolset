#!/usr/bin/env python3
# coding: utf-8
#
# $Id: plot_metrology.py 2937 2020-06-19 13:04:13Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

"""
POC/training

graph metrology from CSV file (using test_ipmitool.py)

"""

import argparse
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Plot temp/power metrology from IPMI data')
    parser.add_argument('-d', '--debug', action='store_true', help='Active le debug')
    parser.add_argument('-f', '--file', nargs=1, type=str, help='data file to parse')

    return parser.parse_args()


def dateparse(date):
    """ transformer à la volée epoch en date """
    return pd.to_datetime(date, origin='unix', unit='s')


if __name__ == '__main__':
    """ """
    args = get_args()
    if args.debug:
        debug = True
        print(args)
    else:
        debug = False

    data_path = args.file[0]

    with open(data_path, 'r') as f:
        series = pd.read_csv(f, header=0, index_col=0, parse_dates=['date'], date_parser=dateparse)
        if debug:
            print(type(series))
            print(series.shape)
            print(series.dtypes)
            print(series.index)
            print(series.head())
        print(series.describe())

        # Use seaborn style defaults and set the default figure size
        sns.set(rc={'figure.figsize': (11, 4)})
        # series.plot()
        series[['CPU1', 'CPU2']].plot()
        plt.show()
