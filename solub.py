# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:38:57 2019

@author: Andy
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import root


def m2p_co2_polyol(m_co2, m_polyol, rho_polyol=1.084, V=240, p0=30E5,
                   polyol_name='VORANOL 360'):
    """
    Converts the mass of carbon dioxide (dry ice) in the Parr reactor to the
    expected pressure based on solubility in the polyol, VORANOL 360.

    m_co2 : mass of dry ice upon sealing Parr reactor [g]
    m_polypl : mass of polyol, VORANOL 360 [g]
    rho_polyol : density of polyol, VORANOL 360 [g/mL]
    V : available internal volume of Parr reactor [mL]
    p0 : initial guess of pressure for nonlinear solver (~expected pressure) [Pa]

    returns :
        pressure expected based on mass of CO2 [Pa]
    """
    # volume of polyol [mL]
    V_polyol = m_polyol / rho_polyol
    # volume of gaseous head space [mL]
    V_gas = V - V_polyol

    # interpolation functions
    f_sol = interpolate_dow_solubility(polyol_name)
    f_rho = interpolate_rho_co2()

    # equation to solve for pressure
    def fun(p, m_co2=m_co2, f_rho=f_rho, V_gas=V_gas, m_polyol=m_polyol, 
            f_sol=f_sol):
        """
        Function to solve to determine pressure.
        """
        return m_co2 - f_rho(p)*V_gas - m_polyol*f_sol(p)

    result = root(fun, p0)
    p = result.x

    print('Mass in gas phase = %.2f g.' % (f_rho(p)*V_gas))
    print('Mass in liquid phase = %.2f g.' % (f_sol(p)*m_polyol))

    return p


def p2m_co2_polyol(p, m_polyol, rho_polyol=1.084, polyol_name='VORANOL 360',
                   V=240, m0=20):
    """
    Computes the required mass of dry ice (CO2) to add to a Parr reactor of 
    volume V with a given mass of polyol to reach the desired pressure based on
    the solubility data of CO2 in this polyol.
    
    Parameters:
        p : int
            Desired final pressure in Parr reactor [bar]
        m_polyol : int
            Mass of polyol [g]
        rho_polyol : int, default 1.084
            Density of polyol [g/mL]
        polyol_name : string, default 'VORANOL 360'
            Name of the polyol (for loading corresponding solubility data)
        V : int, default 240
            Volume of Parr reactor [mL]
        m0 : int, default 20
            Initial guess for dry ice mass [g]
            
    Returns:
        m : int
            Mass of dry ice required to achieve desired pressure [g]
    """
    # volume of polyol [mL]
    V_polyol = m_polyol / rho_polyol
    # volume of gaseous head space [mL]
    V_co2_gas = V - V_polyol
    # Interpolate density of CO2 at given pressure [g/mL] and 25 C
    rho_co2 = interpolate_rho_co2(p=p)
    # Mass of CO2 in gas phase [g]
    m_co2_gas = rho_co2 * V_co2_gas
    # Interpolate weight fraction of CO2 based on Dow solubility data
    w_co2 = interpolate_dow_solubility(polyol_name, p=p)
    # Calculate mass of CO2 dissolved in polyol [g]
    m_co2_dissolved = w_co2 * m_polyol
    # Total mass [g]
    m = m_co2_gas + m_co2_dissolved
    
    print('Mass in gas phase = %.2f g.' % (m_co2_gas))
    print('Mass in liquid phase = %.2f g.' % (m_co2_dissolved))

    return m

    
