import psycopg2
from psycopg2 import sql

class PlayerDatabase:

    def __init__(self):
        self.connection_params = {
            'dbname': 'photon',
            'user': 'student',
            #'password': 'student',
            #'host': 'localhost',
            #'port': '5432'
        }

    def connect(self):
        return psycopg2.connect(**self.connection_params)

    def get_players(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players;")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_player(self, player_id, codename):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
            conn.commit()
            print(f"Added player {codename} with ID {player_id}")
        except Exception as e:
            print(f"Error inserting player: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
# example of main for when ran on main 
# if __name__ == "__main__":
#     db = PlayerDatabase()  # Create a database instance
#     db.add_player(503, "NightHawk")  # Add a player
#     players = db.get_players()  # Fetch players
#     for player in players:
#         print(player)