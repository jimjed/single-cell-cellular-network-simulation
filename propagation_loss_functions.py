import numpy as np
from config import *

# Converting Watts to dBm
def Watts_to_dBm(p_w):
    return 10*np.log10(p_w)+30

#Setting MSs at random places
def MS_location_assignment(num_of_users):
    """
    MS must be placed randomly in the area of circle around the base station.
    So random number is generated for square of r between 0.001 and 1 and then
    used to generate the distance r. Here 0.001 is used to avaoid log0 problem.
    Sqaure of r is used to ensure more even distribution on the area of circle.
    Args:
        num_of_users (int): Number of users for whom location is to be generated.
    Returns:
        tuple: (array of distances of each MS from BS in km,
                array of angles of each MS in radians)
    """
    return cell_radius_km * np.sqrt(np.random.uniform(0.001, 1, num_of_users)), 2 * np.pi * np.random.uniform(0, 1, num_of_users)

# Path loss calculation using Okumura-Hata Model for large cities
def Path_loss_Hata(MS_radius):
    """Standard Hata Model for urban areas.
    Args:
        MS_radius (array): Distance of each MS from the BS in km.
    """
    return (69.55+26.16*np.log10(carrier_f_MHz)-13.82*np.log10(Antenna_h_Tx)-
            3.2*(np.log10(11.75*Antenna_h_Rx))**2+4.97+
            (44.9-6.55*np.log10(Antenna_h_Tx))*np.log10(MS_radius))

# Calculation of shadowing. 
def Path_loss_shadowing(num_of_users):
   """
   Lognormal distribution in linear means normal distribution in dB.
   Generates and returns shadowing loss for num_of_users.
   """
   return np.random.normal(0, Shadowing_location_variability, size=num_of_users)

# Calculation of Fading effect.
def Fading_effect(num_of_users):
    """
    Generates and returns Rayleigh fading for num_of_users.
    Args:
        num_of_users (int): Number of users for whom fading value is generated.
    """
    fading_power_std = np.sqrt(Fading_amplitude_variance/2)
    x = np.random.normal(Fading_mean, fading_power_std, num_of_users)
    y = np.random.normal(Fading_mean, fading_power_std, num_of_users)
    fading_linear = np.abs(x+1j*y)
    # Adding zero protection
    fading_linear[fading_linear==0] = 1e-10
    return 20*np.log10(fading_linear)