from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import logging
import time
from datetime import datetime

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Live display for ABC irradiations')
    parser.add_argument(
        '-f', '--file',
        type=str,
        default='Monitoring.txt',
        help="Filename to scan")
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=15,
        help="Refresh interval in seconds")
    parser.add_argument(
        '-d', '--doserate',
        type=float,
        default=0.85,
        help="Dose rate in Mrad/h")
    return parser


def read_file(filename, dt, i, t):
    with io.open(filename, 'r') as f:
        skip = False
        for index, l in enumerate(f):
            if l.startswith('==='):
                dt_string = l.split('===')[1].strip()
                dt_obj = datetime.strptime(dt_string, '%d/%m/%Y %H:%M.%S')
                skip = True if dt_obj in dt else False
                if not skip:
                    dt.append(dt_obj)
            elif l.startswith('NTC') and not skip:
                t.append(float(l.split('=')[1].strip()))
            elif l.startswith('IDDD') and not skip:
                i.append(float(l.split('=')[1].strip()))

    return dt, i, t


def update_view(figure, line1, line2, dt, currents, temps, doserate):
    start_time = dt[0]
    doses = [(d - start_time).total_seconds() * doserate / 3600 for d in dt]
    times = [(d - start_time).total_seconds() for d in dt]
    line1.set_xdata(doses)
    line1.set_ydata(currents)
    line2.set_xdata(times)
    line2.set_ydata(temps)
    figure.canvas.draw()
    figure.canvas.flush_events()


def monitoring(filename, interval, doserate):
    d, i, t = [], [], []
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 0.3)
    ax1.set_xlabel('TID [Mrad]')
    ax1.set_ylabel('IDDD [mA]')
    ax2.set_xlim(0, 1800)
    ax2.set_ylim(10, 30)
    ax2.set_xlabel('time since start [s]')
    ax2.set_ylabel('T [C]')
    line1, = ax1.plot([], [])
    line2, = ax2.plot([], [])

    while True:
        d, i, t = read_file(filename, d, i, t)
        update_view(fig, line1, line2, d, i, t, doserate)
        start_time = d[0]
        dose = (d[-1] - start_time).total_seconds() * doserate / 3600
        t_ = dose * 3600 / doserate
        logger.info("Plotting {} data points".format(len(d)))
        logger.info("latest dose: {:.3g} Mrad --- latest current: {:.3g} mA ---latest temperature: {:.1f} C".format(
            dose, i[-1], t[-1]))
        logger.info("Time since start: {} s".format(t_))
        logger.info("=================================================================================")
        time.sleep(interval)


if __name__ == '__main__':
    args = create_argument_parser().parse_args()
    logging.info("Starting current monitor for file {} -- interval {} s --- dose rate {} Mrad/h".format(
        args.file, args.interval, args.doserate
    ))
    logging.info("############################################################################################\n")
    monitoring(args.file, args.interval, args.doserate)
