from person import Person
from systemLogger import SystemLogger
from datetime import datetime
import pyodbc
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Admin(Person):
    def __init__(self, first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, admin_id):
        super().__init__( first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number)
        self.registration_date = registration_date 
        self._admin_id = admin_id

    @classmethod
    def fetch_data(cls): # mao ni magkuha student data gikan db
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PlatformAdmin") #sql statement
        rows = cursor.fetchall()

        Instructors = [cls( first_name = row.FirstName, middle_name = row.MiddleName, last_name = row.LastName, age = row.Age, gender  = row.Gender, email = row.Email, password = row.Password, birthday = row.Birthday, address = row.Address, phone_number = row.PhoneNumber, registration_date = row.RegistrationDate, admin_id = row.AdminID) for row in rows]
        cursor.close() 
        conn.close()
        return Instructors
    
    @staticmethod
    def admin_full_name(first_name, middle_name, last_name):
        return f"{first_name} {middle_name} {last_name}".strip()

    @classmethod
    def register_admin(cls):
        os.system("cls")  # clear the console
        existing_emails = cls.fetch_data()  # check if the instructor is already registered
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" ADMIN REGISTRATION MENU")
            first_name = input("Input first name: ")
            middle_name = input("Input middle name: (press Enter to skip) ")
            last_name = input("Input last name: ")
            age = int(input("Input age: "))
            gender = input("Input gender (M/F): ").upper()
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

            cursor.execute("{CALL GenerateAdminID()}")
            generated_admin_id = cursor.fetchone()[0]  # get the first column of the first row (0 ra siya kay naka-index man na)
            if not generated_admin_id:
                raise ValueError("Failed to generate a valid AdminID.")

            new_admin = cls(first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number, registration_date, generated_admin_id)
            insert_query = """
                INSERT INTO PlatformAdmin
                (FirstName, MiddleName, LastName, Age, Gender, Email, Password, Birthday, Address, PhoneNumber, RegistrationDate, AdminID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (new_admin.first_name, new_admin.middle_name, new_admin.last_name, new_admin.age, new_admin.gender, new_admin._email, new_admin._password, new_admin._birthday, new_admin.address, new_admin._phone_number, new_admin.registration_date, new_admin._admin_id))
            conn.commit()
            os.system("cls")
            SystemLogger.log_info(f"{first_name} {last_name} was successfully registered as an admin!")
            action = input("Press Enter to return to menu...")
            return

        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def login_admin(cls):
        os.system("cls")
        admins = cls.fetch_data()  # fetch all admins from the database
        conn = create_connection()
        cursor = conn.cursor()

        try:
            conn = create_connection() 
            cursor = conn.cursor() 
                 
            while True:
                print(" SIGN IN AS ADMIN:")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                # Check if the admin exists and if the password matches
                admin = next((admin for admin in admins if admin._email.lower() == email.lower()), None)

                if admin and admin._password == password:  # Check if admin exists and password matches
                    return admin
                else:
                    os.system("cls")
                    print("Invalid email or password")
                    action = input("Press Enter key to again . . .\n ")
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
    def deactivate_student(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            print(" DEACTIVATE STUDENT ACCOUNT:")
            student_id = input("Enter Student ID: ").upper()
            cursor.execute("SELECT AccountStatus FROM Students WHERE StudentID = ?", (student_id,))
            student = cursor.fetchone()

            if student is None:
                print(f"Student {student_id} not found.")
                action = input("\nPress Enter to return to menu . . . \n")
                return
            account_status = student[0]
            
            if account_status == 'Deactivated':
                print("Account is already deactivated.")
                action = input("\nPress Enter to return to menu . . . \n")
                return

            cursor.execute("UPDATE Students SET AccountStatus = 'Deactivated' WHERE StudentID = ?", (student_id,))
            conn.commit()

            print(f"Account for {student_id} has been deactivated.")
            action = input("\nPress Enter to return to exit . . . \n")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def deactivate_instructor(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            print(" DEACTIVATE INSTRUCTOR ACCOUNT:")
            instructor_id = input("Enter Instructor ID: ")
            cursor.execute("SELECT AccountStatus FROM Instructors WHERE InstructorID = ?", (instructor_id,))
            student = cursor.fetchone()

            if student is None:
                print("Instructor not found.")
                action = input("\nPress Enter to return to exit . . . \n")
                return
            account_status = student[0]
            
            if account_status == 'Deactivated':
                print("Account is already deactivated.")
                action = input("\nPress Enter to return to exit . . . \n")
                return

            cursor.execute("UPDATE Instructors SET AccountStatus = 'Deactivated' WHERE InstructorID = ?", (instructor_id,))
            conn.commit()

            print(f"Account for {instructor_id} has been deactivated.")
            action = input("\nPress Enter to return to exit . . . \n")
            return

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_all_admins(cls):
        os.system("cls") 
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT AdminID, FirstName, MiddleName, LastName,Age, Gender, PhoneNumber,Address, RegistrationDate FROM PlatformAdmin") 
            rows = cursor.fetchall()

            if not rows:
                print("No students found.")
                return
            print("ADMIN DASHBOARD:\n")
            print(f"{'Admin ID':<20}{'Full Name':<40}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<30}{'Registration Date':<15}")
            print("=" * 153)

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip() 
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"
                print(f"{row[0]:<20}{full_name:<40}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<30}{registration_date_str:<15}")

            action = input("\nPress Enter key to return to menu . . . \n")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    def view_admin_profile(admin):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            admin_id = admin._admin_id
            cursor.execute("SELECT AdminID, FirstName, MiddleName, LastName, Age, Gender, PhoneNumber,Address, RegistrationDate FROM PlatformAdmin WHERE AdminID = ?", (admin_id),) 
            rows = cursor.fetchall()

            if not rows:
                print("No Admin found.")
                action = input("\nPress Enter to return to menu . . . \n")
                return admin
            
            print("PROFILE DASHBOARD:\n")
            print(f"{'Admin ID':<20}{'Full Name':<40}{'Age':<10}{'Gender':10}{'Phone Number':<15}{'Address':<30}{'Registration Date':<15}")
            print("=" * 153)

            for row in rows:
                full_name = f"{row[1]} {row[2]} {row[3]}".strip() 
                registration_date_str = row[8].strftime("%Y-%m-%d") if row[8] else "N/A"
                print(f"{row[0]:<20}{full_name:<40}{row[4]:<10}{row[5]:<10}{row[6]:<15}{row[7]:<30}{registration_date_str:<15}")

                action = input("\nPress Enter to return to menu . . . \n")
                return admin
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}")
            action = input("\nPress Enter to return to menu . . . \n")

        finally:
            cursor.close()
            conn.close()

    def platform_statistic(self):
        os.system("cls")   
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS TotalActiveStudents FROM Students WHERE AccountStatus = 'Active';")
            students = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS TotalActiveInstructors FROM Instructors WHERE AccountStatus = 'Active';")
            instructors = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS TotalApprovedCourses FROM Courses WHERE CourseStatus = 'Approved';")
            courses = cursor.fetchall()

            print(" PLATFORM STATISTICS:")
            print("=" * 30)
            print(f"{'Active Students:':<25} {students[0][0]:<40}")
            print(f"{'Active Instructors:':<25} {instructors[0][0]:<40}")
            print(f"{'Available Courses:':<25} {courses[0][0]:<40}")

            action = input("\nPress Enter to return to menu . . .\n")
            return

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}")
            action = input("\nPress Enter to return to menu . . .\n")

        finally:
            cursor.close()
            conn.close()