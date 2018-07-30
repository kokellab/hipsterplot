#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Ian Horn <horn.imh@gmail.com> and
#                    Danilo J. S. Bellini <danilo.bellini@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function, division
import math, random, sys
from operator import itemgetter

# Python 2.x and 3.x compatibility
if sys.version_info.major == 2:
    range = xrange
    from future_builtins import map, zip

# ◌ ▪▼
CHAR_LOOKUP_SYMBOLS = [(0, ' '),(10, '·'), (20, '▫'), (30, '▪'), (40, 'o'), (50, 'O'), (60, '□'), (70, '•'), (80, '⓿'), (90, '■'), (100, '█')]


def bin_generator(data, bin_ends):
    """ Yields a list for each bin """
    max_idx_end = len(bin_ends) - 1
    iends = enumerate(bin_ends)

    idx_end, value_end = next(iends)
    bin_data = []
    for el in sorted(data):
        while el >= value_end and idx_end != max_idx_end:
            yield bin_data
            bin_data = []
            idx_end, value_end = next(iends)
        bin_data.append(el)

    # Finish
    for unused in iends:
        yield bin_data
        bin_data = []
    yield bin_data


def enumerated_reversed(seq):
    """ A version of reversed(enumerate(seq)) that actually works """
    return zip(range(len(seq) - 1, -1, -1), reversed(seq))


def gen_plot(y_vals, x_vals=None, num_x_chars=120, num_y_chars=15):

    def charlookup(num_chars):
        """ Character for the given amount of elements in the bin """
        #print(num_chars)
        return next(ch for num, ch in CHAR_LOOKUP_SYMBOLS if num_chars <= num)

    y_vals = list(y_vals)
    x_vals = list(x_vals) if x_vals else list(range(len(y_vals)))
    if len(x_vals) != len(y_vals):
        raise ValueError("x_vals and y_vals must have the same length")

    ymin = min(y_vals)
    ymax = max(y_vals)
    xmin = min(x_vals)
    xmax = max(x_vals)

    xbinwidth = (xmax - xmin) / num_x_chars
    y_bin_width = (ymax - ymin) / num_y_chars

    x_bin_ends = [(xmin + (i+1) * xbinwidth, 0) for i in range(num_x_chars)]
    y_bin_ends = [ymin + (i+1) * y_bin_width for i in range(num_y_chars)]

    columns_pairs = bin_generator(zip(x_vals, y_vals), x_bin_ends)
    columns_pairs_argh = bin_generator(zip(x_vals, y_vals), x_bin_ends)
    ygetter = lambda iterable: map(itemgetter(1), iterable)
    argh = lambda *args: [len(el) for el in bin_generator(*args)]
    max_density = max(max(argh(ygetter(pairs), y_bin_ends)) for pairs in columns_pairs_argh)
    print(max_density)
    yloop = lambda *args: [charlookup(len(el) * 100 / max_density) for el in bin_generator(*args)]
    columns = (yloop(ygetter(pairs), y_bin_ends) for pairs in columns_pairs)
    rows = list(zip(*columns))

    for idx, row in enumerated_reversed(rows):
        y_bin_mid = y_bin_ends[idx] - y_bin_width * 0.5
        yield "{:.2E} {}".format(y_bin_mid, "".join(row))


def plot(y_vals, x_vals=None, num_x_chars=70, num_y_chars=15):
    """
    Plots the values given by y_vals. The x_vals values are the y indexes, by
    default, unless explicitly given. Pairs (x, y) are matched by the x_vals
    and y_vals indexes, so these must have the same length.

    The num_x_chars and num_y_chars inputs are respectively the width and
    height for the output plot to be printed, given in characters.
    """
    for p in gen_plot(y_vals, x_vals, num_x_chars, num_y_chars):
        print(p)


if __name__ == '__main__':
    #xs = [x**1.5+0.5*x*random.random() for x in range(1, int(round(120**1.5)))]
    #print(list(sorted(xs)))
    #ys = [math.cos(8*x**(0.5)/120.0)+5*random.random()/math.sqrt(x) for x in xs]
    xs = list(range(-100, 100))
    ys = [x**3 for x in xs]
    ys2 = [2000*x+2000*random.random() if x % 10 != 0 else 7*10**5 for x in xs]
    xs.extend(xs)
    ys.extend(ys2)
    num_x_chars = 120
    print('')
    plot(ys, x_vals=xs, num_x_chars=num_x_chars, num_y_chars=20)
    print('')
