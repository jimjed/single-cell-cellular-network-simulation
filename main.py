# Non-standard units are mentioned in variable name.
# For power unit, dB is to be considered
# unless mentioned otherwise in variable name.

import numpy as np
import matplotlib.pyplot as plt
from config import *
from propagation_loss_functions import *
from simulation_functions import *

# Variable to capture maximum number of users that can be served with given GoS
# value.
max_num_of_users = 0

p_blocked = []
p_dropped = []

print('\nSimulating for various number of users...\n')
print('User Count\tP(blocked:signal)\tP(blocked:channel)\tP(blocked)\tP(dropped)')

for num_of_users in num_of_users_list:
    """
    Simulates call requests, blocking and dropping for various number of users
    and captures probability of blocked and dropped calls."""
    p_bc, p_bs, p_d = average_stats_for_multiple_positions(num_of_users)
    p_blocked.append(p_bc+p_bs)
    p_dropped.append(p_d)

#Find max number of users for which GoS is satisfied
for i in range(len(p_blocked)):
    if p_blocked[i]<=GoS:
        max_num_of_users = num_of_users_list[i]

if max_num_of_users == 0:
    print('\nGiven GoS of', GoS, 'cannot be achieved with the given parameters.\n')
else:
    print('\nGiven system can provide GoS', GoS, 'for', max_num_of_users, 'users\n')

# Plotting results for probability of blocked calls vs. number of users
plt.figure(figsize=(10, 6))
plt.plot(num_of_users_list, p_blocked, color='red', marker='o', label='Probability of blocked calls')
plt.axhline(y=GoS, color='green', linestyle='--', label='GoS 0.02')
plt.xlabel('Number of users')
plt.ylabel('Probability')
plt.title('Probability of blocked calls vs. number of users')
plt.grid(True)
plt.legend()
plt.show()

# Plotting results for probability of dropped calls vs. number of users
plt.figure(figsize=(10, 6))
plt.plot(num_of_users_list, p_dropped, color='orange', marker='x', label='Probability of dropped calls')
plt.xlabel('Number of users')
plt.ylabel('Probability')
plt.title('Probability of dropped calls vs. number of users')
plt.grid(True)
plt.legend()
plt.show()