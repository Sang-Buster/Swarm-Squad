import sqlite3


def agent_tbl_writer(df):
    # Write the data to the SQLite database
    conn = sqlite3.connect("./src/data/swarm_squad.db")
    df.to_sql("agent", conn, if_exists="replace", index=False)
    conn.close()

    print("Updated the agent table in the database")
