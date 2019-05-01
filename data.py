# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:31:58 2019

Defines functions useful for loading, manipulating, and saving data and
metadata.

@author: Andy
"""

def get_filepaths(path, template):
    """
    Returns a list of filepaths to files inside the given folder that start 
    with the given header.
    
    Parameters:
        path : string
            Path to folder of files of interest
        template : string
            Template for file names, using "*" for varying parts of file name
    
    Returns:
        filepaths : list
            List of filepaths to the desired files
    """
    