from grade import Grade
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

class Assignment(): # allow instructors to assign work
    def __init__(self, ass_id, course_id, student_id, ass_name, ass_details, ass_type, learning_resources, date_created, deadline, answer, score, items, ass_status, answer_status):
        self._ass_id = ass_id        
        self.course_id = course_id
        self.student_id = student_id
        self.ass_name = ass_name
        self.ass_details = ass_details
        self.ass_type = ass_type      
        self.learning_resources = learning_resources # learning materials
        self.date_created = date_created
        self.deadline = deadline
        self.answer = answer
        self.score = score
        self.items = items
        self.ass_status = ass_status    # uploaded/removed
        self.answer_status = answer_status # 'in-progress', 'completed', 'overdue', '
  
    @classmethod
    def fetch_assignments(cls):  # Fetch assignment data from the database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Assignments")  # SQL statement for Assignments table
        rows = cursor.fetchall()

        assignments = [cls(assignment_id=row.AssignmentID, 
                        course_id=row.CourseID, 
                        assi_name=row.AssignmentName, 
                        ass_details=row.AssignmentDetails, 
                        ass_type=row.AssignmentType,
                        learning_resources=row.LearningResources, 
                        date_created=row.DateCreated,
                        deadline=row.Deadline, 
                        items=row.Items, 
                        ass_status=row.AssignmentStatus, ) for row in rows]  # Create Assignment instances
                        
        cursor.close() 
        conn.close()
        return assignments

    def create_assignment(instructor):
        os.system("cls") 
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" VIEW ASSIGNMENT:")
            cursor.execute("EXEC GenerateAssignmentID")
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate AssignmentID.")
            
            assignment_id = result[0]
            print(f"Generated ID: {assignment_id}")
            
            course_id = input("Assign to Course ID: ").upper()
            instructor_id = instructor._instructor_id

            ass_name = input("Enter Assignment Name: ")
            ass_details = input("Enter Assignment Details: ")
            ass_type = "Task"      
            learning_resources = input("Upload Learning Materials (mp4/pdf/txt file): ")

            while not learning_resources.strip():
                learning_resources = input("ERROR: Materials cannot be empty. Please upload Learning Materials (mp4/pdf/txt file): ")

            date_created = datetime.now().date()
            deadline = input("Set Deadline (YYYY-MM-DD): ")
            items = input("Set total items/score: ")
            ass_status = "Uploaded"

            insert_query = """
                INSERT INTO Assignments (AssignmentID, CourseID, InstructorID, AssignmentName, AssignmentDetails, AssignmentType, LearningResources, DateCreated, Deadline, TotalItems, AssignmentStatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (assignment_id, course_id, instructor_id, ass_name, ass_details, ass_type, learning_resources, date_created, deadline, items, ass_status))           
            conn.commit()
            SystemLogger.log_info(f"{assignment_id} was successfully uploaded as an assignment.")
            action = input("Press Enter key to return to menu . . .")
            return instructor

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            action = input("Press Enter key to return to menu . . .")
            return instructor
        
        finally:
            cursor.close()
            conn.close()

    def view_created_assignments(instructor): 
        os.system("cls")   
        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
            SELECT 
                CourseID,               
                AssignmentName,
                AssignmentDetails, 
                LearningResources, 
                DateCreated, 
                Deadline 
            FROM Assignments
            WHERE InstructorID = ?
            ORDER BY CourseID;
            """
            cursor.execute(query, (instructor._instructor_id))
            assignment_rows = cursor.fetchall()

            if not assignment_rows:
                print(f"No Assignments found..")
                action = input("Press Enter key to proceed . . .")
                return
            
            print(f"YOUR CREATED ASSIGNMENTS ( ordered by course ):\n")
            print(f"{'CourseID':<15}{'Assignment Name':<25}{'Details':<40}{'Resources':<30}{'Created On':<20}{'Deadline':<20}")
            print("=" * 140)

            for assignment in assignment_rows:
                date_created = assignment[4].strftime("%Y-%m-%d") if isinstance(assignment[4], datetime) else str(assignment[4])
                deadline = assignment[5].strftime("%Y-%m-%d") if isinstance(assignment[5], datetime) else str(assignment[5])
                
                print(f"{assignment[0]:<15}{assignment[1]:<25}{assignment[2]:<40}{assignment[3]:30}{date_created:<20}{deadline:<20}")

            action = input("\nPress Enter to return to menu . . . ")
            return instructor

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}. Please check your input!")
            print("An error occurred. Please try again later.")
        finally:
            cursor.close()
            conn.close()

    def view_my_assignment(student): 
        os.system("cls")   
        conn = create_connection()
        cursor = conn.cursor()
        try:
            print(" ASSIGNMENT DASHBOARD:")
            cursor.execute("SELECT CourseID FROM Enrollments WHERE Status = 'Enrolled' AND StudentID = ?", (student._student_id,))
            rows = cursor.fetchall()

            if not rows:
                print("No available courses for you.")
                action = input("Press Enter to return to menu . . .")
                return student
            print("\nEnrolled Courses: ")
            print(f"=" * 20)
            for row in rows:
                print(f"{row[0]:<15}")

            course_id = input("\nEnter Course ID to view assignment: ").upper()

            query = """
            SELECT 
                AssignmentID,
                AssignmentName, 
                AssignmentDetails, 
                LearningResources, 
                DateCreated, 
                Deadline 
            FROM Assignments
            WHERE CourseID = ?;
            """
            cursor.execute(query, (course_id,))
            assignment_rows = cursor.fetchall()

            if not assignment_rows:
                os.system("cls")
                SystemLogger.log_info(f"No Assignments found for {course_id}.")
                action = input("\nPress Enter to return to menu . . .")
                return student
                
            os.system("cls")
            print(f"YOUR ASSIGNMENTS FROM {course_id}:\n")
            print(f"{'AssignmentID':<15}{'Assignment Name':<30}{'Details':<30}{'Resources':<15}{'Created On':<20}{'Deadline':<20}")
            for assignment in assignment_rows:
                date_created = assignment[4].strftime("%Y-%m-%d") if isinstance(assignment[4], datetime) else str(assignment[4])
                deadline = assignment[5].strftime("%Y-%m-%d") if isinstance(assignment[5], datetime) else str(assignment[5])
                
                print(f"{assignment[0]:<15}{assignment[1]:<30}{assignment[2]:<30}{assignment[3]:15}{date_created:<20}{deadline:<20}")
                action = input("\nPress '1' to return to menu or '2' to answer assignment: ")
            
            if action == "1":
                return student
            elif action == "2":
                Assignment.submit_assignment(student)
            else:
                return

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}. Please check your input!")
            action = input("An error occurred. Please try again later. ")

        finally:
            cursor.close()
            conn.close()

    def submit_assignment(student):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            print("\n SUBMIT ASSIGNMENT:")
            cursor.execute("EXEC GenerateAnswerID")  # Correct stored procedure call
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate CourseID.")
    
            answer_id = result[0]
            assignment_id = input("Enter Assignment ID to answer: ").upper()
            student_id = student._student_id
            
            # Check if the assignment is valid for the enrolled courses
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Assignments 
                WHERE AssignmentID = ? AND CourseID IN (
                    SELECT CourseID 
                    FROM Enrollments 
                    WHERE StudentID = ? AND Status = 'Enrolled'
                )
            """, (assignment_id, student_id))
            
            assignment_exists = cursor.fetchone()[0] > 0
            
            if not assignment_exists:
                print("Invalid Assignment ID. You can only submit assignments that are assigned to your enrolled courses.")
                action = input("\nPress Enter to return to menu . . .")
                return student
            
            # Check if the student has already submitted an answer for this assignment
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Answers 
                WHERE AssignmentID = ? AND StudentID = ?
            """, (assignment_id, student_id))
            
            already_submitted = cursor.fetchone()[0] > 0
            
            if already_submitted:
                print("You have already submitted an answer for this assignment. You cannot submit again.")
                action = input("\nPress Enter to return to menu . . .")
                return student
            
            answer = input("Upload your answer here: ")
            answer_status = "On Time"
            answer_date = datetime.now().date()

            insert_query = """
                INSERT INTO Answers (AnswerID, AssignmentID, StudentID, Answer , AnswerStatus, DateAnswered)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (answer_id, assignment_id, student_id, answer, answer_status, answer_date))
            conn.commit()
            print("Answer submitted successfully!")
            action = input("\nPress Enter to return to menu . . .")
            return student
        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")
            action = input("\nPress Enter to return to menu . . .")
            return student
        finally:
            cursor.close()
            conn.close()

    def view_student_assignment(instructor):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CourseID, CourseTitle, CourseDescription FROM Courses WHERE CourseStatus = 'Approved' AND InstructorID = ?",(instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                print("No courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            print(f"YOUR APPROVED COURSES:\n"
                  f"{'Course ID':<15}{'Title':<30}{'Description':<50}")
            print("=" * 70)

            for row in rows:
                print(f"{row[0]:<15}{row[1]:<30}{row[2]:<50}")

            course_id = input("\nEnter Course ID to view assignments: ").upper

            cursor.execute("SELECT AssignmentID FROM Assignments WHERE CourseID = ?",(course_id))
            rows = cursor.fetchall()

            os.system("cls")
            print(f" ASSIGNMENTS FOR {course_id}:")
            print(f"{'Assignment ID':<15}")
            print("=" * 15)

            for row in rows:
                print(f"{row[0]:<15}")

            assignment_id = input("\nEnter Assignment ID to view student answers: ").upper()
            cursor.execute("SELECT AnswerID, StudentID, Answer FROM Answers WHERE AssignmentID = ?",(assignment_id))
            rows = cursor.fetchall()

            os.system("cls")
            print(f" ANSWERS FOR ASSIGNMENT {assignment_id}:")
            print(f"{'Answer ID':<15}{'Student ID':<15}{'Answer':<50}")
            print("=" * 60)

            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}{row[2]:<50}")

            action = input("\nPress 1 to grade answer or Enter key to return to menu . . .")

            if action == "1":
                answer_id = input("\nEnter Answer ID to grade: ").upper()
                student_id = input("Enter the corresponding Student ID: ").upper()
                Grade.create_grade(instructor, answer_id, student_id, course_id)
            else:
                return instructor
             
        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")
            action = input("Press Enter key to return to menu . . . \n")

        finally:
            cursor.close()
            conn.close()

    def view_compeleted(student):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT AnswerID FROM Answers WHERE StudentID = ?", (student._student_id,))
            rows = cursor.fetchall()
        
            if not rows:
                print("You have not answered any assignments.")
                action = input("Press 1 to return to menu or press 2 to answer an assignment. ")

                if action == '1':
                    return student
                elif action == '2':
                    return Assignment.submit_assignment(student)
                else:
                    SystemLogger.log_error("Invalid input")
                    return
                
            print("\nYour Completed Assignments: ")
            print(f"=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            action = input("\nPress Enter to return to menu . . .\n")
            return student

        except Exception as e:
            SystemLogger.log_error(f"{e}, please check your input!")
            action = input("Press Enter to return to menu . . .")

        finally:
            cursor.close()
            conn.close()
    

