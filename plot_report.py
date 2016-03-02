#!/usr/bin/env python
# coding: utf-8

"""
   File Name: plot_report.py
      Author: Wan Ji
      E-mail: wanji@live.com
  Created on: Thu Jul 30 13:12:01 2015 CST
"""
DESCRIPTION = """
Plot the report file
"""

import os
import argparse
import logging

import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def runcmd(cmd):
    """ Run command.
    """

    logging.info("%s" % cmd)
    os.system(cmd)


def getargs():
    """ Parse program arguments.
    """

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('report', type=str,
                        help='report file')
    parser.add_argument('figdir', type=str,
                        help='directory to save the figure ')
    parser.add_argument('indexers', type=str, nargs='+',
                        help='(PQIndexer|SHIndexer)')
    parser.add_argument("--log", type=str, default="INFO",
                        help="log level")

    return parser.parse_args()


def load_report(report_path):
    report_lines = []
    with open(report_path, "r") as rptf:
        for line in rptf:
            if line.startswith("*" * 64):
                report_lines = []
            report_lines.append(line.strip())
    return report_lines


def parse_report(report_lines):
    v_results = []
    cur_result = None
    index = None
    nbits = None
    for line in report_lines:
        if line.startswith("index_"):
            if cur_result is not None:
                v_results.append((index, nbits, cur_result))
            cur_result = []
            index = line.split("-")[0].split("_")[1]
            nbits = int(line.split("-")[1].split("_")[1])
        elif line.startswith("recall@"):
            K = int(line.split()[0].split("recall@")[-1])
            R = float(line.split()[1])
            cur_result.append((K, R))
    if cur_result is not None:
        v_results.append((index, nbits, cur_result))
    return v_results


def main(args):
    """ Main entry.
    """
    report_lines = load_report(args.report)
    v_results = parse_report(report_lines)

    font = {'family': 'normal',
            # 'weight': 'bold',
            'size': 16}

    matplotlib.rc('font', **font)

    for i, indexer in zip(range(len(args.indexers)), args.indexers):
        fig = plt.figure(i)
        ax = fig.add_subplot(1, 1, 1)
        ax.hold(True)
        print v_results
        for index, nbits, results in v_results:
            if nbits not in [128, 64, 32, 16, 8]:
                continue
            if index != indexer:
                continue
            X = [r[0] for r in results]
            Y = [r[1] for r in results]
            print np.vstack((X, Y))
            ax.plot(X, Y, label="%d-bit" % (nbits))
            plt.xlabel("$R$")
            plt.ylabel("$recall$")
        ax.hold(False)
        ax.set_xscale("log")
        # pl.legend(loc='lower right')
        plt.legend(loc='upper left')
        plt.savefig(args.figdir + "/%s.png" % indexer)
        plt.savefig(args.figdir + "/%s.eps" % indexer)
    plt.show()


if __name__ == '__main__':
    args = getargs()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: " + args.log)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=numeric_level)
    main(args)
