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
                category_id INTEGER,
                activity_name TEXT NOT NULL
            )
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                activity_id INTEGER,
                FOREIGN KEY (activity_id) REFERENCES activities(id)
            )
        """)
    connection.commit()
    print('create tables')

def add_activity(category_id, activity_name):
    cursor.execute(
        """
        INSERT INTO activities (category_id, activity_name)
        VALUES (?, ?)
        """,
        (category_id, activity_name)
    )
    connection.commit()
    return cursor.lastrowid


def add_activity_log(date, activity_id):
    cursor.execute(
        """
        INSERT INTO activities_log (date, activity_id)
        VALUES (?, ?)
        """,
        (date, activity_id)
    )
    connection.commit()
    return cursor.lastrowid

def add_category(category):
    try:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category,)
        )

        connection.commit()
        print('added')
        return cursor.lastrowid
    except:
        print("no name find")
        return None
        
# delete all the data in the table
def reset_table(table):
    cursor.execute(f"""
            DROP TABLE {table};
        """)
    connection.commit()
    print('deleted')


def delete_activities(category_id, activity_name):
    cursor.execute(
        """
        DELETE FROM activities
        WHERE category_id = ?
        AND activity_name = ?
        """,
        (category_id, activity_name)
    )

    connection.commit()

    print(f"Deleted {activity_name}")

def delete_category(category_id):
    cursor.execute(
        """
        DELETE FROM activities
        WHERE category_id = ?
        """,
        (category_id,)
    )

    cursor.execute(
        """
        DELETE FROM categories
        WHERE id = ?
        """,
        (category_id,)
        )

    connection.commit()

    print(f"Deleted {category_id}")
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