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

class Grade(): # allow instructors to grade students
    def __init__(self, grade_id, student_id, ass_id, initial_grade, final_grade, feedback):
        self._grade_id = grade_id
        self.student_id = student_id
        self.ass_id = ass_id
        self.initial_grade = initial_grade
        self.final_grade = final_grade
        self.feedback = feedback

    def create_grade(instructor, answer_id, student_id, course_id):
        conn = create_connection()
        cursor = conn.cursor()

        try:    
            cursor.execute("EXEC GenerateGradeID")
            result = cursor.fetchone()

            if result is None:
                raise Exception("Failed to generate Grade ID.")
            
            grade_id = result[0]
            initial_grade_input = input("Enter their score: ")
            
            while not initial_grade_input.strip():
                initial_grade_input = input("ERROR: Score cannot be empty. Please enter their score: ")
            
            initial_grade = float(initial_grade_input)
            feedback = input("Enter your feedback: ")

            insert_query = """
                INSERT INTO Grades (GradeID, StudentID, CourseID, AnswerID, InitialGrade, TotalItems, FinalGrade, Feedback) 
                VALUES (?, ?, ?, ?, ?, NULL, NULL, ?);
            """
            cursor.execute(insert_query, (grade_id, student_id, course_id, answer_id, initial_grade, feedback))
            conn.commit()
            
            os.system("cls")
            input("Grade successfully recorded. Press Enter to return to the main menu...")

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            input("An error occurred. Press Enter to continue...")

        finally:
            cursor.close()
            conn.close()
        return instructor

    def view_your_grade(student): # view answer where studentid = student._student_id then view grade na ni
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls")
        try:
            cursor.execute("SELECT AnswerID FROM Answers WHERE StudentID = ?", (student._student_id))
            rows = cursor.fetchall()

            print(" ANSWERED ASSIGNMENTS:")
            print(f"{'Answer ID':<15}")
            print("=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            answer_id = input("\nEnter Answer ID to view grade: ")

            cursor.execute("SELECT InitialGrade, Feedback FROM Grades WHERE AnswerID = ?", (answer_id))
            rows = cursor.fetchone()
            os.system("cls")
            SystemLogger.log_info(f"Your grade for Answer {answer_id} is {rows[0]} \nWith Feedback: {rows[1]}")
            input("Press Enter to return to menu . . . \n")

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            input("An error occurred. Press Enter to continue...")

        finally:
            cursor.close()
            conn.close()
    
    def view_student_grade(instructor):
        conn = create_connection()
        cursor = conn.cursor()
        os.system("cls")
        try:
            cursor.execute("SELECT CourseID FROM Courses WHERE InstructorID = ? AND CourseStatus = 'Approved'", (instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                print("No courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return

            print(" YOUR COURSES:")
            print(f"{'Course ID':<15}")
            print("=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            course_id = input("\nEnter Course ID to view student: ").upper()
            cursor.execute("SELECT StudentID FROM Enrollments WHERE CourseID = ?", (course_id))
            rows = cursor.fetchall()

            if not rows:
                print("No student found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            os.system("cls")
            print(f" YOUR STUDENTS FOR COURSE {course_id}:")
            print(f"{'Student ID':<15}")
            print("=" * 15)
            for row in rows:
                print(f"{row[0]:<15}")

            student_id = input("\nEnter Student ID to view their grade: ").upper()
            cursor.execute("SELECT AnswerID, InitialGrade FROM Grades WHERE StudentID = ? AND CourseID = ?", (student_id, course_id))
            rows = cursor.fetchall()

            if not rows:
                print(f"No grades found for Student {student_id}.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            os.system("cls")
            print(f" STUDENT {student_id} GRADES FOR COURSE {course_id}:")
            print(f"{'Answer ID':<15}{'Score':<15}")
            print("=" * 25)
            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}")

            action = input("\nPress Enter to return to menu . . . \n")

        except Exception as e:
            SystemLogger.log_error(f"{str(e)}, please check your input!")
            action = input("An error occurred. Press Enter to continue...")

        finally:
            cursor.close()
            conn.close()

