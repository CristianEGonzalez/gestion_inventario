import sqlite3

class Inventory:
    def __init__(self, db_path="inventory.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
            """)

    def add_product(self, name, price, stock):
        with self.conn:
            self.conn.execute("INSERT INTO inventory (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))

    def delete_product(self, name):
        with self.conn:
            self.conn.execute("DELETE FROM inventory WHERE name = ?", (name,))

    def modify_stock(self, name, new_stock):
        with self.conn:
            self.conn.execute("UPDATE inventory SET stock = ? WHERE name = ?", (new_stock, name))
    
    def low_stock_report(self):
        with self.conn:
            low_stock = self.conn.execute("SELECT * FROM inventory WHERE stock < 5").fetchall()
            return low_stock
            
    def modify_price(self, name, new_price):
        with self.conn:
            self.conn.execute("UPDATE inventory SET price = ? WHERE name = ?", (new_price, name))
            
    def calculate_total_value(self):
        with self.conn:
            inventory = self.conn.execute("SELECT * FROM inventory").fetchall()
            total_value = 0
            for product in inventory:
                total_value += product[2] * product[3]
            return total_value


    def search_product(self, search_term):
        results = self.conn.execute("SELECT * FROM inventory WHERE name LIKE ?", (f"%{search_term}%",)).fetchall()
        return results
    
    def exist_product(self, name):
        result = self.conn.execute("SELECT * FROM inventory WHERE name = ?", (name,)).fetchone()
        return result

    def show_inventory(self):
        inventory = self.conn.execute("SELECT * FROM inventory").fetchall()
        return inventory

    def sort_by(self, type):
        sorted_inventory = self.conn.execute("SELECT * FROM inventory ORDER BY " + type).fetchall()
        return sorted_inventory

