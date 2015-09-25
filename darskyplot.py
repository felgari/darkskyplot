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

import numpy as np
import glob
import sys
import os
import logging
import pargparser
import re
from matplotlib.pyplot import *
from polarctes import *
from polardata import *

def init_log(progargs):
    """ Initializes the file log and messages format. 
    
    Args:
        progargs - ProgramArguments object, it contains the information of all 
            program arguments received.
    
    """ 
    
    # If no log level is indicated use the default level.
    if progargs.log_level_provided:
        logging_level = LOG_LEVELS[progargs.log_level]
    else:
        logging_level = LOG_LEVELS[DEFAULT_LOG_LEVEL_NAME]
    
    # If a file name has been provided as program argument use it.
    if progargs.log_file_provided:
        log_file = progargs.log_file_name
    else:
        log_file = sys.stdout
    
    # Set the logger parameters.
    root = logging.getLogger()
    root.setLevel(logging_level)

    ch = logging.StreamHandler(log_file)
    ch.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    ch.setFormatter(formatter)
    
    root.addHandler(ch)
    
    logging.debug("Logging initialized.")    

def data_is_valid(data_read):
    """ Check if the data read has the right format.
    
    Data must have two lines, the first is taken as text containing the title
    of the data.
    The second line must be an array of real numbers with a given length.
    
    Args:
        data - The data read.
        
    Returns:
        A list if the data format is valid, None otherwise.
        
    """
      
    data_output = None
    
    # The file must contain at least a number of lines. More lines are
    # discarded.
    if len(data_read) >= DATA_FILE_MIN_LINES:
        data_line = data_read[DATA_FILE_ITEM_WITH_DATA]
        
        # Separate data in a item list.
        data_line_split = data_line.split(DATA_SEPARATOR)
        
        # Check the length of the list of elements.
        if len(data_line_split) == DATA_SIZE:
            # Convert items to float
            data_numbers = [float(i) for i in data_line_split] 
            
            # Check if all the items are float numbers.
            if all(isinstance(x, float) for x in data_numbers):
                data_output = [data_read[DATA_FILE_ITEM_WITH_TITLE],\
                               data_numbers]
            else:
                logging.warning('Data contains items that are not real numbers.')
        else:
            logging.warning('Data size is not valid: ' + \
                            str(len(data_line_split)))
    else:
        logging.warning('Number of lines in files is not enough:' + \
                        str(len(data_read)))
    
    return data_output

def read_data_files(path):
    """ Read data from files.
    
    The data are read from file with a given extension from the path received.
    Each file must contain a first line with the title for the data and a
    second line with the list of measures taken.
    
    Args:
        path - The path where the files are read.
        
    Returns:
        The data read. A list with an item for each file read.
        Each item contains the title of the data and a list of the measures.
        
    """   
    
    # To store the data read from files.
    data = []
    
    # Get all the files in current directory with the extension used for the
    # data files.    
    data_files_full_path = [f for f in \
                            glob.glob(os.path.join(path, "*." + \
                                                   DATA_FILE_EXT))]
    
    # Process the files that could contain data.
    for data_file_name in data_files_full_path:
        
        logging.debug('Reading file: ' + data_file_name)
    
        this_data = np.array([])
    
        # Read from file as text lines.
        with open(data_file_name) as f:
            # Process each line of the file.
            for line in f:                
                this_data = np.append(this_data, line)
            
            # Check if the data read is valid.
            data_read = data_is_valid(this_data)
            
            if data_read <> None:
                logging.debug('Data is valid from file: ' + data_file_name)
                
                # In that case add the data read to the list of data 
                # to return.
                data.append(data_read)
            else:
                logging.warning('Data is not valid from file: ' + \
                                data_file_name)     
    return data
 
def interpolate_sky_measures(initial_values):
    """ Interpolate for the values received.
    
    The values received are all the measures taken from the sky at some azimuth
    and zenith values.
    The order of the values is first all the measures of 0 degrees, staring at
    lowest azimuth, second all the measures of 30 degrees and so on.
    This function first interpolates for all the values of each azimuth from 
    first zenith value to the last one. This is, first it interpolates for 
    values at 0 degrees, second it interpolates for values at 30 degrees and so 
    on.
    At last the function interpolates from 0 to 360 for each zenith value. 
    
    Args:
        initial_values - The values to interpolate.
        
    Returns:
        The interpolated values.
        
    """    
    
    # Array to store all the interpolations made for the zenith values of
    # each azimuth.
    interp_zeniths = np.array([])
    
    i = 0
    
    zeniths_length = len(ALL_ZENITH_VALUES)
    
    # Interpolate for each azimuth.
    while i < len(initial_values):
        
        yp = initial_values[i:i+len(ZENITHS)]
        
        int = np.interp(ALL_ZENITH_VALUES, ZENITHS, yp)
        
        interp_zeniths = np.append(interp_zeniths, int)
                
        # Next interpolation begins after all zenith values at current azimuth.
        i = i + len(ZENITHS)
    
    all_azimuths = np.array([])
        
    # Interpolates at all zenith values.
    for i in range(len(ALL_ZENITH_VALUES)):
        
        values_at_zenith = np.array([])
        
        # Build a list of all the measurements at a given azimuth.
        for j in range(len(AZIMUTHS)):
            
            index = i + len(ALL_ZENITH_VALUES) * j
 
            values_at_zenith = np.append(values_at_zenith, \
                                         [interp_zeniths[index]])
                
        # Interpolate for all the azimuths and remove the last value as it is
        # a repetition of the first value.
        int = np.interp(AZIMUTH_RANGE, AZIMUTHS, values_at_zenith)[:-1]
        
        # Add the interpolated value to the list.
        all_azimuths = np.append(all_azimuths, int)
        
    return all_azimuths
 

