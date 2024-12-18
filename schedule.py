from systemLogger import SystemLogger
from datetime import datetime, time
import pyodbc
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= STANVIVOBOOK\\SQLEXPRESS;"
        "DATABASE=OnlineLearningDB;"
        "Trusted_Connection=yes;"
    )

class Schedule():   # for course timing

    def __init__(self, instructor_id, course_id, start_time, end_time, schedule_id, meet_days):
        self.instructor_id = instructor_id        
        self.course_id = course_id
        self.start_time = start_time
        self.end_time = end_time
        self._schedule_id = schedule_id
        self.meet_days = meet_days  # Added MeetDays attribute

    @classmethod
    def fetch_data(cls):  # Fetch schedule data from the database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ScheduleID, InstructorID, CourseID, StartTime, EndTime, MeetDays FROM Schedules")  # Updated SQL statement
        rows = cursor.fetchall()

        schedules = [cls(instructor_id=row.InstructorID, 
                         course_id=row.CourseID, 
                         start_time=row.StartTime, 
                         end_time=row.EndTime, 
                         schedule_id=row.ScheduleID, 
                         meet_days=row.MeetDays) for row in rows]  # Create Schedule instances
                         
        cursor.close() 
        conn.close()
        return schedules
    

    def create_schedule(instructor):
        os.system("cls")  # Clear the console
        conn = create_connection()
        cursor = conn.cursor()

        try:
            print(" ADD SCHEDULE:")

            cursor.execute("SELECT CourseID, InstructorID, CourseTitle, CourseDescription, Unit, Price FROM Courses WHERE CourseStatus = 'Approved' AND InstructorID = ?",(instructor._instructor_id))
            rows = cursor.fetchall()

            if not rows:
                print("No courses found.")
                action = input("Press Enter key to return to menu . . . \n")
                return
            
            print(f"Your courses:\n"
                  f"{'Course ID':<15}{'Instructor ID':<15}{'Title':<30}{'Description':<50}{'Unit':<10}{'Price':<10}")
            print("=" * 140)

            for row in rows:
                print(f"{row[0]:<15}{row[1]:<15}{row[2]:<30}{row[3]:<50}{row[4]:<10}{row[5]:<10}")

            cursor.execute("EXEC GenerateScheduleID")
            result = cursor.fetchone()
            
            if result is None:
                raise Exception("Failed to generate ScheduleID.")
            
            schedule_id = result[0]  # retrieve the generated ScheduleID
            
            instructor_id = instructor._instructor_id
            print("")
            course_id = input("Enter course ID to add schedule: ").upper()
            meet_days = input("Enter meeting days ( e.g., Mon, Wed, Fri ): ")

            if not Schedule.validate_meeting_days(meet_days):
                    os.system("cls")
                    print("ERROR: Invalid day entered. Please enter valid days like 'Mon, Wed, Fri'.")
                    action = input("\nPress Enter key to try again. . . ")
                    return Schedule.create_schedule(instructor)
            
            start_time = input("Set start time (HH:MM:SS): ")  
            end_time = input("Set end time (HH:MM:SS): ")   

            schedule = (schedule_id, instructor_id, course_id, start_time, end_time, meet_days)
            insert_query = """
                INSERT INTO Schedules (ScheduleID, InstructorID, CourseID, StartTime, EndTime, MeetDays)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (schedule[0], schedule[1], schedule[2], schedule[3], schedule[4], schedule[5]))
            conn.commit()  # Commit the transaction

            SystemLogger.log_info(f"{schedule_id} was successfully registered!")
            
            action = input("Press Enter to return to menu . . .\n")
            return instructor

        except pyodbc.IntegrityError as e:
            # Handle specific database errors such as conflicts
            SystemLogger.log_error(f"Schedule conflict detected: {e}")
            print("Schedule conflict detected, please choose a different time.")
            action = input("\nPress Enter to return to menu . . .")
            return instructor

        except Exception as e:
            # Catch any other general errors
            print("\n An error occurred while creating the schedule. Possible schedule conflict, refer to your shedule  dashboard.")
            action = input("\nPress Enter to return to menu . . .")
            return instructor

        finally:
            cursor.close()
            conn.close()

    def view_student_schedule(student):
        pass

    def view_instructor_schedule(instructor):
        os.system("cls") 
        conn = create_connection()
        cursor = conn.cursor()
        try:
            instructor_id = instructor._instructor_id 
            cursor.execute("""
                SELECT ScheduleID, InstructorID, CourseID, StartTime, EndTime, MeetDays 
                FROM Schedules 
                WHERE InstructorID = ?
            """, (instructor_id,))
            
            rows = cursor.fetchall()
            if not rows:
                print("No schedule found.")
                action = ("Press Enter ket to continue . . . ")
                return instructor

            print(" YOUR SCHEDULE DASHBOARD:\n")
            print(f"{'Schedule ID':<20}{'Instructor ID':<20}{'Course ID':20}{'Start Time':<20}{'End Time':<20}{'Meet Days':<20}")
            print("=" * 150)  # Separator line

            for row in rows:
                start_time = row[3].strftime("%H:%M:%S") if isinstance(row[3], time) else "N/A"  # Format StartTime
                end_time = row[4].strftime("%H:%M:%S") if isinstance(row[4], time) else "N/A"  # Format EndTime
                print(f"{row[0]:<20}{row[1]:<20}{row[2]:<20}{start_time:<20}{end_time:<20}{row[5]:<20}")

            action = input("\nPress Enter to return to menu . . .\n")
            return instructor

        except Exception as e:
            SystemLogger.log_error(f"Error: {str(e)}, please check your input!")
        finally:
            cursor.close()
            conn.close()

    def validate_meeting_days(meeting_days):
        valid_days = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
        days = meeting_days.split(",")
        
        for day in days:
            if day not in valid_days:
                return False  # Invalid day in input
        return True