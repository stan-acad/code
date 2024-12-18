from student import Student
from instructor import Instructor
from admin import Admin
from course import Course
from enrollment import Enrollments
from schedule import Schedule
from assignment import Assignment
from grade import Grade
from bulletin import Bulletins
from systemLogger import SystemLogger
import os

class AdminPlatform():

    platform_name = "MLA Learning Academy"
    platform_owner = "Abdina Learning LLC"

    @staticmethod
    def policy():
        os.system("cls")
        print("""
    E-Learning Platform Policy

    1. Purpose
        - The purpose of this policy is to establish guidelines for the use of the e-learning platform 
          to ensure a safe, respectful, and productive learning environment for all users.

    2. User Registration
        - All users must register for an account to access the platform.
        - Users must provide accurate and complete information during registration.
        - Users are responsible for maintaining the confidentiality of their account credentials.

    3. Code of Conduct
        - Users are expected to treat each other with respect and courtesy.
        - Harassment, discrimination, or any form of abusive behavior will not be tolerated.
        - Users must engage in discussions and activities in a constructive and professional manner.

    4. Content Guidelines
        - Users are encouraged to share knowledge and resources that are relevant to the learning
          objectives.
        - All content shared on the platform must comply with copyright laws and intellectual property 
          rights.
        - Inappropriate content, including but not limited to hate speech, explicit material, or spam, 
          is strictly prohibited.

    5. Privacy and Data Protection
        - The platform is committed to protecting the privacy of its users.
        - Personal information will be collected, used, and stored in accordance with applicable data
          protection laws.
        - Users should not share personal information of others without their consent.

    6. Academic Integrity
        - Users must adhere to principles of academic honesty.
        - Plagiarism, cheating, or any form of dishonest behavior will result in disciplinary action.
        - Users are encouraged to properly cite sources and give credit to original authors.

    7. Accessibility
        - The platform aims to be accessible to all users, including those with disabilities.
        - Users are encouraged to provide feedback on accessibility issues to improve the platform.

    8. Support and Feedback
        - Users can reach out to the support team for assistance with technical issues or questions about
          the platform.
        - Feedback on the platform's features and content is welcome and will be considered for future
          improvements.

    9. Policy Changes
        - The platform reserves the right to modify this policy at any time.
        - Users will be notified of significant changes, and continued use of the platform constitutes 
          acceptance of the updated policy.

    10. Enforcement
        - Violations of this policy may result in account suspension or termination.
        - Users may report violations to the platform administrators for review.

    11. Limitation of Liability
        - The platform is not responsible for any direct, indirect, incidental, or consequential damages 
          resulting from the use or inability to use the platform.

    12. Governing Law
        - This policy shall be governed by and construed in accordance with the laws of the jurisdiction 
          in which the platform operates.
              
    """)
        choice = input("Press Enter key to return to menu . . . \n")

        
    @staticmethod
    def mission():
        os.system("cls")
        print("""
    E-Learning Platform Mission

    1. Commitment to Education
        - Our mission is to provide high-quality educational resources and opportunities to learners 
          of all backgrounds, empowering them to achieve their academic and professional goals.

    2. Accessibility
        - We strive to make education accessible to everyone, regardless of their location, background, 
          or circumstances, by leveraging technology to break down barriers to learning.

    3. Innovation
        - We are dedicated to fostering innovation in education by continuously improving our platform 
          and incorporating the latest technologies and teaching methodologies.

    4. Community Engagement
        - We aim to build a vibrant learning community where students, instructors, and administrators 
          can collaborate, share knowledge, and support each other in their educational journeys.

    5. Lifelong Learning
        - We believe in the importance of lifelong learning and provide resources that encourage 
          continuous personal and professional development.

    6. Student-Centered Approach
        - Our platform is designed with the learner in mind, ensuring that all features and resources 
          are user-friendly and tailored to meet the diverse needs of our students.

    7. Academic Integrity
        - We uphold the highest standards of academic integrity and encourage our users to engage in 
          honest and ethical practices in their learning and assessments.

    8. Support and Resources
        - We are committed to providing comprehensive support and resources to help our users succeed, 
          including technical assistance, academic advising, and access to a wealth of learning materials.

    9. Feedback and Improvement
        - We value feedback from our users and continuously seek ways to enhance our platform and 
          services based on their needs and suggestions.

    10. Global Impact
        - Our mission extends beyond individual success; we aim to make a positive impact on society 
          by equipping learners with the knowledge and skills needed to contribute to their communities 
          and the world.

    """)
        choice = input("Press Enter key to return to menu . . . \n")
        
    @staticmethod
    def vision():
        os.system("cls")
        print("""
    E-Learning Platform Vision

    1. Empowering Learners
        - Our vision is to empower learners to take control of their educational journeys, providing them 
          with the tools and resources they need to succeed in a rapidly changing world.

    2. Inclusive Learning Environment
        - We envision a learning environment that is inclusive and supportive, where every individual 
          feels valued and has the opportunity to thrive, regardless of their background or circumstances.

    3. Transformative Education
        - We aim to transform the educational landscape by integrating innovative technologies and 
          pedagogical approaches that enhance the learning experience and foster critical thinking.

    4. Global Community
        - Our vision includes building a global community of learners, educators, and thought leaders 
          who collaborate and share knowledge across borders, cultures, and disciplines.

    5. Lifelong Learning Culture
        - We aspire to cultivate a culture of lifelong learning, encouraging individuals to continuously 
          seek knowledge and skills that will help them adapt and excel in their personal and professional lives.

    6. Excellence in Education
        - We are committed to achieving excellence in education by providing high-quality content, 
          engaging learning experiences, and effective support systems that promote student success.

    7. Innovation and Adaptability
        - Our vision is to remain at the forefront of educational innovation, continuously adapting to 
          the evolving needs of learners and the demands of the global job market.

    8. Positive Societal Impact
        - We envision our platform making a positive impact on society by equipping learners with the 
          knowledge and skills necessary to contribute meaningfully to their communities and the world.

    """)
        choice = input("Press Enter key to return to menu . . . \n")

    # REGISTER 

    def register_instructors(self):
        Instructor.register_instructor()

    def register_admin(self):
        Admin.register_admin()

    # LOG-IN

    def log_in_student_menu(self):
        student = Student.login_student()        
        if student:
            self.student_menu(student)

    def log_in_instructor(self):
        instructor = Instructor.login_instructor()
        if instructor:
            self.instructor_menu(instructor)  

    def log_in_admin(self):
        admin = Admin.login_admin()
        if admin:
            self.admin_menu(admin)

    # OTHER THINGS

    def enroll_courses(self, student):
        student = Enrollments.enroll_course(student)
        if student:
            self.student_menu(student)

    def drop_course(self, student):
        student = Enrollments.drop_course(student)
        if student:
            self.student_menu(student)
    
    def create_course(self, instructor):
        instructor = Course.create_course(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def create_schedule(self, instructor):
        instructor = Schedule.create_schedule(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def create_announcement(self, instructor):
        instructor = Bulletins.create_announcement(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def create_assignment(self, instructor):
        instructor = Assignment.create_assignment(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def create_grade(self, instructor):
        Grade.create_grade(instructor)

    def create_forum_message(self, student):
        student = Bulletins.create_forum_message(student)
        if student:
            self.student_menu(student)

    # VIEW

    def view_student_assignment(self, instructor):
        instructor = Assignment.view_student_assignment(instructor) 
        if instructor:
            self.instructor_menu(instructor)

    def view_student_profile(self, student):
        student = Student.view_student_profile(student)
        if student:
            self.student_menu(student)

    def view_my_assignments(self, student):
        student = Assignment.view_my_assignment(student)
        if student:
            self.student_menu(student)

    def view_created_assignments(self, instructor):
        instructor = Assignment.view_created_assignments(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def view_enrolled_courses(self, student):
        student = Enrollments.view_enrolled_course(student)
        if student:
            self.student_menu(student)

    def view_enrolled_students(self, instructor):
        instructor = Enrollments.view_enrolled_students(instructor)    
        if instructor:
            self.instructor_menu(instructor)

    def view_instructor_course(self, instructor):
        instructor = Course.view_my_course(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def view_instructor_schedule(self, instructor):
        instructor = Schedule.view_instructor_schedule(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def view_instructor_profile(self, instructor):
        instructor = Instructor.view_instructor_profile(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def view_admin_profile(self, admin):
        admin = Admin.view_admin_profile(admin)
        if admin:
            self.admin_menu(admin)

    def view_final_grade(self, student):
        student = Grade.view_your_grade(student)
        if student:
            self.student_menu(student)

    def view_student_grade(self, instructor):
        instructor = Grade.view_student_grade(instructor)
        if instructor:
            self.instructor_menu(instructor)

    def submit_assignment(self, student):
        student = Assignment.submit_assignment(student)
        if student:
            self.student_menu(student)

    def view_completed(self, student):
        student = Assignment.view_compeleted(student)
        if student:
            self.student_menu(student)

    def assess_instructor(self, student):
        student = Bulletins.assess_instructor(student)
        if student:
            self.student_menu(student)

    def platform_statistic(self):
        Admin.platform_statistic(self)

    def main_menu(self):
        os.system("cls")

        menu_options = { 
            "1": self.student_main_menu,
            "2": self.instructor_main_menu,
            "3": self.admin_main_menu,
            "4": self.about_platform
            }

        while True:
            print ( f"Welcome to {self.platform_name}\n"
                    f" MAIN MENU: \n"
                    f"1. As Student\n"
                    f"2. As Instructor\n"
                    f"3. As Admin\n"
                    f"4. About Platform\n"
                    f"5. Exit\n")

            menu_choice = input("Please enter your choice: ").strip()
            
            if menu_choice == "5":
                os.system("cls")
                SystemLogger.log_warning("Exiting the system")                
                break
            elif menu_choice in menu_options:
                menu_options[menu_choice]()
                break
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action")

    def student_main_menu(self):
        os.system("cls")

        menu_options = {
            "1": self.register_student,
            "2": self.log_in_student_menu,
            "3": self.main_menu, }

        while True:
            print (f" STUDENT MAIN MENU: \n"
                    f"1. Register\n"
                    f"2. Sign In\n"
                    f"3. Back to Main Menu\n")
            
            menu_choice = input("Please enter your choice: ")

            if menu_choice in menu_options:
                menu_options[menu_choice]()
                break
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action")

    def register_student(self):
        os.system("cls")

        Student.register_student()    

        menu_options = {
            "N": self.main_menu,
            "Y": self.log_in_student_menu,}
        
        while True:
            
            menu_choice = input("Would you like to sign in (Y) or go back to the main menu (N)? ").upper()

            if menu_choice in menu_options:
                menu_options[menu_choice]()
                break
            else:
                SystemLogger.log_error("Invalid action")

    def student_menu(self, student):
        while True:
            os.system("cls")

            menu_options = {
                "1": Course.view_approved_course,
                "2": lambda: self.enroll_courses(student),
                "3": lambda: self.drop_course(student),
                "4": lambda: self.view_enrolled_courses(student),
                "5": lambda: self.view_my_assignments(student),
                "6": lambda: self.view_completed(student), 
                "7": lambda: self.view_final_grade(student),
                "8": lambda: self.assess_instructor(student),
                "9": lambda: self.create_forum_message(student), 
                "10": lambda: self.view_student_profile(student),
            }

            print ( f" STUDENT MENU:\n"
                    f"1. View Available Course\n"
                    f"2. Enroll Course\n"
                    f"3. Drop Course\n"
                    f"4. View Course History\n"
                    f"5. View/Answer Assignment\n"
                    f"6. View Completed Assignment\n"
                    f"7. View Grades\n" 
                    f"8. Assess Instructor\n" #
                    f"9. Message Forum\n"
                    f"10. View Student Profile\n"
                    f"11. Log Out\n")

            menu_choice = input(f"Welcome, {student.first_name}! Please enter your choice: ")

            if menu_choice == "11":
                os.system("cls")
                SystemLogger.log_warning(f"Logged out as {student.first_name}.")
                action = input("Press Enter key to return to navigation menu\n")
                AdminPlatform.main_menu(self)
            elif menu_choice in menu_options:

                if callable(menu_options[menu_choice]):
                    menu_options[menu_choice]()
                elif menu_options[menu_choice] == "log_out":
                    os.system("cls")
                    SystemLogger.log_warning(f"Logged out as {student.first_name}.")
                    action = input("Press Enter key to return to navigation menu\n")
                    AdminPlatform.main_menu(self)
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action. Please try again.")
                
    def instructor_main_menu(self):
        os.system("cls")

        menu_options = {
            "1": self.log_in_instructor,
            "2": self.main_menu, }

        while True:
            print (f" INSTRUCTOR MAIN MENU: \n"
                    f"1. Sign In\n"
                    f"2. Back to Main Menu\n")
            
            menu_choice = input("Please enter your choice: ")

            if menu_choice in menu_options:
                menu_options[menu_choice]()
                break
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action")

    def instructor_menu(self, instructor):
        while True:
            os.system("cls")

            menu_options = {
                "1": lambda: self.create_course(instructor),
                "2": lambda: self.view_instructor_course(instructor),
                "3": lambda: self.create_schedule(instructor),
                "4": lambda: self.view_enrolled_students(instructor),
                "5": lambda: self.view_instructor_schedule(instructor),
                "6": lambda: self.create_assignment(instructor),
                "7": lambda: self.view_created_assignments(instructor),
                "8": lambda: self.view_student_assignment(instructor), 
                "9": lambda: self.view_student_grade(instructor), 
                "10": lambda: self.create_announcement(instructor),
                "11": lambda: self.view_instructor_profile(instructor),
                "12": "log_out"
            }

            print(f" INSTRUCTOR MENU:\n"
                f"1. Create Course\n"
                f"2. View Courses\n"
                f"3. Create Schedule\n"
                f"4. View Students Enrolled In Course\n"
                f"5. View Your Schedules\n"
                f"6. Create Assignment/Activities\n"
                f"7. View Assignment/Activities\n"
                f"8. View/Grade Submitted Assignments\n"
                f"9. View Student Grades\n"
                f"10. Add Announcement\n"
                f"11. View Profile\n"
                f"12. Log Out\n")

            menu_choice = input(f"Welcome, Instructor {instructor.last_name}! Enter your choice: ")

            if menu_choice == "12":
                os.system("cls")
                SystemLogger.log_warning(f"Logged out as {instructor.first_name}.")
                action = input("Press Enter key to return to navigation menu\n")
                AdminPlatform.main_menu(self)
            elif menu_choice in menu_options:

                if callable(menu_options[menu_choice]):
                    menu_options[menu_choice]()
                elif menu_options[menu_choice] == "log_out":
                    os.system("cls")
                    SystemLogger.log_warning(f"Logged out as {instructor.first_name}.")
                    action = input("Press Enter key to return to navigation menu\n")
                    AdminPlatform.main_menu(self)
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action. Please try again.")
        
    def admin_main_menu(self):
        os.system("cls")

        menu_options  = {
            "1": self.log_in_admin,
            "2": self.main_menu,
        }

        while True:
            print ( f" ADMIN MENU:\n"
                    f"1. Sign in as Admin\n"
                    f"2. Return to Main Menu\n")
            
            menu_choice = input("Please enter your choice: ")

            if menu_choice in menu_options:
                menu_options[menu_choice]()
                break
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action")
            
    def admin_menu(self, admin):
        while True:
            os.system("cls")

            menu_options = {
                "1": Student.register_student,
                "2": Instructor.register_instructor,
                "3": Admin.register_admin, 
                "4": Student.view_all_students,
                "5": Instructor.view_all_instructors,
                "6": Admin.view_all_admins,
                "7": Course.view_all_courses,
                "8": Course.view_approved_course,
                "9": Course.view_pending_course,  
                "10": Enrollments.drop_student,
                "11": Admin.deactivate_student,
                "12": Admin.deactivate_instructor,
                "13": lambda: self.view_admin_profile(admin),
                "14": "log_out"  
            }
            
            print ( f" ADMIN MENU:\n"
                    f"1. Register Student\n"
                    f"2. Register Instructor\n"
                    f"3. Register Admin\n"
                    f"4. View Students\n"
                    f"5. View Instructors\n"
                    f"6. View Admins\n" #
                    f"7. View Courses\n"
                    f"8. View Approved Courses\n"
                    f"9. View Pending Courses\n"
                    f"10. Drop Enrollment\n" 
                    f"11. Deactivate Student\n"
                    f"12. Deactivate Instructor\n"
                    f"13. View Profile\n"
                    f"14. Log Out\n"
                    )
            
            menu_choice = input(f"Welcome, Admin {admin.last_name}! Enter your choice: ")

            if menu_choice == "14":
                os.system("cls")
                SystemLogger.log_warning(f"Logged out as Admin {admin.first_name}.")
                action = input("Press Enter key to return to navigation menu\n")
                AdminPlatform.main_menu(self)
            elif menu_choice in menu_options:
                if callable(menu_options[menu_choice]):
                    menu_options[menu_choice]() 
                elif menu_options[menu_choice] == "log_out":
                    os.system("cls")
                    SystemLogger.log_warning(f"Logged out as Admin {admin.first_name}.")
                    action = input("Press Enter key to return to navigation menu\n")
                    AdminPlatform.main_menu(self)
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action. Please try again.")
    
    def about_platform(self):
        os.system("cls")

        menu_options = { 
            "1": self.policy,
            "2": self.mission,
            "3": self.vision,
            "4": self.platform_statistic,
            "5": self.main_menu,
            }

        while True:
            print ( 
                    f" ABOUT MLA LEARNING ACADEMY: \n"
                    f"1. Policy\n"
                    f"2. Mission\n"
                    f"3. Vision\n"
                    f"4. Our Statistics\n"
                    f"5. Back to Main Menu\n"
                    )

            menu_choice = input("Please enter your choice: ")
            
            if menu_choice in menu_options:
                menu_options[menu_choice]()
                os.system("cls")
            else:
                os.system("cls")
                SystemLogger.log_error("Invalid action") 

adminPlatform = AdminPlatform()
adminPlatform.main_menu()