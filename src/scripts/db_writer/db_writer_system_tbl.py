import sqlite3


def system_tbl_writer(df):
    # Write the data to the SQLite database
    conn = sqlite3.connect("./src/data/swarm_squad.db")
    df.to_sql("system", conn, if_exists="replace", index=False)
    conn.close()

    print("Updated the system table in the database")
