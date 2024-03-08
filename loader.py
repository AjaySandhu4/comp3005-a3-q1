import psycopg
import getpass

def main():
    # Taking user credentials to connect to database
    print('Enter user: ')
    user = input()
    print('Enter password: ')
    pwd = getpass.getpass('')
    setupDatabase(user, pwd) # Create and connect to new database
    print('Connected to database!')

    # Populate new database with the default data
    loadInitialData()
    print('Loaded initial data!')
    
    db_conn.close()
    print('Database setup complete!')
   
# Creates database 'a3' and creates global connection to it
def setupDatabase(user, pwd):
    try:
        with psycopg.connect(f'dbname=postgres user={user} password={pwd} host=localhost port=5432', autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute('DROP DATABASE IF EXISTS a3')
                cursor.execute('CREATE DATABASE a3')

        global db_conn
        db_conn = psycopg.connect(
                f'dbname=a3 user={user} password={pwd} host=localhost port=5432'
        )
    except Exception as e:
        print('Failed to connect to database', e)
        exit(1)

# Loads default data into the database
def loadInitialData():
    try:
        with db_conn.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS students')

            table_creation = "CREATE TABLE students (student_id SERIAL PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, enrollment_date DATE);"
            cursor.execute(table_creation)

            insertion_tuples = (('John', 'Doe', 'john.doe@example.com', '2023-09-01'),('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02'))
            cursor.executemany('INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES(%s,%s,%s,%s)', insertion_tuples)

            db_conn.commit()
    except:
        db_conn.close()
        print('Failed to insert initial data')
        exit(1)


if __name__ == '__main__':
    main()

