import csv, sqlite3
import os.path
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "products.db")
csv_path = os.path.join(BASE_DIR, "db.csv")

con = sqlite3.connect(db_path)

# Load CSV data into Pandas DataFrame
stud_data = pd.read_csv(csv_path)

# Write the data to a sqlite table
stud_data.to_sql('exisiting_products', con, if_exists='replace', index=False)

# Create a cursor object
cur = con.cursor()

# Fetch and display result
#for row in cur.execute('SELECT * FROM student'):
#    print(row)
# Close connection to SQLite database
con.close()