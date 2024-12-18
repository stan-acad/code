import pyodbc
import os
from systemLogger import SystemLogger

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Course(): # store course details

    student_limit = 100 

    def __init__(self, course_id, instructor_id, course_status, course_title, course_description, unit, price):
        self._course_id = course_id
        self.instructor_id = instructor_id
        self.course_status = course_status # approved/pending
        self.course_title = course_title
        self.course_description = course_description
        self.unit = unit
        self.price = price

    @classmethod
    def fetch_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Courses")  # SQL statement
        rows = cursor.fetchall()

        Courses = [
            cls(
                _course_id = row.CourseID,  # Adjusted to match database column
                instructor_id = row.InstructorID,
                course_status = row.CourseStatus,
                course_title = row.CourseTitle,
                course_description = row.CourseDescription,
                unit = row.Unit,
                price = row.Price
            )
            for row in rows
        ]
        cursor.close()
        conn.close()
        return Courses

    def create_course( instructor):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" ADD COURSE:")
            cursor.execute("EXEC GenerateCourseID")  # Correct stored procedure call
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate CourseID.")
            
            course_id = result[0]  # Retrieve the generated CourseID
            print(f"Generated CourseID: {course_id}")  # Print the CourseID for debugging
            
            instructor_id = instructor._instructor_id  # Use instructor_id directly, no need for a set
            course_status = "Pending"
            course_title = input("Enter course title: ")
            course_description = input("Enter course description: ")

            try:
                unit = int(input("Enter unit: ")) 
                price = float(input("Enter price: "))
            except ValueError as ve:
                raise ValueError("Invalid input for unit or price. Please enter numeric values.") from ve
            
            student_limit = 100  # Default value for StudentLimit
            course = (course_id, instructor_id, course_status, course_title, course_description, unit, price)

            insert_query = """
                INSERT INTO Courses (CourseID, InstructorID, CourseStatus, CourseTitle, CourseDescription, Unit, Price, StudentLimit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (course[0], course[1], course[2], course[3], course[4], course[5], course[6], student_limit))
            conn.commit()  # Commit the transaction
            SystemLogger.log_info(f"{course_id} was successfully registered, waiting for admin approval!")
            action = input("\nPress Enter to return to menu . . .")
            return

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_all_courses(cls):
        os.system("cls") 
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Courses") 
            rows = cursor.fetchall()

            if not rows:
                print("No courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            print("COURSE DASHBOARD:\n")
            print(f"{'Course ID':<15}{'Instructor ID':<15}{'Status':<10}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
            print("=" * 130)  # Separator line

            for row in rows:
                print(f"{row.CourseID:<15}{row.InstructorID:<15}{row.CourseStatus:<10}{row.CourseTitle:<30}{row.CourseDescription:<50}{row.Unit:<10}{row.Price:<10}")
                
            action = input("\nPress Enter to return to exit . . . \n")
            return
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
            action = input("\nPress Enter to return to exit . . . \n")
            return
        
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_approved_course(cls):  
        os.system("cls")   
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CourseID, InstructorID, CourseTitle, CourseDescription, Unit, Price FROM Courses WHERE CourseStatus = 'Approved'")
            rows = cursor.fetchall()

            if not rows:
                print("No approved courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            print(f"APPROVED COURSES:\n"
                  f"{'Course ID':<15}{'Instructor ID':<15}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
            print("=" * 140)

            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}{row[2]:<30}{row[3]:<50}{row[4]:<10}{row[5]:<10}")

            action = input("\nPress Enter to return to menu . . .")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
            action = input("\nPress Enter to return to exit . . . \n")
            return
        finally:
            cursor.close()
            conn.close()

    def view_my_course(instructor):  
        os.system("cls")   
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CourseID, InstructorID, CourseTitle, CourseDescription, Unit, Price FROM Courses WHERE CourseStatus = 'Approved' AND InstructorID = ?",(instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                print("No courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            print(f"YOUR APPROVED COURSES:\n"
                  f"{'Course ID':<15}{'Instructor ID':<15}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
            print("=" * 140)

            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}{row[2]:<30}{row[3]:<50}{row[4]:<10}{row[5]:<10}")

            action = input("\nPress Enter to return to menu . . .")
            return
            
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
            action = input("\nPress Enter to return to exit . . . \n")
            return
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_pending_course(cls):    
        os.system("cls")    # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CourseID, InstructorID, CourseTitle, CourseDescription, Unit, Price FROM Courses WHERE CourseStatus = 'Pending'")
            rows = cursor.fetchall()

            if not rows:
                print("No pending courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            print(f"PENDING COURSES:\n"
                f"{'Course ID':<15}{'Instructor ID':<15}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
            print("=" * 140)
            
            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}{row[2]:<30}{row[3]:<50}{row[4]:<10}{row[5]:<10}")
            
            action = input("\nPress '1' to return to menu or '2' to approve pending course: ")
            if action == "1":
                return 
            elif action == "2":
                cls.approve_course()
            else:
                SystemLogger.log_error("Invalid input. Please try again.")

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def approve_course(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            course_id = input("Enter the course ID to approve: ").upper()
            cursor.execute("SELECT CourseStatus FROM Courses WHERE CourseID = ?", (course_id,))
            course = cursor.fetchone()

            if course is None:
                print("ERROR: Course not found.")
                action = input("\nPress '1' to return to menu or '2' to approve pending course.")
                return
            
            current_status = course[0]

            if current_status == 'Approved':
                print("Course is already approved.")
                action = input("\nPress '1' to return to menu or '2' to approve pending course.")
                return
            elif current_status != 'Pending':
                print("Course cannot be approved because its status is not 'Pending'.")
                action = input("\nPress '1' to return to menu or '2' to approve pending course.")
                return
            # Update the course status to 'Approved'
            cursor.execute("UPDATE Courses SET CourseStatus = 'Approved' WHERE CourseID = ?", (course_id,))
            conn.commit()
            os.system()
            print(f"Course ID {course_id} has been approved.")
            action = input("\nPress '1' to return to menu or '2' to approve pending course.")
            return

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
            action = input("\nPress '1' to return to menu or '2' to approve pending course.")

        finally:
            cursor.close()
            conn.close()
