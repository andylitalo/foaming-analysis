# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:14:09 2019

Contains functions that are useful for image processing.

@author: Andy
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def proc_im_seq(im_path_list, proc_fn, columns):
    """
    Processes a sequence of images with the given function and returns the
    results. Images are provided as filepaths to images, which are loaded (and
    possibly copied before analysis to preserve the image).
    
    Parameters:
        im_path_list : array-like
            Sequence of filepaths to the images to be processed
        proc_fn : function handle
            Handle of function to use to process image sequence
        columns : array-like
            Results from image processing are saved to this dataframe
    
    Returns:
        df : Pandas DataFrame
            Dataframe of results from image processing        
    """
    # Initialize dataframe of results from image processing
    num_ims = len(im_path_list)
    df = pd.DataFrame(index=np.arange(num_ims), columns=columns)

    # Process each image in sequence and save results.
    for i in range(num_ims):
        im = plt.imread(im_path_list[i])
        df.iloc[i] = proc_fn(im)
            
    return df
        

def compute_stream_width(im):
    """
    Computes the width of a stream of a darker color inside the image.
    
    Parameters:
        
    Returns:
        
    """
    # create 0-255 uint8 copy of image
    im_copy = (255*np.copy(im)).astype('uint8')
    # find edges by determining columns with most saturated (255) pixels
    left, right = IPF.get_edgeX(imCopy, channel=channel)

    # show edges to check that they were found properly
    if viewIms:
        IPF.show_im(imCopy[:,:left,:], 'left edge')
        IPF.show_im(imCopy[:,right:,:], 'right edge')
    
    #### MASKING ###
    imMasked = IPF.create_and_apply_mask(imCopy, 'rectangle', message=maskMsg)
    
    # show masked edges and mask to ensure they were determined properly
    if viewIms:
        IPF.show_im(imMasked[:,:left,:], 'left edge')
        IPF.show_im(imMasked[:,right:,:], 'right edge')
    if viewIms:
        IPF.show_im(mask, 'mask')
        
    # compute stream width and standard deviation 
    streamWidthMean, streamWidthStDev = IPF.calculate_stream_width(imMasked, left, right)