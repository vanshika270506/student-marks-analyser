import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# ADMIN CREDENTIALS
# ===============================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("StudentsPerformance.csv")
marks = df[['math score', 'reading score', 'writing score']]
class_average = marks.mean()
# Overall average per student
df['overall_avg'] = marks.mean(axis=1)

# Rank (1 = highest)
df['rank'] = df['overall_avg'].rank(ascending=False, method='min')

# Percentile
df['percentile'] = df['overall_avg'].rank(pct=True) * 100

# At-risk flag
def at_risk(student_marks):
    if student_marks.mean() < 40 or (student_marks < 35).any():
        return "AT RISK ⚠️"
    else:
        return "SAFE ✅"
def get_all_at_risk_students():
    at_risk_list = []

    for idx in range(len(df)):
        student_marks = marks.loc[idx]
        if at_risk(student_marks) == "AT RISK ⚠️":
            at_risk_list.append({
                "Student ID": idx,
                "Math": student_marks['math score'],
                "Reading": student_marks['reading score'],
                "Writing": student_marks['writing score'],
                "Average": round(student_marks.mean(), 2)
            })

    return pd.DataFrame(at_risk_list)



# ===============================
# HELPER FUNCTIONS
# ===============================

def pass_fail_status(student_marks):
    avg = student_marks.mean()
    return "PASS ✅" if avg >= 40 else "FAIL ❌"

def subject_feedback(mark):
    if mark >= 75:
        return "Excellent 🌟"
    elif mark >= 60:
        return "Good 👍"
    elif mark >= 40:
        return "Average ⚠️"
    else:
        return "Needs Improvement ❌"
def improvement_analysis(student_marks):
    result = {}
    for subject in student_marks.index:
        if student_marks[subject] > class_average[subject]:
            result[subject] = "Above Average 📈"
        elif student_marks[subject] < class_average[subject]:
            result[subject] = "Below Average 📉"
        else:
            result[subject] = "Equal to Average ➖"
    return result


# ===============================
# STUDENT DASHBOARD
# ===============================

def student_dashboard(student_id):
    student_marks = marks.loc[student_id]

    while True:
        print("\n===== STUDENT DASHBOARD =====")
        print(f"Student ID: {student_id}")
        print("1. View Marks")
        print("2. View Marks Graph")
        print("3. Average vs Class Average")
        print("4. Pass / Fail Status")
        print("5. Subject-wise Feedback")
        print("6. Rank & Percentile")
        print("7. Improvement / Decline Analysis")
        print("8. At-Risk Status")
        print("9. Logout")


        choice = input("Enter choice: ")

        # ---------------- VIEW MARKS ----------------
        if choice == "1":
            print("\nYour Marks:")
            print(student_marks)

        # ---------------- MARKS GRAPH ----------------
        elif choice == "2":
            student_marks.plot(kind='bar')
            plt.title(f"Marks of Student {student_id}")
            plt.ylabel("Marks")
            plt.ylim(0, 100)
            plt.tight_layout()
            plt.show()

        # -------- AVERAGE vs CLASS AVERAGE ----------
        elif choice == "3":
            comparison = pd.DataFrame({
                "Your Marks": student_marks,
                "Class Average": class_average
            })

            while True:
                print("\n--- Average vs Class Average ---")
                print("1. View Scores Only")
                print("2. View Graph Only")
                print("3. View Both Scores & Graph")
                print("4. Back")

                sub_choice = input("Enter choice: ")

                if sub_choice == "1":
                    print("\nScores Comparison:")
                    print(comparison)

                elif sub_choice == "2":
                    comparison.plot(kind='bar')
                    plt.title("Your Marks vs Class Average")
                    plt.ylabel("Marks")
                    plt.tight_layout()
                    plt.show()

                elif sub_choice == "3":
                    print("\nScores Comparison:")
                    print(comparison)

                    comparison.plot(kind='bar')
                    plt.title("Your Marks vs Class Average")
                    plt.ylabel("Marks")
                    plt.tight_layout()
                    plt.show()

                elif sub_choice == "4":
                    break

                else:
                    print("Invalid choice!")

        # ---------------- PASS / FAIL ----------------
        elif choice == "4":
            status = pass_fail_status(student_marks)
            print("\nOverall Status:", status)

        # ------------- SUBJECT FEEDBACK -------------
        elif choice == "5":
            print("\nSubject-wise Feedback:")
            for subject, mark in student_marks.items():
                print(f"{subject}: {subject_feedback(mark)}")

        elif choice == "6":
            print("\n===== RANK DETAILS =====")
            print("Rank:", int(df.loc[student_id, 'rank']))
            print("Percentile:", round(df.loc[student_id, 'percentile'], 2), "%")
        

        elif choice == "7":
            print("\n===== IMPROVEMENT ANALYSIS =====")
            analysis = improvement_analysis(student_marks)
            for subject, status in analysis.items():
             print(f"{subject}: {status}")
        

        elif choice == "8":
           risk_status = at_risk(student_marks)
           print("\nStudent Risk Status:", risk_status)
        

        # ---------------- LOGOUT ----------------
        elif choice == "9":
            print("Logging out...")
            break

        else:
            print("Invalid choice!")


# ===============================
# STUDENT LOGIN (PASSWORD PROTECTED)
# ===============================

def student_login():
    try:
        student_id = int(input(f"Enter Student ID (0 - {len(df)-1}): "))
        password = int(input("Enter Password: "))

        if password == student_id + 1000:
            print("Student login successful!")
            student_dashboard(student_id)
        else:
            print("Invalid Student ID or Password")

    except ValueError:
        print("Invalid input!")

# ===============================
# ADMIN MENU
# ===============================

def subject_statistics():
    print("\n===== SUBJECT STATISTICS =====")
    for subject in marks.columns:
        print(f"\n{subject.upper()}")
        print("Average:", round(marks[subject].mean(), 2))
        print("Max:", marks[subject].max())
        print("Min:", marks[subject].min())

def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. View Subject Statistics")
        print("2. Compare Students")
        print("3. View At-Risk Students")
        print("4. Logout")


        choice = input("Enter choice: ")

        if choice == "1":
            subject_statistics()
        elif choice == "2":
            marks.head(5).plot(kind='bar')
            plt.title("Student Comparison (First 5 Students)")
            plt.ylabel("Marks")
            plt.tight_layout()
            plt.show()
        elif choice == "3":
            at_risk_df = get_all_at_risk_students()

            if at_risk_df.empty:
             print("\nNo at-risk students found 🎉")
            else:
             print("\n===== AT-RISK STUDENTS LIST =====")
             print(at_risk_df)

        elif choice == "4":
            break
        else:
            print("Invalid choice!")

# ===============================
# MAIN LOGIN SYSTEM
# ===============================

def login():
    while True:
        print("\n===== STUDENT MARKS ANALYSIS SYSTEM =====")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                print("Admin login successful!")
                admin_menu()
            else:
                print("Invalid admin credentials")

        elif choice == "2":
            student_login()

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid option!")

# ===============================
# PROGRAM START
# ===============================
login()
