To run the simulation using different configurations as mentioned in report, 
change the values directly in the config.py file which is imported and save it.
    Change 1:   P_TX_W = 20
                num_of_users_list = [1000, 1100, 1200, 1300, 1400, 1500, 1600]
    Change 2:   Do changes mentioned in Change 1.
                Antenna_h_Tx = 40
    Change 3:   Do changes mentioned in Change 2.
                Total_Channel_Count = 60
    Change 4:   On top of baseline config,
                Antenna_Gain_Tx = 12
    Change 5:   On top of baseline config,
                cell_radius_km = 1.2


Create a virtual environment using below command after opening the project folder:
    For macOS
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    For Linux:
        Use same as macOS
    For Windows:
        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt

If requirements.txt is not installed, enter below command:
    pip install -r requirements.txt

To run the program, enter below command:
    python3 main.py
