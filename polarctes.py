#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Felipe Gallego. All rights reserved.
#
# Script to get a polar plot for sky darkness measurements. 
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import numpy as np
from matplotlib.pyplot import *

# Log levels, taken from logging.
LOG_LEVELS = { "CRITICAL" : logging.CRITICAL,
              "ERROR": logging.ERROR,
              "WARNING": logging.WARNING,
              "INFO": logging.INFO,
              "DEBUG": logging.DEBUG }

DEFAULT_LOG_LEVEL_NAME = "WARNING"

DEFAULT_LOG_FILE_NAME = "log.txt"

# Extension for the files of data.
DATA_FILE_EXT = 'dat'
DATA_FILE_MIN_LINES = 2
DATA_FILE_ITEM_WITH_TITLE = 0
DATA_FILE_ITEM_WITH_DATA = 1
DATA_SEPARATOR = ','
DATA_SIZE = 65
DATA_LIST_TITLE = 0
DATA_LIST_DATA = 1

# Zenith values where measures have been taken.
ZENITHS = [20, 40, 60, 80, 90]

# All the values for zenith, plus one to get the last value
ALL_ZENITH_VALUES = np.array((range(ZENITHS[0], ZENITHS[-1] + 1)))

# All the values for zenith, plus one to get the last value in reverse order.
ALL_ZENITH_VALUES_INV = np.array(range(ZENITHS[-1], ZENITHS[0] - 1, -1))

# Azimuth values where measures have been taken.
AZIMUTHS = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]

# Range of values for azimuth, plus one to get the last value
AZIMUTH_RANGE = range(AZIMUTHS[0], AZIMUTHS[-1] + 1)

# Plot settings.
LIGHTEST_VALUE = 19.0
DARKER_VALUE = 22.0

GRIDS_ALPHA = 0.6
CONTOUR_ALPHA = 0.7

TITLE_X_POS = 1.1
TITLE_Y_POS = 1.03

# Direction to plot the values from 0 degrees and increasing,
CLOCKWISE_DIRECTION = -1
COUNTERCLOCKWISE_DIRECTION = 1

# Color bar settings.
COLORBAR_SHRINK = 0.9
COLORBAR_PAD = 0.08
COLORBAR_THICKNESS = 30
COLORBAR_LABEL = "Oscuridad del cielo (mag/arcsec²)"

COLORMAP_NAME = 'YellowBlack'

# Distance between contour lines.
CONTOUR_LINES_DISTANCE = 6
CONTOUR_LINE_WIDTH = 0.4
CONTOUR_FONT_SIZE = 10

# Ticks labels settings
X_TICKS_LABELS = ['N', '', 'E', '', 'S', '', 'O', '']

DEG_CHR = unichr(176)

X_TICKS_LABELS_DEG = ['0' + DEG_CHR, '30' + DEG_CHR, '60' + DEG_CHR, 
                        '90' + DEG_CHR, '120' + DEG_CHR, '150' + DEG_CHR, 
                        '180' + DEG_CHR, '210' + DEG_CHR,  '240' + DEG_CHR, 
                        '270' + DEG_CHR, '300' + DEG_CHR, '330' + DEG_CHR]

Y_TICKS_RANGE = range(90, 20, 20)

def define_color_map():
    """ Define a color map to plot the values.
    """
    
    # This color map goes from a brilliant yellow to black passing by 
    # dark blue tones.
    cdict = {'red':   ((0.0, 0.8, 0.8),
                       (0.55, 0.35, 0.35),
                       (1.0, 0.001, 0.001)),
    
             'green': ((0.0, 0.6, 0.6),
                       (0.55, 0.35, 0.35),
                       (1.0, 0.001, 0.001)),
    
             'blue':  ((0.0, 0.01, 0.01),
                       (0.63, 0.35, 0.35),
                       (1.0, 0.03, 0.03))
            }  
    
    # Register the color map defined.
    register_cmap(name=COLORMAP_NAME, data=cdict)