from systemLogger import SystemLogger
from datetime import datetime
import os
import pyodbc

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Bulletins:
    def __init__(self, bulletin_id, student_id, course_id, instructor_id, assessment, forum_message, bulletin_type, date):
        self._bulletin_id = bulletin_id
        self.student_id = student_id
        self.course_id = course_id
        self.instructor_id = instructor_id
        self.assessment = assessment
        self.forum_message = forum_message
        self.bulletin_type = bulletin_type  # course or instructor assessment/forum message/announcement
        self.date = date

    @classmethod
    def fetch_data(cls): 
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bulletins")
        rows = cursor.fetchall()

        schedules = [cls(bulletin_id = row.BulletinID,
                         student_id = row.StudentID, 
                         course_id = row.CourseID, 
                         instructor_id = row.InstructorID, 
                         assessment = row.Assessment, 
                         forum_message = row.ForumMessage, 
                         bulletin_type = row.BulletinType,
                         date = row.Date) for row in rows]  # Create Schedule instances
                         
        cursor.close() 
        conn.close()
        return schedules
        
    def create_announcement(instructor):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" ADD ANNOUNCEMENTS:")
            cursor.execute("SELECT CourseID FROM Courses WHERE CourseStatus = 'Approved' AND InstructorID = ?",(instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                print("No approved courses found.")
                return
            print(f" Your Approved Courses:\n"
                  f"{'Course ID':<15}")
            print("=" * 15)

            for row in rows:
                print(f"{row[0]:<15}")

            cursor.execute("EXEC GenerateBulletinID")  
            result = cursor.fetchone()
            if result is None:
                raise Exception("Failed to generate BulletinID.")
            
            bulletin_id = result[0] 
            
            course_id = input("\nAssign a Course ID for your announcement: ")
            instructor_id = instructor._instructor_id 
            forum_message = input("Enter your announcement: \n\n")            
            bulletin_type = "Announcement"
            date = datetime.now().date() 
            
            insert_query = """
                INSERT INTO Bulletins (BulletinID, StudentID, CourseID, InstructorID, Assessment, ForumMessage, BulletinType, Date)
                VALUES (?, NULL, ?, ?, NULL, ?, ?, ?)
            """
            cursor.execute(insert_query, (bulletin_id, course_id, instructor_id, forum_message, bulletin_type, date))
            
            conn.commit()  # Commit the transaction
            SystemLogger.log_info(f"{bulletin_id} was successfully uploaded as an announcement.")
            action = input("Press Enter to continue...")
            return instructor

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")

        finally:
            cursor.close()
            conn.close()

    def create_forum_message(student):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" POST A FORUM MESSAGE:")
            cursor.execute("SELECT CourseID FROM Enrollments WHERE Status = 'Enrolled' AND StudentID = ?", (student._student_id))
            rows = cursor.fetchall()

            if not rows:
                print("No available courses for you.")
                action = input("Press Enter to return to menu . . . \n")
                return student
            print("\n Enrolled Courses:")
            print(f"=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            cursor.execute("EXEC GenerateBulletinID") 
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate BulletinID.")
            
            bulletin_id = result[0]  # retrieve the generated BulletinID
            
            course_id = input("\nAssign a Course ID for your message: ").upper()
            student_id = student._student_id 
            forum_message = input("Enter your forum message: \n\n")            
            bulletin_type = "FMessage"
            date = datetime.now().date()  
            
            insert_query = """
                INSERT INTO Bulletins (BulletinID, StudentID, CourseID, InstructorID, Assessment, ForumMessage, BulletinType, Date)
                VALUES (?,?, ?, NULL, NULL, ?, ?, ?)
            """
            cursor.execute(insert_query, (bulletin_id,student_id, course_id, forum_message, bulletin_type, date))
            
            conn.commit()  
            SystemLogger.log_info(f"{bulletin_id} was successfully uploaded to the forum.")
            action = input("Press Enter to continue...\n")
            return student

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            action = input("Press Enter to continue...\n")
            return student
        finally:
            cursor.close()
            conn.close()

    def assess_instructor(student):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" POST INSTRUCTOR ASESSMENT:")
            cursor.execute("SELECT C.InstructorID FROM Enrollments E JOIN Courses C ON E.CourseID = C.CourseID WHERE E.Status = 'Enrolled' AND E.StudentID = ?;", (student._student_id))
            rows = cursor.fetchall()

            if not rows:
                print("No available instructor for you.")
                action = input("Press Enter to return to menu . . .\n")
                return student
            
            print("\n Your instructors: ")
            print(f"=" * 15)

            for row in rows:
                print(f"{row[0]:<15}")

            cursor.execute("EXEC GenerateBulletinID")
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate BulletinID.")
            
            bulletin_id = result[0]
            student_id = student._student_id 
            instructor_id = input("\nEnter Instructor ID to assess: ").upper()

            valid_instructor = False
            for row in rows:
                if row[0].upper() == instructor_id: 
                    valid_instructor = True
                    break

            if valid_instructor:
                assessment = input("Enter your assessment: \n")            
                bulletin_type = "InstructorAssessment"
                date = datetime.now().date() 
                
                insert_query = """
                    INSERT INTO Bulletins (BulletinID, StudentID, CourseID, InstructorID, Assessment, ForumMessage, BulletinType, Date)
                    VALUES ( ?, ?, NULL, NULL, ?, NULL, ?, ?)
                """
                cursor.execute(insert_query, (bulletin_id, student_id, assessment, bulletin_type, date))
                conn.commit()
                os.system("cls")
                SystemLogger.log_info(f" Your assessment for {instructor_id} was successfully uploaded.")
                action = input("Press Enter to continue...")
                return student
            else:
                print(f"Invalid Instructor ID: {instructor_id}. Please enter a valid ID from the list.")
                action = input("Press Enter to continue . . . \n")
                return student

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            action = input("Press Enter to continue . . . \n")
            return student
        finally:
            cursor.close()
            conn.close()

    def view_student_assessment(instructor):
        os.system("cls")  # clear the console
        conn = create_connection()
        cursor = conn.cursor()
        try:
            print(" STUDENT FEEDBACK ( ordered by course ):")
            cursor.execute("SELECT CourseID, Assessment WHERE InstructorID = ? AND BulletinType = 'InstructorAssessment' ORDER BY CourseID ;", (instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                os.system("cls")
                print("No available feedbacks for you.")
                action = input("Press Enter to continue . . . \n")
                return instructor
            
            print(f"{'CourseID':<20}{'Full Name':<30}")
            print("=" * 153) 
            
            for row in rows:
               print(f"{row[0]:<20}{row[1]:<30}")

            action = input("\nPress Enter to return to menu . . .")
            return instructor

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

