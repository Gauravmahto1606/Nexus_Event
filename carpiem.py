from tkinter import *
from tkinter import messagebox
import re

class Student:
    def __init__(self, name, roll_no, enrollment_no, branch, email, contact_no):
        self.name = name
        self.roll_no = roll_no
        self.enrollment_no = enrollment_no
        self.branch = branch
        self.email = email
        self.contact_no = contact_no
        self.registered_events = []
    def display_details(self):
        details = (
            f"\nStudent Details:\n"
            f"Name: {self.name}\n"
            f"Roll No: {self.roll_no}\n"
            f"Enrollment No: {self.enrollment_no}\n"
            f"Branch: {self.branch}\n"
            f"Email: {self.email}\n"
            f"Contact No: {self.contact_no}"
        )
        return details

    def display_registered_events(self):
        if self.registered_events:
            events = f"\nRegistered Events for {self.name} ({self.enrollment_no}):\n"
            events += "\n".join([f"- {event}" for event in self.registered_events])
            return events
        else:
            return f"\n{self.name} ({self.enrollment_no}) has not registered for any events."
        

        
        
class EventSelection:
    def __init__(self, student):
        self.student = student
        self.group_events = ["Cricket", "Football", "Basketball", "Volleyball"]
        self.individual_events = ["Sprint Race", "Table Tennis"]
        self.max_group_events = 2

    # working
    def select_event(self, event_name):
        if event_name in self.group_events:
            if event_name in self.student.registered_events:
                return f"Error: {event_name} is already selected "
                
            if len(self.student.registered_events) < self.max_group_events:
                self.student.registered_events.append(event_name)
                return f"{event_name} selected successfully!"
            else:
                return f"Error: Maximum limit of {self.max_group_events} group events reached."
        elif event_name in self.individual_events:
            if event_name in self.student.registered_events:
                return f"Error: {event_name} is already selected "
            self.student.registered_events.append(event_name)
            return f"{event_name} selected successfully!"
        else:
            return f"Error: {event_name} is not a valid event."
    
    

        
        
class StudentRegistrationApp:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Student Event Registration")

        self.students = []
        self.load_students_from_file()  # Load students from file when the program starts
        self.root.resizable(False,False)
        self.create_menu()

    def create_menu(self):
        self.root.geometry("400x300")
        menu_frame =Frame(self.root)
        menu_frame.pack(padx=20, pady=20)
        

        Label(menu_frame, text="Menu:").grid(row=0, column=0,sticky="w")

        Button(menu_frame, text="Register a new student", command=self.register_new_student).grid(row=1, column=0, sticky="w")
        Button(menu_frame, text="Register for events", command=self.register_for_events).grid(row=2, column=0, sticky="w")
        Button(menu_frame, text="Search by Enrollment No", command=self.search_by_enrollment).grid(row=3, column=0, sticky="w")
        Button(menu_frame, text="Display Students in Events", command=self.display_students_in_events).grid(row=4, column=0, sticky="w")
        Button(menu_frame, text="Exit", command=self.root.quit).grid(row=5, column=0, sticky="w")
    
    def register_new_student(self):
        register_window = Toplevel(self.root)
        
        
        register_window.geometry("400x300")
        
        register_window.title("Register New Student")

        Label(register_window, text="Enter student details:").grid(row=0, column=0,pady=5)

        Label(register_window, text="Name:").grid(row=1, column=0)
        name_entry = Entry(register_window)
        name_entry.grid(row=1, column=1)

        Label(register_window, text="Roll No:").grid(row=2, column=0)
        roll_no_entry = Entry(register_window)
        roll_no_entry.grid(row=2, column=1)

        Label(register_window, text="Enrollment No:").grid(row=3, column=0)
        enrollment_entry = Entry(register_window)
        enrollment_entry.grid(row=3, column=1)

        Label(register_window, text="Branch:").grid(row=4, column=0)
        branch_entry = Entry(register_window)
        branch_entry.grid(row=4, column=1)

        Label(register_window, text="Email:").grid(row=5, column=0)
        email_entry = Entry(register_window)
        email_entry.grid(row=5, column=1)

        Label(register_window, text="Contact No:").grid(row=6, column=0)
        contact_entry = Entry(register_window)
        contact_entry.grid(row=6, column=1)

        Button(register_window, text="Register", command=lambda: self.register_student(
            name_entry.get(), roll_no_entry.get(), enrollment_entry.get(),
            branch_entry.get(), email_entry.get(), contact_entry.get(), register_window)
        ).grid(row=7, column=0, columnspan=2, pady=10)

    def register_student(self, name, roll_no, enrollment_no, branch, email, contact_no, window):
        
        if not name.isalpha():
            messagebox.showerror("Error", "Name must contain only alphabetic characters.")
            return
        if not roll_no.isdigit():
            messagebox.showerror("Error", "Roll Number must contain only Digit.")
            return
        if not enrollment_no.isdigit():
            messagebox.showerror("Error", "Enrollment Number must contain only Digit.")
            return
        if not branch.isalpha():
            messagebox.showerror("Error", "Branch must contain only alphabetic characters.")
            return
        

        # Validation for email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        if not contact_no.isdigit() or len(contact_no) != 10:
            messagebox.showerror("Error", "Contact number must be a 10-digit number.")
            return
        student = Student(name, roll_no, enrollment_no, branch, email, contact_no)
        self.students.append(student)
        self.save_students_to_file()  # Save students to file after registration
        window.destroy()

    def register_for_events(self):
        register_window = Toplevel(self.root)
        register_window.geometry("400x300")
        register_window.title("Register for Events")

        Label(register_window, text="Enter enrollment number:").grid(row=0, column=0, columnspan=2, pady=5)
        enrollment_entry = Entry(register_window)
        enrollment_entry.grid(row=0, column=2)

        Button(register_window, text="Search", command=lambda: self.display_event_selection(
            enrollment_entry.get(), register_window)
        ).grid(row=0, column=3, pady=5)

    def display_event_selection(self, enrollment_no, window):
        for student in self.students:
            if student.enrollment_no == enrollment_no:
                event_selection = EventSelection(student)
                event_selection_window =Toplevel(window)
                event_selection_window.geometry("400x300")
                
                event_selection_window.title(f"Event Selection for {student.name}")

                Label(event_selection_window, text="Available Events:").pack()
                Label(event_selection_window, text="Group Events:").pack()
                for event in event_selection.group_events:
                    Button(event_selection_window, text=event, command=lambda e=event: self.select_event(e, student, event_selection_window)).pack()
                Label(event_selection_window, text="Individual Events:").pack()
                for event in event_selection.individual_events:
                    Button(event_selection_window, text=event, command=lambda e=event: self.select_event(e, student, event_selection_window)).pack()

                break
        else:
            messagebox.showerror("Error", "Student not found.")

    def select_event(self, event_name, student, window):
        event_selection = EventSelection(student)
        result = event_selection.select_event(event_name)
        if "Error" in result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Success", result)
        # self.load_students_from_file()
        window.destroy()

    def search_by_enrollment(self):
        search_window = Toplevel(self.root)
        search_window.geometry("400x300")
        search_window.title("Search by Enrollment No")

        Label(search_window, text="Enter enrollment number:").grid(row=0, column=0, pady=5)
        enrollment_entry = Entry(search_window)
        enrollment_entry.grid(row=0, column=1)

        Button(search_window, text="Search", command=lambda: self.display_student_details(
            enrollment_entry.get(), search_window)
        ).grid(row=0, column=2, pady=5)

