# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 11:47:30 2019

@author: Andy
"""

import numpy as np


def get_flow_rates_fixed_speed(d_inner, v_center=1.0, ID=500):
    """
    Computes the flow rates of inner and outer streams given the width of the
    inner stream (d_inner) in um, the velocity at the center of the stream
    (v_center) in m/s, and the inner diameter (ID)in um of the channel.

    Assumes Newtonian fluid and same viscosities for inner and outer streams.

    returns:
        Q_i = flow rate of inner stream in mL/min
        Q_o = flow rate of outer stream in mL/min
    """
    # convert to SI
    R_i_m = d_inner/2/1E6
    R_m = ID/2/1E6

    # compute flow rates
    Q_i_m3s = np.pi*v_center*R_i_m**2*(1-0.5*(R_i_m/R_m)**2)
    Q_o_m3s = 0.5*np.pi*v_center*R_m**2 - Q_i_m3s

    # convert units to mL/min
    Q_i = Q_i_m3s*60E6
    Q_o = Q_o_m3s*60E6

    return Q_i, Q_o

def get_flow_rates(eta, p_i=None, Q_i=None, p_o=None, Q_o=None, l_obs_cap=10,
    r_obs_cap=250, l_inner_cap=2.3, r_inner_cap=280, l_tube_i=20,
    r_tube_i=481.25, l_tube_o=20, r_tube_o=481.25):
    """
    Gives flow rates for inner and outer streams given system parameters.
    Assumes uniform viscosity, Newtonian fluids, and outlet to atmospheric
    pressure.

    Equations were solved using Mathematica, the results of which can be found
    in the file "flow_p_q_eqns" in the same folder as this file ("Calculations").

    inputs:
        eta         :   viscosity of fluid [Pa.s]
        p_i         :   pressure at inner stream source [bar]
        Q_i         :   flow rate of inner stream [uL/min]
        p_o         :   pressure at outer stream source [bar]
        Q_o         :   flow rate of outer stream [uL/min]
        l_obs_cap   :   length of observation capillary [cm]
        r_obs_cap   :   inner radius of observation capillary [um]
        l_inner_cap :   length of inner capillary [cm]
        r_inner_cap :   inner radius of inner capillary [um]
        l_tube_i    :   length of tubing for inner stream (source to inner
                            capillary) [cm]
        r_tube_i    :   inner radius of tubing for inner stream
        l_tube_o    :   length of tubing for outer stream (source to
                            microfluidic device/acrylic block) [cm]
        r_tube_o    :   inner radius of tubing for outer stream [um]

    returns:
        Q_i         :   flow rate of inner stream [uL/min]
        Q_o         :   flow rate of outer stream [uL/min]
    """
    # ensure that only one of pressure or flow rate is given
    assert (p_i is None) != (Q_i is None), "Provide only one: p_i or Q_i."
    assert (p_o is None) != (Q_o is None), "Provide only one: p_o or Q_o."

    # CONVERT TO SI
    l_obs_cap /= 100 # cm -> m
    r_obs_cap /= 1E6 # um -> m
    l_inner_cap /= 100 # cm -> m
    r_inner_cap /= 1E6 # um -> m
    l_tube_i /= 100 # cm -> m
    r_tube_i /= 1E6 # um -> m
    l_tube_o /= 100 # cm -> m
    r_tube_o /= 1E6 # um -> m

    # inner and outer pressures given
    if (p_i is not None) and (p_o is not None):
        # CONVERT TO SI
        p_i *= 1E5 # bar -> Pa
        p_o *= 1E5 # bar -> Pa

        # Calculate flow rates
        num_Q_i = np.pi*r_tube_i**4*r_inner_cap**4*(l_obs_cap*(p_i - p_o)* \
                    r_tube_o**4 + l_tube_o*p_i*r_obs_cap**4)
        num_Q_o = np.pi*r_tube_o**4*(l_obs_cap*(p_o - p_i)*r_tube_i**4*\
                    r_inner_cap**4 + p_o*(l_inner_cap*r_tube_i**4 + \
                    l_tube_i*r_inner_cap**4)*r_obs_cap**4)
        denom = (8*eta*(l_inner_cap*r_tube_i**4* \
                (l_obs_cap*r_tube_o**4 + l_tube_o*r_obs_cap**4) + \
                r_inner_cap**4*(l_tube_o*l_obs_cap*r_tube_i**4 + \
                l_tube_i*l_obs_cap*r_tube_o**4 + \
                l_tube_i*l_tube_o*r_obs_cap**4)))
        Q_i = num_Q_i / denom
        Q_o = num_Q_i / denom

    # given inner stream pressure and outer stream flow rate
    elif (p_i is not None) and (Q_o is not None):
        # CONVERT TO SI
        p_i *= 1E5
        Q_o /= 60E9

        # calculate the flow rate of the inner stream [m^3/s]
        Q_i = (r_tube_i**4*r_inner_cap**4*(p_i*np.pi*r_obs_cap**4 - \
                8*l_obs_cap*Q_o*eta)) / \
                (8*eta*(l_obs_cap*r_tube_i**4*r_inner_cap**4 + \
                (l_inner_cap*r_tube_i**4 + l_tube_i*r_inner_cap**4)*r_obs_cap**4))

    # given inner stream flow rate and outer stream pressure
    elif (Q_i is not None) and (p_o is not None):
        # CONVERT TO SI
        Q_i /= 60E9
        p_o *= 1E5

        # calculate the flow rate of the outer stream [m^3/s]
        Q_o = (p_o*np.pi*r_tube_o**4 - 8*eta*l_obs_cap*(r_tube_o/r_obs_cap)**4*Q_i) / \
                (8*eta*(l_obs_cap*(r_tube_o/r_obs_cap)**4 + l_tube_o))

    elif (Q_i is not None) and (Q_o is not None):
        # CONVERT TO SI
        Q_i /= 60E9
        Q_o /= 60E9
    else:
        error("if statements failed to elicit a true response.")

    # CONVERT FROM M^3/S -> UL/MIN
    Q_i *= 60E9
    Q_o *= 60E9

    return Q_i, Q_o


def get_pressures(eta, Q_i, Q_o, l_obs_cap=10,
    r_obs_cap=250, l_inner_cap=2.3, r_inner_cap=280, l_tube_i=20,
    r_tube_i=481.25, l_tube_o=20, r_tube_o=481.25):
    """
    inputs:
        eta         :   viscosity of fluid [Pa.s]
        Q_i         :   flow rate of inner stream [uL/min]
        Q_o         :   flow rate of outer stream [uL/min]
        l_obs_cap   :   length of observation capillary [cm]
        r_obs_cap   :   inner radius of observation capillary [um]
        l_inner_cap :   length of inner capillary [cm]
        r_inner_cap :   inner radius of inner capillary [um]
        l_tube_i    :   length of tubing for inner stream (source to inner
                            capillary) [cm]
        r_tube_i    :   inner radius of tubing for inner stream
        l_tube_o    :   length of tubing for outer stream (source to
                            microfluidic device/acrylic block) [cm]
        r_tube_o    :   inner radius of tubing for outer stream [um]

    returns:
        p_i         :   pressure at source of inner stream [bar]
        p_o         :   pressure at source of outer stream [bar]
        p_inner_cap :   pressure at inlet to inner capillary [bar]
        p_obs_cap   :   pressure at inlet to observation capillary [bar]
                                *assumes no pressure drop down microfluidic device
    """
    # CONVERT TO SI
    Q_i /= 60E9 # uL/min -> m^3/s
    Q_o /= 60E9 # uL/min -> m^3/s
    l_obs_cap /= 100 # cm -> m
    r_obs_cap /= 1E6 # um -> m
    l_inner_cap /= 100 # cm -> m
    r_inner_cap /= 1E6 # um -> m
    l_tube_i /= 100 # cm -> m
    r_tube_i /= 1E6 # um -> m
    l_tube_o /= 100 # cm -> m
    r_tube_o /= 1E6 # um -> m

    # compute pressures using Poiseuille flow pressure drop starting from end
    p_obs_cap = 8*eta*l_obs_cap/(np.pi*r_obs_cap**4)*(Q_i+Q_o)
    p_inner_cap = p_obs_cap + 8*eta*l_inner_cap/(np.pi*r_inner_cap**4)*Q_i
    p_o = p_obs_cap + 8*eta*l_tube_o/(np.pi*r_tube_o**4)*Q_o
    p_i = p_inner_cap + 8*eta*l_tube_i/(np.pi*r_tube_i**4)*Q_i

    # convert from Pa to bar
    p_obs_cap /= 1E5
    p_inner_cap /= 1E5
    p_o /= 1E5
    p_i /= 1E5

    return p_i, p_o, p_inner_cap, p_obs_cap


def get_inner_stream_radius(Q_i, Q_o, r_obs_cap=250):
    """
    Calculates the radius of the inner stream in the observation capillary given
    the flow rates of the inner and outer streams.

    Assumes Newtonian fluids with the same viscosity.

    inputs:
        Q_i         :   flow rate of inner stream [just must be same units as Q_o]
        Q_o         :   flow rate of outer stream [just must be same units as Q_i]
        r_obs_cap   :   inner radius of observation capillary [um]

    returns:
        r_inner_stream  :   radius of the inner stream [um]
    """
    # calculate inner stream using equation A.14 in candidacy report
    r_inner_stream = r_obs_cap*np.sqrt(1 - np.sqrt(Q_o/(Q_i + Q_o)))

    return r_inner_stream

def get_velocity(Q_i, Q_o, r_obs_cap=250):
    """
    Calculates the velocity at the center of the inner stream given the flow
    rates.

    inputs:
        Q_i         :   flow rate of inner stream [uL/min]
        Q_o         :   flow rate of outer stream [uL/min]
        r_obs_cap   :   inner radius of observation capilary [um]

    returns:
        v_center    :   velocity at center of inner stream [m/s]
    """
    # CONVERT TO SI
    Q_i /= 60E9 # uL/min -> m^3/s
    Q_o /= 60E9 # uL/min -> m^3/s
    r_obs_cap /= 1E6 # um -> m

    # maximum velocity in exit capillary [m/s]
    v_center = 2*(Q_o+Q_i)/(np.pi*r_obs_cap**2)
    # convert m/s -> cm/s
    v_center *= 100

    return v_center

if __name__=='__main__':
    Q_i, Q_o = get_flow_rates_fixed_speed(20)

    print('Inner flow rate = %.4f mL/min and outer flow rate = %.2f mL/min' % (Q_i,Q_o))
