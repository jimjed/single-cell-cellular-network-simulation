import numpy as np
from config import *
from propagation_loss_functions import *

P_Tx_dBm = Watts_to_dBm(P_Tx_W) #dBm

#Shadowing + PL calculation
def static_loss_calculation(MS_radius, num_of_users):
    """
    Since shadowing and path loss are both static for a given location,
    they can be calculated once and used multiple times.
    Args:
        MS_radius (array): Distance of each MS from the BS in km.
        num_of_users (int): Number of users for whom calculation is done.
    """
    return (P_Tx_dBm - Feeder_loss_Tx + Antenna_Gain_Tx + Antenna_Gain_Rx -
            Orientation_loss_Rx - Path_loss_Hata(MS_radius) -
            Path_loss_shadowing(num_of_users))

#Call request generation function
def stats_for_one_position(P_Rx_static, num_of_users):
    """
    Simulates call requests, blocking and dropping for users at one position.
    Args:
        P_Rx_static (array): Static received power (shadowing+Hata loss) at each MS in dBm.
        num_of_users (int): Number of users at the position.
    Returns:
        tuple: (number of call requests generated,
                number of blocked calls due to channel unavailability,
                number of blocked calls due to insufficient signal,
                number of dropped calls,
                number of calls successfully started)
    """
    call_ongoing = np.zeros(num_of_users)
    #Calculating probability of call
    p_call = lambda_call_request_per_user_per_min * dt /60

    #Initialising parameters to capture call counts
    blocked_call_count_signal = blocked_call_count_channel = 0
    dropped_call_count = call_generate_count = call_started_count = 0
    Available_channel_count = Total_Channel_Count
    time_in_call = np.zeros(num_of_users)

    while call_generate_count < 200:
        """Simulating until 200 call requests are generated.
        This is to ensure sufficient number of call requests are generated
        for accurate statistics."""

        # Fading values is generated every iteration and new received power at MS is calculated
        P_Rx = P_Rx_static + Fading_effect(num_of_users)

        for i in range(num_of_users):        # Running loop through all users
            if call_ongoing[i]==0:                        #Check if call is on-going
                """
                Actions to be taken if user is idle:
                - Generate call request based on probability of call
                - If call request is generated, check if signal strength is sufficient
                  to start call
                - If signal strength is sufficient, check if channel is available
                  to start call
                - If both conditions are satisfied, start the call
                - If any of the conditions is not satisfied, mark call as blocked
                """
                if np.random.uniform(0,1) <= p_call:         #Check probability of call is satisfied
                    call_generate_count += 1              #increase the count of attempted calls
                    if P_Rx[i] >= P_Sensitivity:          #Check if user has enough signal strength to start call
                        if Available_channel_count > 0:
                            Available_channel_count -= 1  #Mark one channel as occupied for the call
                            call_ongoing[i] = 1           #Mark call is ongoing for the user
                            call_started_count+=1
                            time_in_call[i] = 0           #Reset timer to start tracking duration of call
                        else:
                            blocked_call_count_channel += 1      #Increase blocked call count if channels are not available for use
                    else:
                        blocked_call_count_signal += 1           #Increase blocked call count if signal strength is insufficient

            else:
                """
                Actions to be taken if user is in call:
                - Increment time in call
                - Check if received power is still above sensitivity
                  to continue the call
                - If received power is below sensitivity, drop the call
                - If call duration exceeds maximum call duration, disconnect the call
                """
                time_in_call[i] += dt                     #Increment time in call

                # Drop call if Rx power is lower than sensitivity
                if P_Rx[i] < P_Sensitivity:
                    call_ongoing[i] = 0
                    Available_channel_count += 1
                    dropped_call_count += 1

                #Disconnect call if max call duration is breached
                elif time_in_call[i] >= call_duration_min*60:
                    call_ongoing[i] = 0
                    Available_channel_count += 1
    return call_generate_count, blocked_call_count_channel, blocked_call_count_signal, dropped_call_count, call_started_count

#Calculates average of various call statistics for MS at various positions
def average_stats_for_multiple_positions(num_of_users):
    """
    Simulates call requests, blocking and dropping for users at multiple positions
    and returns average statistics.
    Args:    
        :param num_of_users: Number of users for whom calculation is done.
    """
    total_call_generate_count = total_blocked_call_count_channel = total_blocked_call_count_signal = total_dropped_call_count = total_call_started_count = 0
    for i in range(simulation_count):
        # Generate new position for users for use in this iteration
        MS_radius, MS_angle = MS_location_assignment(num_of_users)

        #Calculate received power without considering fading, for newly generated position of users
        P_Rx_static = static_loss_calculation(MS_radius, num_of_users)

        #This function returns call count stats after simulating calls for users at one position
        call_generate_count, blocked_call_count_channel, blocked_call_count_signal, dropped_call_count, call_started_count = stats_for_one_position(P_Rx_static, num_of_users)
        
        # Accumulating call stats over multiple positions
        total_call_generate_count += call_generate_count
        total_blocked_call_count_channel += blocked_call_count_channel
        total_blocked_call_count_signal += blocked_call_count_signal
        total_dropped_call_count += dropped_call_count
        total_call_started_count += call_started_count
    # Print average stats for the number of users    
    print(num_of_users, '\t\t', round(total_blocked_call_count_signal/total_call_generate_count, 3), '\t\t\t', round(total_blocked_call_count_channel/total_call_generate_count, 3), '\t\t\t', round((total_blocked_call_count_channel+total_blocked_call_count_signal)/total_call_started_count, 3), '\t\t', round(total_dropped_call_count/total_call_started_count, 3))
    
    return total_blocked_call_count_channel/total_call_generate_count, total_blocked_call_count_signal/total_call_generate_count, total_dropped_call_count/total_call_started_count
