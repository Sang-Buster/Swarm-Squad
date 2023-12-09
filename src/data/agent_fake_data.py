import pandas as pd
import sqlite3
import uuid
import random
import time

# Define the columns for the Agent List table
agent_columns = ['Agent Name', 'Agent ID', 'Agent Type', 'Status', 'Mode', 'Location', 'Alert Count']

while True:
    # Generate fake data for each column
    agent_name = range(1, 11)
    agent_id = [str(uuid.uuid4()) for _ in range(10)]
    agent_type = random.choices(['quadcopter', 'fixed-wing', 'vehicle', 'robots'], k=10)
    status = random.choices(['Connected', 'Disconnected'], k=10)
    mode = random.choices(['Manual', 'Autonomous'], k=10)   
    location = [f"{random.uniform(29.1863, 29.1940):.4f}, {random.uniform(-81.045, -81.053):.3f}" for _ in range(10)]
    error_count = random.choices(range(1, 10), k=10)

    # Create a dataframe
    agent_df = pd.DataFrame(list(zip(agent_name, agent_id, agent_type, status, mode, location, error_count)), columns=agent_columns)

    # Create a connection to the SQLite database
    # If the database does not exist, it will be created
    conn = sqlite3.connect('./src/data/swarmsquad.db')

    # Write the data to a table in the database
    agent_df.to_sql('agent', conn, if_exists='replace', index=False)

    # Close the connection to the database
    conn.close()

    print("Updated the database")

    # Pause for 1 second before the next update
    time.sleep(0.5)