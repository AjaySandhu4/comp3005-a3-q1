import psycopg
import getpass
from tabulate import tabulate

def main():
    print('Enter user: ')
    user = input()
    print('Enter password: ')
    pwd = getpass.getpass('')
    connectToDatabase(user, pwd)
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
                try:
                    addStudent(first_name, last_name, email, enrollment_date)
                except:
                    print('Failed to add student')
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

def connectToDatabase(user, pwd):
    try:
        global db_conn
        db_conn = psycopg.connect(
                f'dbname=a3 user={user} password={pwd} host=localhost port=5432'
        )
    except:
        print('Failed to connect to database')
        exit(1)

def getAllStudents():
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['first_name',' last_name', 'email', 'enrollment_date'], tablefmt='fancy_grid'))

def addStudent(first_name, last_name, email, enrollment_date):
    with db_conn.cursor() as cursor:
        cursor.execute('INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES(%s,%s,%s,%s)', (first_name, last_name, email, enrollment_date))

def updateStudentEmail(student_id, email):
    with db_conn.cursor() as cursor:
        cursor.execute('UPDATE students SET email=%s WHERE student_id=%s', (email, student_id))

def deleteStudent(student_id):
    with db_conn.cursor() as cursor:
        cursor.execute(f'DELETE FROM students WHERE student_id={student_id}')

if __name__ == '__main__':
    main()