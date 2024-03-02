import pandas as pd
import sqlite3
import random
import time

# Define the columns for the Telemetry Data table
telemetry_columns = ['Agent Name', 'Location', 'Destination', 'Altitude', 'Pitch', 'Yaw', 'Roll', 'Airspeed/Velocity', 'Acceleration', 'Angular Velocity']

while True:
    # Generate fake data for each column
    agent_name = range(1, 11)
    altitude = [round(random.uniform(0, 40), 3) for _ in range(10)]  # Altitude in meters
    location = [f"{random.uniform(-81.044, -81.052):.4f}, {random.uniform(29.187, 29.1940):.4f}, {altitude[i]}" for i in range(10)]
    destination = [f"{random.uniform(29.187, 29.1940):.4f}, {random.uniform(81.044, 81.052):.4f}, 50" for _ in range(10)]
    pitch = [random.randint(-180, 180) for _ in range(10)]
    yaw = [random.randint(-180, 180) for _ in range(10)]
    roll = [random.randint(-180, 180) for _ in range(10)]
    airspeed_velocity = [round(random.uniform(50, 200), 3) for _ in range(10)]  # Airspeed/Velocity in km/h
    acceleration = [round(random.uniform(0, 10), 3) for _ in range(10)]  # Acceleration in m/s^2
    angular_velocity = [round(random.uniform(-3.14, 3.14), 3) for _ in range(10)]  # Angular Velocity in rad/s
        
    # Create a dataframe
    telemetry_df = pd.DataFrame(list(zip(agent_name, location, destination, altitude, pitch, yaw, roll, airspeed_velocity, acceleration, angular_velocity)), columns=telemetry_columns)

    # Create a connection to the SQLite database
    # If the database does not exist, it will be created
    conn = sqlite3.connect('./src/data/swarm_squad.db')

    # Write the data to a table in the database
    telemetry_df.to_sql('telemetry', conn, if_exists='replace', index=False)

    # Close the connection to the database
    conn.close()

    print("Updated the database")

    # Pause for half second before the next update
    time.sleep(0.5)