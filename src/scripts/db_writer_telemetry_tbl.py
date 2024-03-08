import sqlite3

def telemetry_tbl_writer(df):
    # Write the data to the SQLite database
    conn = sqlite3.connect('./src/data/swarm_squad.db')
    df.to_sql('telemetry', conn, if_exists='replace', index=False)
    conn.close()

    print("Updated the telemetry table in the database")