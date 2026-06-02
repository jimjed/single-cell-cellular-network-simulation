import numpy as np

#Possible number of users in the cell
#num_of_users_list = [1000, 1100, 1200, 1300, 1400, 1500, 1600]
num_of_users_list = [10, 20, 30, 40, 50]

#System parameters
cell_radius_km = 1.5 #km
carrier_f_MHz = 900 #MHz

#BS parameters
P_Tx_W = 10 #Watts
Feeder_loss_Tx = 4 #dB
Antenna_Gain_Tx = 8 #dB
Antenna_h_Tx = 30 #meters

#Call requests and channel parameters
lambda_call_request_per_user_per_min = 0.017 #request per min
call_duration_min = 3 #minutes
Total_Channel_Count = 50

#MS parameters
P_Sensitivity = -102 #dBm
Antenna_Gain_Rx = 3 #dB
Orientation_loss_Rx = 3 #dB
Antenna_h_Rx = 1.5 #meters

#Shadowing + Fading parameters
Shadowing_location_variability = 5
Fading_mean = 0
Fading_amplitude_variance = 1

#Simulation parameters
dt = 1 #second
GoS = 0.02 #2% Grade of Service
simulation_count = 10 #Number of simulations for each user count

# Variable to capture maximum number of users that can be served with given GoS
# value.
max_num_of_users = 0