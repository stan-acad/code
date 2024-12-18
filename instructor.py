from datetime import datetime
from person import Person
from systemLogger import SystemLogger
import pyodbc
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Instructor(Person):
    def __init__(self, first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, account_status, instructor_id):
        super().__init__( first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number)
        self._instructor_id = instructor_id
        self.registration_date = registration_date
        self.account_status = account_status
        
    @staticmethod
    def instructor_full_name(first_name, middle_name, last_name):
        return f"{first_name} {middle_name} {last_name}".strip()
    
    @classmethod
    def fetch_data(cls): # mao ni magkuha student data gikan db

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructors") #sql statement
        rows = cursor.fetchall()

        Instructors = [cls( first_name = row.FirstName, 
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
                           instructor_id = row.InstructorID) for row in rows]
        cursor.close() 
        conn.close()
        return Instructors

    @classmethod
    def register_instructor(cls):
        os.system("clear")  # clear the console
        existing_emails = cls.fetch_data()  # check if the instructor is already registered
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" INSTRUCTOR REGISTRATION MENU")
            first_name = input("Input first name: ")
            middle_name = input("Input middle name: (press Enter to skip)  ")
            last_name = input("Input last name: ")
            age = int(input("Input age: "))
            gender = input("Input gender (M/F): ")
            email = input("Input email: ")

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

            cursor.execute("{CALL GenerateInstructorID()}")
            generated_instructor_id = cursor.fetchone()[0]  # get the first column of the first row (0 ra siya kay naka-index man na)
            if not generated_instructor_id:
                raise ValueError("Failed to generate a valid InstructorID.")

            new_instructor = cls(first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, account_status, generated_instructor_id)
            insert_query = """
                INSERT INTO Instructors 
                (FirstName, MiddleName, LastName, Age, Gender, Email, Password, Birthday, Address, PhoneNumber, RegistrationDate, AccountStatus, InstructorID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (new_instructor.first_name, new_instructor.middle_name, new_instructor.last_name, new_instructor.age, new_instructor.gender, new_instructor._email, new_instructor._password, new_instructor._birthday, new_instructor.address, new_instructor._phone_number, new_instructor.registration_date, new_instructor.account_status, new_instructor._instructor_id))
            conn.commit() 
            os.system("cls")
            SystemLogger.log_info(f"{first_name} {last_name} was successfully registered as an instructor!")
            action = input("Press Enter key to return to main menu . . .")
        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def login_instructor(cls):
        os.system("cls")
        instructors = cls.fetch_data()  # fetch all instructors from the database
        conn = None
        cursor = None

        try:
            conn = create_connection() 
            cursor = conn.cursor() 

            while True:
                print(" SIGN IN AS INSTRUCTOR:")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                instructor = next((instructor for instructor in instructors if instructor._email.lower() == email.lower()), None)

                if instructor:
                    if instructor.account_status.lower() == "deactivated":  # Check account status
                        os.system("cls")
                        print("ERROR: Your account is deactivated. Please contact us at support@mla.edu.ph for assistance.\n")
                        action = input("Press Enter key to exit . . . \n")
                        break
                    elif instructor and instructor._password == password: 
                        return instructor
                else:
                    os.system("cls")
                    print("ERROR: Invalid password.")
                    action = input("Press Enter key to try again . . .\n ")
                    os.system("cls")
            
        except Exception as e:
            SystemLogger.log_error(f"Error during login: {e}")
            return False  
        finally:
            if cursor is not None:
                cursor.close()  
            if conn is not None:
                conn.close()   

    @classmethod
    def view_all_instructors(cls):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT InstructorID, FirstName, MiddleName, LastName, Age, Gender, PhoneNumber, Address, RegistrationDate FROM Instructors")
            rows = cursor.fetchall()

            if not rows:
                print("No students found.")
                return
            
            print(f"{'Instructor ID':<20}{'Full Name':<30}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<30}{'Registration Date':<15}")
            print("=" * 153)  # Separator line

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip()  # Accessing by index
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"  # Format the date
                print(f"{row[0]:<20}{full_name:<30}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<30}{registration_date_str:<15}")

            action = input("\nPress Enter to return to exit . . . \n")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            action = input("\nPress Enter to return to exit . . . \n")
            return
        
        finally:
            cursor.close()
            conn.close()
        
    def view_instructor_profile(instructor):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            instructor_id = instructor._instructor_id
            cursor.execute("SELECT InstructorID, FirstName, MiddleName, LastName, Age, Gender, PhoneNumber, Address, RegistrationDate FROM Instructors WHERE InstructorID = ?", (instructor_id,))
            rows = cursor.fetchall()

            if not rows:
                print("Profile not found.")
                return
            
            print(" YOUR PROFILE:")
            print(f"{'Instructor ID':<20}{'Full Name':<30}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<30}{'Registration Date':<15}")
            print("=" * 153)  # Separator line

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip()  # Accessing by index
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"  # Format the date
                print(f"{row[0]:<20}{full_name:<30}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<30}{registration_date_str:<15}")
            action = input("\nPress Enter to return to main menu . . .\n")
            return instructor
        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()
        