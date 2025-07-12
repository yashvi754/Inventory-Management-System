# create_db.py

import sqlite3

def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()

    # Employee Table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee("
        "   eid TEXT PRIMARY KEY, "
        "   name TEXT, "
        "   email TEXT, "
        "   gender TEXT, "
        "   contact TEXT, "
        "   dob TEXT, "
        "   doj TEXT, "
        "   pass TEXT, "
        "   utype TEXT, "
        "   address TEXT, "
        "   salary TEXT"
        ")"
    )
    con.commit()

    # Supplier Table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS supplier("
        "   invoice INTEGER PRIMARY KEY AUTOINCREMENT, "
        "   name TEXT, "
        "   contact TEXT, "
        "   desc TEXT"
        ")"
    )
    con.commit()

    # Category Table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS category("
        "   cid INTEGER PRIMARY KEY AUTOINCREMENT, "
        "   name TEXT"
        ")"
    )
    con.commit()

    # Product Table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS product("
        "   pid INTEGER PRIMARY KEY AUTOINCREMENT,"
        "   Supplier TEXT,"
        "   Category TEXT,"
        "   name TEXT,"
        "   price TEXT,"
        "   qty TEXT,"
        "   status TEXT"
        ")"
    )
    con.commit()
    
    # Sales Table (NEW)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS sales("
        "   invoice INTEGER PRIMARY KEY, "
        "   cname TEXT, "
        "   contact TEXT, "
        "   amount REAL, "
        "   net_pay REAL, "
        "   date TEXT, "
        "   bill_data TEXT"
        ")"
    )
    con.commit()

    con.close()

# Run this function once to create the tables.
create_db()
print("Database and tables created successfully.")