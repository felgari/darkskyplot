#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Felipe Gallego. All rights reserved.
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

"""Process the program arguments received by main function.

Define the arguments available, check for its correctness, and provides 
these arguments to other modules. 
"""

import argparse
import os

class ProgramArguments(object):
    """ Encapsulates the definition and processing of program arguments. """
    
    MIN_NUM_ARGVS = 0
    
    def __init__(self):
        """ Initializes parser. 
        
        Initialization of variables and the object ProgramArguments 
        with the definition of arguments to use.

        """   
        
        # Initializes variables with default values.        
        self.__data_files_path = os.getcwd()
        self.__args = None                 
            
        # Creates the object that parses the program arguments.
        self.__parser = argparse.ArgumentParser()
        
        # Initiate arguments of the parser.
        self.__parser.add_argument("-p", dest="p", metavar="path", \
                                   help="Path of the data files.")
        
        self.__parser.add_argument("-s", dest="s", action="store_true", 
                                   help="Store figures to files.")     
        
        self.__parser.add_argument("-r", dest="r", action="store_true", 
                                   help="Use the own range of data for color.")                       
        
        self.__parser.add_argument("-l", metavar="log file name", dest="l", \
                                   help="File to save the log messages") 
        
        self.__parser.add_argument("-v", metavar="log level", dest="v", \
                                   help="Level of the log messages to generate")  
        
    @property    
    def data_files_path(self):        
        return self.__data_files_path
        
    @property
    def save_figures_to_file(self):
        return self.__args.s
    
    @property
    def use_data_for_color_range(self):
        return self.__args.r    
    
    @property    
    def log_file_provided(self): 
        return self.__args.l <> None
    
    @property
    def log_file_name(self):
        return self.__args.l       
    
    @property    
    def log_level_provided(self): 
        return self.__args.v <> None
    
    @property
    def log_level(self):
        return self.__args.v                     
    
    def parse(self):
        """ Parse program arguments.
        
        Performs the parsing of program arguments using the'ArgumentParser' 
        object created in __init__.
        
        """
        
        # Parse program arguments.
        self.__args = self.__parser.parse_args()
            
        # Update variables if a program argument has been received
        # for their values.
        if self.__args.p <> None:
            self.__data_files_path = self.__args.p    
            
    def print_usage(self):
        """ Print arguments options """
                
        self.__parser.print_usage()     
        
    def print_help(self):
        """ Print help for arguments options """
                
        self.__parser.print_help()           
     