# working
    def display_student_details(self, enrollment_no, window):
        for student in self.students:
            if student.enrollment_no == enrollment_no:
                details_window = Toplevel(window)
                details_window.geometry("400x300")
                details_window.title(f"Details for {student.name}")

                details_text = Text(details_window)
                details_text.pack()

                details_text.insert(END, student.display_details())
                details_text.insert(END, student.display_registered_events())
                break
        else:
             messagebox.showerror("Error", "Student not found.")
    
    


    def display_students_in_events(self):
        students_in_events_window = Toplevel(self.root)
        students_in_events_window.title("Students in Events")
        students_in_events_window.geometry("400x300")

        Label(students_in_events_window, text="Students in Events:").pack()

        for student in self.students:
            if student.registered_events:
                student_info = f"{student.name} ({student.enrollment_no}) - Events: {', '.join(student.registered_events)}"
                Label(students_in_events_window, text=student_info).pack()

# working

    def save_students_to_file(self):
        with open("students.txt", "w") as file:
            for student in self.students:
                file.write(f"Student Name : {student.name},Roll NO : {student.roll_no},Enrollment Number : {student.enrollment_no},Branch : {student.branch},Email : {student.email},Phone No : {student.contact_no},{'|'.join(student.registered_events)}\n")

    # new
    # def save_students_to_file(self):
    #         with open("students.txt", "w") as file:
    #             for student in self.students:
    #                 file.write(f"Student Name: {student.name}, Roll NO: {student.roll_no}, Enrollment Number: {student.enrollment_no}, Branch: {student.branch}, Email: {student.email}, Phone No: {student.contact_no} , ")
    #                 if student.registered_events:
    #                     file.write(f"Registered Events: {'|'.join(student.registered_events)}\n")
    #                 else:
    #                     file.write("Registered Events: None\n")



    def load_students_from_file(self):
        try:
            with open("students.txt", "r") as file:
                for line in file:

                    data = line.strip().split(",")
                    student_data = []
                    for part in data[0:len(data)-1]:
                        key,value = part.split(":")
                        student_data.append(value.strip())
                    student = Student(student_data[0], student_data[1], student_data[2], student_data[3], student_data[4], student_data[5])
                    student.registered_events = data[6].split("|")
                    student_data.append(data[6].split("|"))
                    # print(student_data)
                    self.students.append(student)
                    
        except FileNotFoundError as e:
            print(e)
        
        
def main():
    root =Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

