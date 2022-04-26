import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def insert_cars(self, sql, carList):
        with self.conn:
            self.cursor.executemany(sql, carList)
            self.conn.commit()

    def check_car_stock(self, message):
        with self.conn:
            result = self.cursor.execute(f"SELECT * FROM almati WHERE model = '{message}' AND stock = 1").fetchall()
            return result

    def count_car_model(self, message):
        with self.conn:
            result = self.cursor.execute(f"SELECT * FROM almati WHERE model = '{message}'").fetchall()
            return result

    def set_in_stock(self, message):
        with self.conn:
            self.cursor.execute(f"UPDATE almati SET stock = 1 WHERE name = '{message}'")
            self.conn.commit()
        
    def set_out_of_stock(self, message):
        with self.conn:
            self.cursor.execute(f"UPDATE almati SET stock = 0 WHERE name = '{message}'")
            self.conn.commit()