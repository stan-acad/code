from datetime import datetime
from systemLogger import SystemLogger
from person import Person
import pyodbc 
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Student(Person):

    def __init__(self, first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, account_status, student_id):
        super().__init__( first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number)
        self.registration_date = registration_date
        self.account_status = account_status
        self._student_id = student_id

    @staticmethod
    def student_full_name(first_name, middle_name, last_name):
        return f"{first_name} {middle_name} {last_name}".strip()
    
    @classmethod
    def fetch_data(cls): # mao ni magkuha student data gikan db

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students") #sql statement
        rows = cursor.fetchall()

        Students = [cls( 
                        first_name = row.FirstName, 
                        middle_name = row.MiddleName, 
                        last_name = row.LastName, 
                        age = row.Age, 
                        gender  = row.Gender, 
                        email = row.Email, 
                        password = row.Password, 
                        birthday = row.Birthday, 
                        address = row.Address, 
                        phone_number = row.PhoneNumber, 
                        registration_date = row.RegistrationDate,
                        account_status = row.AccountStatus, 
                        student_id = row.StudentID) for row in rows]
        cursor.close() 
        conn.close()
        return Students

    @classmethod
    def register_student(cls):
        os.system("cls")  # clear the console
        existing_emails = cls.fetch_data()  # Check if the student is already registered
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" STUDENT REGISTRATION MENU:")
            first_name = input("Enter first name: ")
            middle_name = input("Enter middle name: (press Enter to skip) ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: ")) 
            gender = input("Enter gender (M/F): ").upper()
            email = input("Enter your email: ")

            # check if the email exists
            for existing_email in existing_emails:
                if existing_email._email.lower() == email.lower(): 
                    SystemLogger.log_error("Email already in use!")
                    return None  # exit if email exists

            password = input("Enter password: ")
            birthday = input("Enter birthdate (YYYY-MM-DD): ")
            address = input("Enter address (City, Province): ")
            phone_number = input("Enter phone number: ")
            registration_date = datetime.now().date()
            account_status = "Active"

            # call the stored proc
            cursor.execute("{CALL GenerateStudentID()}")
            generated_student_id = cursor.fetchone()[0]  # get the first column of the first row (0 ra siya kay naka-index man na)
            if not generated_student_id:
                raise ValueError("Failed to generate a valid StudentID.")

            new_student = cls(first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, account_status, generated_student_id)
            insert_query = """
                INSERT INTO Students 
                (FirstName, MiddleName, LastName, Age, Gender, Email, Password, Birthday, Address, PhoneNumber, RegistrationDate, AccountStatus, StudentID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (new_student.first_name, new_student.middle_name, new_student.last_name, new_student.age, new_student.gender, new_student._email, new_student._password, new_student._birthday, new_student.address, new_student._phone_number, new_student.registration_date,new_student.account_status, new_student._student_id))
            conn.commit()
            os.system("cls") 
            SystemLogger.log_info(f"{first_name} {last_name} was successfully registered as a student!")
            action = input("Press Enter key to return to menu . . . \n")
            return

        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def login_student(cls):
        os.system("cls")
        students = cls.fetch_data()  # fetch all students from the database
        conn = None
        cursor = None

        try:
            conn = create_connection() 
            cursor = conn.cursor()      

            while True:  # loop until successful login
                print(" SIGN IN AS STUDENT:")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                # if the student exists
                student = next((student for student in students if student._email.lower() == email.lower()), None)

                if student:
                    if student.account_status.lower() == "deactivated":  # Check account status
                        os.system("cls")
                        print("ERROR: Your account was deactivated. Please contact us at support@mla.edu.ph for assistance.\n")
                        action = input("Press Enter  key to exit . . . \n")
                        break
                    elif student._password == password: 
                        return student
                else:
                    os.system("cls")
                    print("ERROR: Invalid email/password.")
                    action = input("Press Enter key to try again . . .\n ")
                    os.system("cls")

        except Exception as e:
            SystemLogger.log_error(f"Error during login: {e}")
            return False  # Return false on error
        finally:
            if cursor is not None:
                cursor.close()  # Close cursor if it was created
            if conn is not None:
                conn.close()    # Close connection if it was created

    @classmethod
    def view_all_students(cls):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT StudentID, FirstName, MiddleName, LastName,Age, Gender, PhoneNumber,Address, RegistrationDate FROM Students") 
            rows = cursor.fetchall()

            if not rows:
                print("No students found.")
                return
            print("STUDENT DASHBOARD:\n")
            print(f"{'Student ID':<20}{'Full Name':<40}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<40}{'Registration Date':<15}")
            print("=" * 153)

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip() 
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"
                print(f"{row[0]:<20}{full_name:<40}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<40}{registration_date_str:<15}")

            action = input("\nPress Enter key to return to menu . . . \n")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    def view_student_profile(student):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = student._student_id
            cursor.execute("SELECT StudentID, FirstName, MiddleName, LastName,Age, Gender, PhoneNumber,Address, RegistrationDate FROM Students WHERE StudentID = ?", (student_id),) 
            rows = cursor.fetchall()

            if not rows:
                print("No students found.")
                action = input("\nPress Enter to return to menu . . .\n\n\n")
                return student
            
            print("PROFILE DASHBOARD:\n")
            print(f"{'Student ID':<20}{'Full Name':<40}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<40}{'Registration Date':<15}")
            print("=" * 153)

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip() 
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"
                print(f"{row[0]:<20}{full_name:<40}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<40}{registration_date_str:<15}")

                action = input("\nPress Enter to return to menu . . .\n")
                return student
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()