def prepare_interp_measures(interp_measures):
    """ Perform some manipulations on interpolated values necessary to get a
        good polar plot.
 
    Args:
        interp_measures - The interpolated values of the measures.
        
    Returns:
        azimuths - A list with all the azimuth values used.
        interp_measures - The prepared interpolated measures.
 
    """
        
    # Add to the end the values at 0 degrees to have those same values at 360.
    interp_measures = np.append(interp_measures, interp_measures[:71])
    
    # Get azimuths and convert degrees to radians.
    azimuths = np.radians(AZIMUTH_RANGE)
    
    # Reshape array using Fortran style (first index changing fast), as the
    # order of the interpolated values is by azimuths.
    interp_measures = interp_measures.reshape(len(azimuths), \
                                              len(ALL_ZENITH_VALUES_INV), \
                                              order='F')
    
    # Set the same values at 0 and 360 degrees to avoid jumps in the plot on
    # this azimuth.
    interp_measures[-1] = interp_measures[0]
    
    return azimuths, interp_measures

def plot_polar(title, initial_values, progargs):
    """ Plot a polar plot with values received.
 
    Args:
        initial_values - The values to interpolate.
        title - The title of the figure to plot.
        progargs - program arguments. 
        
    Returns:
        None.
 
    """
    
    logging.debug('Plotting figure for: ' + title)
    
    # Get interpolated values for all zenith and azimuths ranges from the
    # intervals of the original data.
    interp_measures = interpolate_sky_measures(initial_values)
    
    azimuths, interp_measures = prepare_interp_measures(interp_measures)    
    
    # Chose a polar plot.
    fig, ax = subplots(subplot_kw=dict(projection='polar'))
    
   # Set the values of the grids.
    ax.set_rgrids(ALL_ZENITH_VALUES_INV, alpha=GRIDS_ALPHA)

    # Get coordinates for both axis.
    r, theta = np.meshgrid(ALL_ZENITH_VALUES_INV, azimuths)

    # Polar plot ticks.
    ax.set_yticks(Y_TICKS_RANGE)
    ax.set_yticklabels(map(str, Y_TICKS_RANGE))
    ax.set_xticklabels(X_TICKS_LABELS)

    # Where zero degrees are.
    ax.set_theta_zero_location('N')

    # Direction for degrees.
    ax.set_theta_direction(COUNTERCLOCKWISE_DIRECTION)

    # Set the figure title.
    title_processed = re.sub('[\t\n]', ' ', title)
    ax.set_title(title_processed, x=TITLE_X_POS, y=TITLE_Y_POS)

    # Set color map for plot.
    set_cmap(COLORMAP_NAME)
    
    # Contours.
    cax = ax.contour(theta, r, interp_measures, CONTOUR_LINES_DISTANCE, \
                     linewidths=CONTOUR_LINE_WIDTH, colors='k', \
                     alplha=CONTOUR_ALPHA)
    
    clabel(cax, inline=True, fmt='%.1f', fontsize=CONTOUR_FONT_SIZE, \
           rightside_up=True)

    # Check if the data range should be used for the color range.
    if not progargs.use_data_for_color_range:
        # Set fixed minimum and maximum dark values to plot all the figures
        # with the same range of colors.
        interp_measures[0][0] = LIGHTEST_VALUE
        interp_measures[-1][-1] = DARKER_VALUE
    
    cax = ax.contourf(theta, r, interp_measures, COLORBAR_THICKNESS)
    cb = fig.colorbar(cax, shrink=COLORBAR_SHRINK, pad=COLORBAR_PAD)
    cb.set_label(COLORBAR_LABEL)
    
    show()
    
def main(progargs):
    """ Main function.
    
    Call the functions to read the data files and get polar plots from the 
    the data read.

    """    
        
    # Process program arguments.
    progargs.parse()           
        
    # Initializes logging.
    init_log(progargs)    
    
    define_color_map()
    
    data = read_data_files(progargs.data_files_path)

    for i in range(len(data)):
        
        data_item = data[i]
        
        # Plot polar graph.
        plot_polar(data_item[DATA_LIST_TITLE], 
                   data_item[DATA_LIST_DATA],
                   progargs)
    
    logging.debug('Program finished.')

# Where all begins ...
if __name__ == "__main__":
    
    # Create object to process program arguments.
    progargs = pargparser.ProgramArguments() 
    
    # If no arguments are provided, show help and exit.
    if len(sys.argv) <= pargparser.ProgramArguments.MIN_NUM_ARGVS:
        print 'The number of program arguments are not enough.'       
        progargs.print_help()
        sys.exit(1)
    else: 
        sys.exit(main(progargs))        