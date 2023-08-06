# db.py
import sqlite3
from sqlite3 import Error
import os

class SessionDB:
    def __init__(self, db_file):
        #self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_table()
        except Error as e:
            print(e)

    def create_table(self):
        try:
            self.conn.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, model TEXT NOT NULL)")
        except Error as e:
            print(e)

    def create_session(self, session_name, model):
        # Insert a new session into the sessions table
        # At this point we don't yet have the API_ID, so we'll insert NULL for now
        self.cursor.execute(
            """
            INSERT INTO sessions (SessionName, API_ID, Model)
            VALUES (?, NULL, ?)
            """,
            (session_name, model)
        )
        self.connection.commit()
        
        # Return the ID of the new session
        return self.cursor.lastrowid  
    
    def update_session(self, id, api_id):
        # Update the API_ID of the session with the given id
        self.cursor.execute(
            """
            UPDATE sessions
            SET API_ID = ?
            WHERE ID = ?
            """,
            (api_id, id)
        )
        self.connection.commit()
        
    def get_session(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id=?", (session_id,))
        return cursor.fetchone()

    def get_all_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions")
        return cursor.fetchall()

    def delete_session(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()