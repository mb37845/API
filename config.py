import sqlite3
import os
from dotenv import load_dotenv 

load_dotenv() 
 

def init_db():
    if os.path.exists(os.getenv("DATABASE_NAME")):
        return
    conn = sqlite3.connect(os.getenv("DATABASE_NAME"))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT , name VARCHAR(100) NOT NULL,email VARCHAR(200) NOT NULL,password VARCHAR(100) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS incomes (user_id int NOT NULL , source VARCHAR(100) NOT NULL, amount float NOT NULL, date DATE NOT NULL , FOREIGN KEY (user_id) REFERENCES users(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (user_id int NOT NULL , source VARCHAR(100) NOT NULL, amount float NOT NULL, date DATE NOT NULL , FOREIGN KEY (user_id) REFERENCES users(id))")
    conn.commit()
    conn.close()

