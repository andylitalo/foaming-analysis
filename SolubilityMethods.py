# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:38:57 2019

@author: Andy
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import root


def m2p_v360(m_co2, m_poly, rho_poly=1.084, V=240, p0=30E5):
    """
    Converts the mass of carbon dioxide (dry ice) in the Parr reactor to the
    expected pressure based on solubility in the polyol, VORANOL 360.
    
    m_co2 : mass of dry ice upon sealing Parr reactor [g]
    m_poly : mass of polyol, VORANOL 360 [g]
    rho_poly : density of polyol, VORANOL 360 [g/mL]
    V : available internal volume of Parr reactor [mL]
    p0 : initial guess of pressure for nonlinear solver (~expected pressure) [Pa]
    
    returns : 
        pressure expected based on mass of CO2 [Pa]
    """
    # volume of polyol [mL]
    V_poly = m_poly / rho_poly
    # volume of gaseous head space [mL]
    V_gas = V - V_poly
    
    # interpolation functions
    f_sol = interpolate_dow_solubility()
    f_rho = interpolate_rho_co2()
    
    # equation to solve for pressure
    def fun(p, m_co2=m_co2, f_rho=f_rho, V_gas=V_gas, m_poly=m_poly, f_sol=f_sol):
        """
        Function to solve to determine pressure.
        """
        return m_co2 - f_rho(p)*V_gas - m_poly*f_sol(p)

    result = root(fun, p0)
    p = result.x
    
    print('Mass in gas phase = %.2f g.' % (f_rho(p)*V_gas))
    print('Mass in liquid phase = %.2f g.' % (f_sol(p)*m_poly))
    
    return p
    
    
def interpolate_dow_solubility(p=None):
    """
    Returns an interpolation function for the solubilty of VORANOL 360 at 25 C
    in terms of weight fraction as a function of the pressure in Pascals.
    Will perform the interpolation if an input pressure p is given.
    """
    # constants
    psi2pa = 1E5/14.5
    
    # copy-paste data from file "co2_solubility_pressures.xlsx"
    data = np.array([[0,0],
            [198.1, 0.0372],
            [405.6, 0.0821],
            [606.1, 0.1351],
            [806.8, 0.1993],
            [893.9, 0.2336]])
    # temperature [K]
    T = 298
    
    # first column is pressure in psia
    p_data_psia = data[:,0]
    # second column is solubility in fraction w/w
    solubility_data = data[:,1]
    
    # convert pressure to Pa
    p_data_pa = psi2pa * p_data_psia
    
    # define interpolation function
    f_sol = interp1d(p_data_pa, solubility_data, kind="cubic")
    
    if p:
        return f_sol(p)
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
    #pressure in Pa
    p_co2_pa = 1E5*np.arange(0,75,5)
    # density in g/mL (at 25 C)
    rho_co2 = np.array([0, 9.11, 18.725, 29.265, 39.805, 51.995, 64.185, 78.905, 
                            93.625, 112.9625, 132.3, 151.9, 258.4, 737.5, 700.95])/1000
    f_rho = interp1d(p_co2_pa, rho_co2, kind="cubic")
    
    if p:
        return f_rho(p)
    else:
        return f_rho
    
def interpolate_eos_co2(quantity, value=None):
    """
    Returns an interpolation function for the density of carbon dioxide
    according to the equation of state (return_p=False) (data taken from 
    http://www.peacesoftware.de/einigewerte/co2_e.html) at 25 C or the pressure
    given the density (return_p=True)
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
        
    # determine what to return
    if value==None:
        return f
    else:
        return f(value)
    
    
    