def interpolate_dow_solubility(polyol_name='VORANOL 360', p=None):
    """
    Returns an interpolation function for the solubilty of VORANOL 360 at 25 C
    in terms of weight fraction as a function of the pressure in bar.
    Will perform the interpolation if an input pressure p is given.
    
    Parameters:
        polyol_name : string, default 'VORANOL 360'
            Name of polyol, used to load corresponding solubility data
        p : int, default None
            Pressure at which solubility is desired to be interpolated
    
    Returns:
        if pressure 'p' not provided (p=None, default):
            f_sol : interpolation function
                Function to interpolate weight fraction solubility given pressure in bar
        else if pressure 'p' provided:
            f_sol(p) : int
                Weight fraction solubility of CO2 in polyol at pressure p [bar]
    """
    # constants
    psi2pa = 1E5/14.5
    
    # copy-paste data from file "co2_solubility_pressures.xlsx" for VORANOL 360
    if polyol_name == 'VORANOL 360':
        data = np.array([[0,0],
            [198.1, 0.0372],
            [405.6, 0.0821],
            [606.1, 0.1351],
            [806.8, 0.1993],
            [893.9, 0.2336]])
    else: 
        print("Data for polyol not found. Ending calculation.")
        return
    # first column is pressure in psia
    p_data_psia = data[:,0]
    # second column is solubility in fraction w/w
    solubility_data = data[:,1]
    # convert pressure to Pa
    p_data_pa = psi2pa * p_data_psia
    # define interpolation function
    f_sol = interp1d(p_data_pa, solubility_data, kind="cubic")

    # Return weight fraction if pressure p provided
    if p:
        # convert pressure to Pascals
        p *= 1E5
        return f_sol(p)
    # Otherwise, return interpolation function for weight fraction vs. pressure
    else:
        return f_sol
    

def interpolate_rho_co2(p=None):
    """
    Returns an interpolation function for the density of carbon dioxide
    according to the equation of state (data taken from
    http://www.peacesoftware.de/einigewerte/co2_e.html) at 25 C.
    The density is returned in term of g/mL as a function of pressure in Pascals.
    Will perform the interpolation if an input pressure p is given.
    """

    p_co2_pa = 1E5*np.arange(0,75,5)
    # density in g/mL (at 25 C)
    rho_co2 = np.array([0, 9.11, 18.725, 29.265, 39.805, 51.995, 64.185, 78.905,
                            93.625, 112.9625, 132.3, 151.9, 258.4, 737.5, 700.95])/1000
    f_rho = interp1d(p_co2_pa, rho_co2, kind="cubic")

    if p:
        #pressure in Pa
        p *= 1E5
        return f_rho(p)
    else:
        return f_rho

def interpolate_eos_co2(quantity, value=None):
    """
    Returns an interpolation function for the density of carbon dioxide
    according to the equation of state (return_p=False) (data taken from
    http://www.peacesoftware.de/einigewerte/co2_e.html) at 25 C or the pressure
    given the density (if a value is given).
    The density is returned in term of g/mL as a function of pressure in Pascals,
    and the pressure is returned in terms of Pascals given density in terms of
    g/mL.
    Will perform the interpolation if a given value is given.
    """
    #pressure in Pa
    p_co2_pa = 1E5*np.arange(0,75,5)
    # density in g/mL (at 25 C)
    rho_co2 = np.array([0, 9.11, 18.725, 29.265, 39.805, 51.995, 64.185, 78.905,
                            93.625, 112.9625, 132.3, 151.9, 258.4, 737.5, 700.95])/1000

    # determine appropriate interpolation function
    if quantity=='p':
        f = interp1d(rho_co2, p_co2_pa, kind="cubic")
    elif quantity=='rho':
        f = interp1d(p_co2_pa, rho_co2, kind="cubic")
    else:
        print("please select a valid quantity: ''rho'' or ''p''")

    # Return the interpolation function
    if value==None:
        return f
    # Otherwise return the corresponding quantity given a value for the input
    else:
        return f(value)

def usb_2_actual_pressure(p_usb, lo_usb=-3, hi_usb=639, lo_cpu=1, hi_cpu=655, cpu2actual=1/0.895):
    """
    Converts pressure read during usb powering with Samsung 5V 2.0 A USB wall adapter to
    predicted actual pressure based on empirical measurements, particularly on pp. 45 and 51
    """
    p_cpu = (hi_cpu-lo_cpu)/(hi_usb-lo_usb)*p_usb + (lo_cpu-lo_usb)
    p_actual = cpu2actual * p_cpu

    return p_actual

def dc_2_actual_pressure(p_dc, p_lo=0, p_hi=1500, cts_lo=207, cts_hi=1023, cts_lo_actual=208, cts_hi_actual=914):
    """
    Converts pressure read during DC powering with
    predicted actual pressure based on empirical measurements based on calibration on pp. 64-65.
    """
    cts = (cts_hi-cts_lo)*(p_dc-p_lo)/(p_hi-p_lo) + cts_lo
    p_actual = (p_hi-p_lo)*(cts-cts_lo_actual)/(cts_hi_actual-cts_lo_actual) + p_lo

    return p_actual
