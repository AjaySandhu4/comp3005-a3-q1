import psycopg
import getpass
from tabulate import tabulate

def main():

    # Taking user credentials to connect to database
    print('Enter user: ')
    user = input()
    print('Enter password: ')
    pwd = getpass.getpass('')
    connectToDatabase(user, pwd)

    # Control structure for user input
    while(True):
        print('\nSelect an option:')
        print('\t 1. Display all students')
        print('\t 2. Add student')
        print('\t 3. Update student email')
        print('\t 4. Delete student')
        print('\t 5. Quit')
        try:
            option = input()
            if(option == '1'):
                print('Displaying students...')
                getAllStudents()
            elif(option == '2'):
                print('Adding student...')
                print('Enter first name: ')
                first_name = input()
                print('Enter last name: ')
                last_name = input()
                print('Enter email: ')
                email = input()
                print('Enter enrollment date: ')
                enrollment_date = input()
                addStudent(first_name, last_name, email, enrollment_date)
            elif(option == '3'):
                print('Updating student email...')
                print('Enter student id')
                student_id = input()
                print('Enter email')
                email = input()
                updateStudentEmail(student_id, email)
            elif(option == '4'):
                print('Deleting student...')
                print('Enter student id')
                student_id = input()
                deleteStudent(student_id)
            elif(option == '5'):
                print('Bye!')
                db_conn.close()
                break
            else:
                raise Exception('Please enter a number between 1 and 4')
        except Exception as e:
            print(e)

# Connects to postgres database
# Assumes that database is a3 postgres is running locally on port 5432
def connectToDatabase(user, pwd):
    try:
        global db_conn
        db_conn = psycopg.connect(
                f'dbname=a3 user={user} password={pwd} host=localhost port=5432'
        )
    except:
        print('Failed to connect to database')
        exit(1)

# Retrieves and displays all student tuples
def getAllStudents():
    with db_conn.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            print(tabulate(rows, headers=['first_name',' last_name', 'email', 'enrollment_date'], tablefmt='fancy_grid'))
        except:
            print('Failed to retrieve students')
            db_conn.rollback()


# Adds student tuple
def addStudent(first_name, last_name, email, enrollment_date):
    with db_conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES(%s,%s,%s,%s)', (first_name, last_name, email, enrollment_date))
            db_conn.commit()
        except:
            print('Failed to add student')
            db_conn.rollback()

# Updates email of student tuple specified by student_id
def updateStudentEmail(student_id, email):
    with db_conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE students SET email=%s WHERE student_id=%s', (email, student_id))
            db_conn.commit()
        except:
            print('Failed to update student')
            db_conn.rollback()

# Deletes student with specified student_id
def deleteStudent(student_id):
    with db_conn.cursor() as cursor:
        try:
            cursor.execute(f'DELETE FROM students WHERE student_id={student_id}')
            db_conn.commit()
        except:
            print('Failed to delete student')
            db_conn.rollback()

if __name__ == '__main__':
    main()