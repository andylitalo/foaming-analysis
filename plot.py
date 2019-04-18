# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:47:57 2019

@author: Andy
"""

import matplotlib.pyplot as plt


def plot_p_T_vs_t(p, T, t, log_t=False, t_lim=None, save_plot=False,
                  save_path='', title='CO2(s) + Voranol 360 in Parr Reactor',
                  lw=2, ax_fs=18, t_fs=20, tk_fs=14, colors=['k','b'], line_styles=['-','--']):
    """
    Plots pressure and temperature on same plot as a function of time.
    Different vertical axes are used to keep pressure and temperature on similar scales.
    """
    # create plot
    fig, ax1 = plt.subplots()
    # plot vs. log time ?
    if log_t:
        ax1.semilogx(t, p, line_styles[0], label='p', color=colors[0], linewidth=lw)
    else:
        ax1.plot(t, p, line_styles[0], label='p', color=colors[0], linewidth=lw)
    # labels
    ax1.set_xlabel('time (s)', fontsize=ax_fs)
    ax1.set_ylabel('pressure (psi)', color=colors[0], fontsize=ax_fs)
    ax1.tick_params('y', colors=colors[0])
    ax1.set_title(title, fontsize=t_fs)

    # separate axis for temperature
    ax2 = ax1.twinx()
    # plot vs. log time ?
    if log_t:
        ax2.semilogx(t, T, line_styles[1], label='T', color=colors[1], linewidth=lw)
    else:
        ax2.plot(t, T, line_styles[1], label='T', color=colors[1], linewidth=lw)
    # labels
    ax2.set_ylabel('temperature (C)', color=colors[1], fontsize=ax_fs)
    ax2.tick_params('y', colors=colors[1])

    # set axis limits ?
    if t_lim is not None:
        plt.xlim(t_lim)
    # increase font size of tick labels
    ax1.tick_params(axis='both', which='major', labelsize=tk_fs)
    ax2.tick_params(axis='y', which='major', labelsize=tk_fs)
    fig.tight_layout()

    # save plot ?
    if save_plot:
        plt.savefig(save_path, bbox_inches="tight")

def plot_p_vs_t(p, t, log_t=False, log_p=False, p_lim=None, t_lim=None, save_plot=False,
                  save_path='', title='Pressure over Time: Voranol 360 w CO2',
                ms=4, ax_fs=18, t_fs=20, tk_fs=14, color='b'):
    fig, ax = plt.subplots()
    # logarithmic axes ?
    if log_t and log_p:
        ax.loglog(t, p, '.', color=color, markersize=ms)
    elif log_t:
        ax.semilogx(t, p, '.', color=color, markersize=ms)
    elif log_p:
        ax.semilogy(t, p, '.', color=color, markersize=ms)
    else:
        ax.plot(t, p, '.', color=color, markersize=ms)
    ax.set_xlabel('time (s)', fontsize=ax_fs)
    ax.set_ylabel('pressure (psi)', fontsize=ax_fs)
    ax.set_title(title, fontsize=t_fs)
    # limit viewing window ?
    if p_lim is not None:
        plt.ylim(p_lim)
    if t_lim is not None:
        plt.xlim(t_lim)
    # increase font size of tick labels
    ax.tick_params(axis='both', which='major', labelsize=tk_fs)
    fig.tight_layout()

    # save plot ?
    if save_plot:
        plt.savefig(save_path, bbox_inches="tight")

    return ax
