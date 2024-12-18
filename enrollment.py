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

class Enrollments(): # manage student-course relationships

    def __init__(self,enrollment_id, student_id, course_id, enrollment_date, payment_method, payment, status):
        self._enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.payment_method = payment_method
        self.payment = payment
        self.status = status # active, dropped, completed

    @classmethod
    def fetch_data(cls): # mao ni magkuha student data gikan db

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enrollments") #sql statement
        rows = cursor.fetchall()

        Enrollments = [cls( enrollment_id = row.EnrollmentID, 
                           student_id = row.StudentID, 
                           course_id = row.CourseID, 
                           enrollment_date = row.EnrollmentDate, 
                           payment_method  = row.PaymentMethod, 
                           payment = row.Payment, 
                           status = row.Status ) for row in rows]
        cursor.close() 
        conn.close()
        return Enrollments

    def enroll_course(student):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls")  # clear the console
        try:
            while True:
                print(" COURSE ENROLLMENT MENU:") 
                existing_students = Enrollments.fetch_data() 
                cursor.execute("{CALL GenerateEnrollmentID()}")
                enrollment_id = cursor.fetchone()[0]
                student_id = student._student_id

                cursor.execute("SELECT CourseID, InstructorID, CourseTitle, CourseDescription, Unit, Price FROM Courses WHERE CourseStatus = 'Approved'")
                rows = cursor.fetchall()

                if not rows:
                    print("No approved courses found.")
                    action = input("\nPress any keys to return to menu . . .\n")
                    return
                
                print(f" Approved Courses:\n"
                    f"{'Course ID':<15}{'Instructor ID':<15}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
                print("=" * 140)

                for row in rows:
                    print(f"{row[0]:<15}{row[1]:<15}{row[2]:<30}{row[3]:<50}{row[4]:<10}{row[5]:<10}")
                    
                course_id = input("\nEnter course ID to enroll: ").upper()

                for existing_student in existing_students:
                    if existing_student.student_id == student_id and existing_student.course_id == course_id:
                        os.system("cls")  # clear the console
                        SystemLogger.log_error(f"Already enrolled in this course.")
                        action = input("\nPress any keys to return to menu . . .\n")
                        return
                else:
                    enrollment_date = datetime.now().date()

                    cursor.execute("SELECT CourseID, CourseTitle, Price FROM Courses")  # reference for price
                    rows = cursor.fetchall()

                    price = None  # price to None or a default value
                    for row in rows:
                        if row[0] == course_id: 
                            course_title = row[1]
                            price = row[2] 
                            break
                    else:
                        SystemLogger.log_error(f"Course with ID {course_id} not found.")
                        action = input("\nPress any keys to retry.")
                        return

                    payment_method = input("Enter payment method (Credit Card/Paypal/Gcash): ")
                    payment = input(f"Do you want to confirm payment of {price} for {course_title}? (Y/N) ").upper()
                    if payment != 'Y':
                        os.system("cls")
                        SystemLogger.log_error(f"{student_id} did not confirm payment for {course_title}")
                        return
                    else:
                        payment = "Paid"

                    status = "Enrolled"

                    enroll_student = __class__(enrollment_id, student_id, course_id, enrollment_date, payment_method, payment, status)
                    insert_query = """
                        INSERT INTO Enrollments 
                        (EnrollmentID, StudentID, CourseID, EnrollmentDate, PaymentMethod, Payment, Status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(insert_query, (enroll_student._enrollment_id, enroll_student.student_id, enroll_student.course_id, enroll_student.enrollment_date, enroll_student.payment_method, enroll_student.payment, enroll_student.status))
                    conn.commit()
                    action = input(f"{student_id} successfully enrolled to course {course_id}. \nPress Enter key to return to menu . . .") 
                    return student

        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def drop_course(student):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls") 

        try:
            print(" DROP ENROLLMENT MENU:")
            cursor.execute("SELECT CourseID FROM Enrollments WHERE Status = 'Enrolled' AND StudentID = ?", (student._student_id))
            rows = cursor.fetchall()

            if not rows:
                print("You are currenlty not enrolled on any course.")
                action = input("Press Enter key to return to menu . . . \n")
                return student
            print("\nEnrolled Courses: ")
            print(f"=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            student_id = student._student_id 
            course_id = input("Enter course ID: ").upper()

            cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ? AND CourseID = ? AND Status = 'Enrolled'", (student_id, course_id))
            enrollment = cursor.fetchone()

            if enrollment:
                update_query = "UPDATE Enrollments SET Status = ? WHERE StudentID = ? AND CourseID = ? AND Status = 'Enrolled'"
                cursor.execute(update_query, ("Dropped", student_id, course_id))
                conn.commit() 
                SystemLogger.log_warning(f"Enrollment for course {course_id} was dropped successfully.")
                action = input("Press Enter key to return to menu . . . \n")
                return student
            else:
                SystemLogger.log_error(f"No enrollment found for student {student_id} in course {course_id}.")
                return None

        except Exception as e:
            SystemLogger.log_error(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def view_enrolled_course(student):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls")

        try:
            student_id = student._student_id
            print(" YOUR COURSES HISTORY:\n")
            cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ?", (student_id,))
            rows = cursor.fetchall()
            print(f"{'Enrollment ID':<20}{'Student ID':<20}{'CourseID':<20}{'Enrollment Date':<30}{'Status':<50}")
            print("=" * 140) 
            for row in rows:
                enrollmentdate = row[3].strftime("%Y-%m-%d") if row[3] else "N/A"  # Format the date
                print(f"{row[0]:<20}{row[1]:<20}{row[2]:<20}{enrollmentdate:<30}{row[6]:<50}")
            action = input("\nPress Enter key to return to menu . . . \n")
            return student
        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def drop_student(cls):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls") 

        try:

            student_id = input("Enter Student ID: ").upper()
            course_id = input("Enter Course ID: ").upper()

            cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ? AND CourseID = ? AND Status = 'Enrolled'", (student_id, course_id))
            enrollment = cursor.fetchone()

            if enrollment:
                update_query = "UPDATE Enrollments SET Status = ? WHERE StudentID = ? AND CourseID = ? AND Status = 'Enrolled'"
                cursor.execute(update_query, ("Dropped", student_id, course_id))
                conn.commit() 
                SystemLogger.log_warning(f"{student_id} enrollment for course {course_id} was dropped successfully.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            else:
                SystemLogger.log_error(f"{student_id} is currently not enrolled in course {course_id} or does not exist.")
                action = input("Press Enter key to return to menu . . . \n")
                return

        except Exception as e:
            SystemLogger.log_error(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def view_enrolled_students(instructor):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls")

        try:
            instructor_id = instructor._instructor_id
            print(" YOUR STUDENTS:\n")
            cursor.execute(f"""
                SELECT 
                    Enrollments.EnrollmentID,
                    Students.StudentID,
                    Students.FirstName,
                    Students.LastName,
                    Courses.CourseID,
                    Courses.CourseTitle,
                    Enrollments.EnrollmentDate
                FROM Enrollments
                JOIN Students ON Enrollments.StudentID = Students.StudentID
                JOIN Courses ON Enrollments.CourseID = Courses.CourseID
                WHERE Courses.InstructorID = ? AND Enrollments.Status = 'Enrolled'
                ORDER BY Courses.CourseTitle;
            """, (instructor_id,))
            
            rows = cursor.fetchall()
            print(f"{'Enrollment ID':<20}{'Student ID':<20}{'First Name':<20}{'Last Name':<20}{'Course ID':<20}{'Course Title':<30}{'Enrollment Date':<30}")
            print("=" * 150) 
            
            for row in rows:
                enrollment_date = row[6].strftime("%Y-%m-%d") if row[6] else "N/A"  # Correctly index the date
                print(f"{row[0]:<20}{row[1]:<20}{row[2]:<20}{row[3]:<20}{row[4]:<20}{row[5]:<30}{enrollment_date:<30}")
                action = input("\nPress Enter to return to menu . . .")
                return instructor

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    def get_enrollment_details(self):    # return the details of the enrollment
        return {
            f'Student_id': {self.student_id},
            f'Course_id': {self.course_id},
            f'Enrollment_date': {self.enrollment_date},
            f'Enrollment_id': {self._enrollement_id},
            f'Status': {self.status} }
