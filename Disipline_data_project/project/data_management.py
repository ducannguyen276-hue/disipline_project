import sqlite3

#connect to database
connection = sqlite3.connect("data_storage.db")
cursor = connection.cursor()

# create table in database incuding (id, first name, last name)
def create_table():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL
                )
            """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category_id INTEGER,
                activity_name TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
    connection.commit()
    print('create table')

# save first/last name to database
def add_info(date, categories, activities):
    try:
        cursor.execute(
            "INSERT INTO activities (date, category_id, activity_name) VALUES (?, ?, ?)",
            (date, categories, activities)
        )

        connection.commit()
        print('added')
    except:
        print("no name find")


def add_category(category):
    try:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category)
        )

        connection.commit()
        print('added')
    except:
        print("no name find")
        
# delete all the data in the table
def reset_table(table):
    cursor.execute(f"""
            DROP TABLE {table};
        """)
    connection.commit()
    print('deleted')
 
# print all the data_storage info in the database
def get_data_storage(table):
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        #check for no information case
        if not rows:
            print("No information")
            return
        
        return rows
    except:
        print('No table')

# close the database
def close_database():
    connection.close()
    print('Close database')