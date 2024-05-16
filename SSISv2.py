import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Iterator
from mysql import connector
from mysql.connector import cursor, errorcode

class Student:
    #initialize new Student object
    def __init__(
        self,
        std_id: str,
        last_name: str, 
        first_name: str, 
        middle_name:str, 
        year:int, 
        gender: str, 
        course_code: str
    ) -> None:
        self.std_id = std_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.year = year
        self.gender = gender
        self.course_code = course_code
    
def read_courses() -> Iterator[list[str]]: 
    try:
        query = 'SELECT * FROM courses ORDER BY code'
        cursor.execute(query)
        
        for course_data in cursor.fetchall():
            yield [
                course_data['code'],
                course_data['name']
            ]
    
    except connector.Error as e:
        print(f"Error occured: {e}")
    
def read_students() -> Iterator[list[str | int]]:
    try:
        query = 'SELECT * FROM students ORDER BY id'
        cursor.execute(query)
        
        for student_data in cursor.fetchall():
            yield [
                student_data['id'],
                student_data['lastName'],
                student_data['firstName'],
                student_data['middleName'],
                int(student_data['yearLevel']),
                student_data['gender'],
                student_data['course']
            ]
    
    except connector.Error as e:
        print(f"Error occured: {e}")
    
def add_student(
    courses: Iterator[list[str]], 
    std_id: str, 
    last_name: str, 
    first_name: str, 
    middle_name: str, 
    year: int, 
    gender: str, 
    course_code: str
) -> str:
    try:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to add this student?")
                
        if confirmation:
            if (course_code := course_code.strip()): #check if course code is provided
                for course in courses: #check if its in course dict
                    if course_code.upper() in course[0].upper():
                        status = "Enrolled"
                        break
                    
                else:
                    status = "Not Available"
            
            else:
                status = "Not Enrolled"
            
            query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (std_id.upper(), last_name.upper(), first_name.upper(), middle_name.upper(), year, gender.upper(), course_code.upper()))
            connection.commit()

        return status
    
    except connector.Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            return "ID number already Exists, student not added"
    
    except Exception as e:
        print("Error occured while adding students", e)
        return "Error"

def main_window() -> None:
    #get the file path...
    global connection
    connection = connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="123456", 
        database="data"
    )
    
    global cursor
    cursor = connection.cursor(dictionary=True)

    #make main windowww
    main_window = tk.Tk()
    main_window.geometry("450x300")
    main_window.title("Main Menu")
    main_window.resizable(False, False)

    frame = tk.Frame(main_window, width=933, height=531, bg="#A51D21")
    frame.pack_propagate(False)
    frame.pack()
    
    def open_add_student_window(): #function to add studentz
        main_window.withdraw()
        add_student_window(read_courses())

    def open_student_list_window(): #function for student lizt
        main_window.withdraw()
        student_list_window(read_students())

    def open_courses_window(): #function to open coursezz
        main_window.withdraw()
        courses_window(read_courses())

    
    welcome_label = tk.Label(frame, text="Welcome to Student Information System", font=("Montserrat", 13,"bold"),fg="#FFFFFF", bg="#A51D21")
    welcome_label.pack()

    #buttonz for the windowz
    add_button = tk.Button(main_window, text="Add Student", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=open_add_student_window)
    add_button.place(x=120, y=50, width=200, height=38)

    list_button = tk.Button(main_window, text="Student List", font=("Montserrat",10), bg="#1A1515",fg="#FFFFFF", bd=0,command=open_student_list_window)
    list_button.place(x=120, y=100, width=200, height=38)

    courses_button = tk.Button(main_window, text="Available Courses",font=("Montserrat",10), bg="#1A1515",fg="#FFFFFF", bd=0, command=open_courses_window)
    courses_button.place(x=120, y=150, width=200, height=38)

    exit_button = tk.Button(main_window, text="Exit",font=("Montserrat",10),bg="#1A1515",fg="#FFFFFF", bd=0, command=quit)
    exit_button.place(x=120, y=200, width=200, height=38)

    main_window.protocol("WM_DELETE_WINDOW", quit)
    
    main_window.mainloop()

def add_student_window(courses: Iterator[list[str]]) -> None:
    def back() -> None:
        add_student_window.destroy()
        main_window()

    def validate_year(year: str) -> bool:
        if year.isdigit():
            return 1 <= int(year) <= 4
        
        return False
    
    def validate_id(std_id: str) -> bool:
        return \
            len(std_id) == 9 and \
            std_id[:4].isdigit() and \
            std_id[5:].isdigit() and \
            std_id[4] == '-'

    def save_student():
        try:
            student_id, last_name, first_name, middle_name, year, course_code = (entry.get() for entry in entry_fields[:6])
            gender = gender_var.get()

            if not validate_year(year):
                messagebox.showerror("Error", "Invalid year level. Please enter a value from 1 to 4.")
                return
            
            if not validate_id(student_id):
                messagebox.showerror("Error", "Invalid student ID format. Please use the format 20XX-XXXX.")
                return

            # get the status
            status = add_student(read_courses(), student_id, last_name, first_name, middle_name, year, gender, course_code)
            messagebox.showinfo("Status", f"Student added. Status: {status}")  # Show status
            
            add_student_window.destroy()
            
            main_window()  # Refresh main window
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    #create a new toplevel window for adding a student
    add_student_window = tk.Toplevel()  
    add_student_window.geometry("850x531")
    add_student_window.title("Add Student")
    add_student_window.resizable(False, False)

    frame = tk.Frame(add_student_window, width=933, height=531, bg="#A51D21")
    frame.pack_propagate(False)
    frame.pack()

    input_label = tk.Label(frame, text="Input Student Information", font=("Montserrat", 15,"bold"),fg="#FFFFFF", bg="#A51D21")
    input_label.pack()
    
    labels = [
        "Student ID(yyyy-nnnn)", 
        "Last Name(Ex:Dela Cruz)", "First Name(Ex:Juan)", "Middle Name (Ex:Santos)", 
        "Year Level (1-4)", "Gender(F/M/Others)", "Course Code(Ex: BSCS)"
    ]

    label_positions = [
        (36, 63), 
        (36, 149), (304, 149), (572, 149), 
        (88, 243), (440, 238), (36, 329)
    ]

    for label_text, (x, y) in zip(labels, label_positions):
        label = tk.Label(frame, text=label_text, font=("Montserrat", 10), bg="#A51D21", fg="white")
        label.place(x=x, y=y) 

    #entry fields for the input
    entry_positions = [
        (23, 96), (23, 185), (292, 185), (561, 185), (75, 276), (40, 350) # Added position for the Course Code entry field
    ]

    entry_fields: list[tk.Entry] = list()
    for (x, y) in entry_positions:
        entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9")
        entry.place(x=x, y=y, width=249)
        entry_fields.append(entry)

    # dropdown for the gender opt
    gender_options = ["Female", "Male", "Others"]
    gender_var = tk.StringVar(add_student_window)
    gender_var.set(gender_options[0])  

    gender_label = tk.Label(frame, text="Gender", font=("Montserrat", 10), bg="#A51D21", fg="white")
    gender_label.place(x=440, y=238)

    gender_dropdown = tk.OptionMenu(frame, gender_var, *gender_options)
    gender_dropdown.config(font=("Montserrat", 10), bg="#D9D9D9", width=15)
    gender_dropdown.place(x=440, y=260)

    #save the student info and add it to csv
    save_button = tk.Button(frame, text="Save", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=save_student)
    save_button.place(x=650, y=468, width=130, height=38)

    back_button = tk.Button(frame, text="Back", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=back)
    back_button.place(x=510, y=468, width=130, height=38)
    
    add_student_window.protocol("WM_DELETE_WINDOW", back)

    add_student_window.mainloop()

def student_list_window(students: Iterator[list[str]]) -> None:
    def back() -> None:
        student_list_window.destroy()
        main_window()

    def search_students() -> None:
        search = search_entry.get().lower()
        
        if not query:
            populate_student_list(students)
            return
        
        query = "SELECT * FROM students WHERE id LIKE %s OR lastName LIKE %s OR firstName LIKE %s OR middleName LIKE %s OR yearLevel LIKE %s or gender LIKE %s or course LIKE %s"
        cursor.execute(query, tuple(f'%{search.upper()}%' for _ in range(7)))
        
        filtered_students = ([
            student["id"], 
            student["lastName"], 
            student["firstName"], 
            student["middleName"],
            int(student["yearLevel"]),
            student["gender"],
            student["course"]
        ] for student in cursor.fetchall())
        
        populate_student_list(filtered_students)
    
    def populate_student_list(student_data: Iterator[list[str | int]]) -> None:
        tree.delete(*tree.get_children())
        
        for student in student_data:
            tree.insert(
                "",
                "end", 
                values=(
                    student[0],
                    student[1],
                    student[2],
                    student[3],
                    student[4],
                    student[5],
                    student[6] if student[6] else None
                ), 
                iid=student[0]
            )

    #new window for the student list
    student_list_window = tk.Tk()
    student_list_window.geometry("2000x700")
    student_list_window.title("Student List")

    search_frame = tk.Frame(student_list_window, bg="#A51D21")
    search_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

    search_label = tk.Label(search_frame, text="Search:", font=("Montserrat", 10), bg="#A51D21", fg="white")
    search_label.pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, font=("Montserrat", 10), width=50)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Search", font=("Montserrat", 10), command=search_students )
    search_button.pack(side=tk.LEFT, padx=5)

    frame = tk.Frame(student_list_window, width=400, height=300)
    frame.pack(fill=tk.BOTH, expand=True)

    list_label = tk.Label(frame, text="Student List", font=("Helvetica", 13),bg="#A51D21",fg="#FFFFFF")
    list_label.pack(fill=tk.X)

    #treeview widget to display data
    tree = ttk.Treeview(frame, columns=("Student ID", "Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course Code"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    #set headings for columns
    tree.heading("Student ID", text="Student ID")
    tree.heading("Last Name", text="Last Name")
    tree.heading("First Name", text="First Name")
    tree.heading("Middle Name", text="Middle Name")
    tree.heading("Year Level", text="Year Level")
    tree.heading("Gender", text="Gender")
    tree.heading("Course Code", text="Course Code")

    populate_student_list(students)

    def remove_student() -> None:
        selected_item = tree.selection()
        
        if selected_item:
            try:
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this student?")

                if confirmation:
                    tree.delete(selected_item[0])  # delete student from treeview
                    
                    query = "DELETE FROM students WHERE id = %s"
                    cursor.execute(query, (selected_item[0],))
                    connection.commit()
                    
            except ValueError:
                messagebox.showerror("Error", "Invalid selection.")
        
        else:
            messagebox.showerror("Error", "No student selected.")

    # Remove button
    remove_button = tk.Button(frame, text="Remove", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=remove_student)
    remove_button.pack(side=tk.LEFT, padx=5)


    # edit student info
    def edit_student() -> None:
        selected_item = tree.selection()
        
        if selected_item:
            try:
                query = "SELECT * FROM students WHERE id = %s"
                cursor.execute(query, (selected_item[0],))
                fetched_row = cursor.fetchone()
                
                student: list[str | int] = [
                    fetched_row["id"],
                    fetched_row["lastName"],
                    fetched_row["firstName"],
                    fetched_row["middleName"],
                    int(fetched_row["yearLevel"]),
                    fetched_row["gender"],
                    fetched_row["course"]
                ]
                
                print("Selected student:", selected_item[0])  # print the selected index for debugging
                edit_student_window(student, students, student_list_window)
                
            except ValueError:
                messagebox.showerror("Error", "Invalid selection.")
        
        else:
            messagebox.showerror("Error", "No student selected.")


    #edit button
    edit_button = tk.Button(frame, text="Edit", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=edit_student)
    edit_button.pack(side=tk.LEFT, padx=5)

    back_button = tk.Button(frame, text="Back", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=back)
    back_button.pack(side=tk.LEFT, padx=5)
    
    student_list_window.protocol("WM_DELETE_WINDOW", back)

def edit_student_window(
    student: list[str | int], 
    students: Iterator[list[str]],
    previous_window: tk.Tk | None=None
) -> None:
    def back() -> None:
        edit_student_window.destroy()
        main_window()

    def save_student_changes() -> None:
        try:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to save changes for this student?")
                
            if confirmation:
                parameters = {
                    'id': entry_fields[0].get().upper(),
                    'lastName': entry_fields[1].get().upper(),
                    'firstName': entry_fields[2].get().upper(),
                    'middleName': entry_fields[3].get().upper(),
                    'yearLevel': int(entry_fields[4].get()),
                    'gender': gender_var.get().upper(),
                    'course': course_code_entry.get().upper() if course_code_entry else None
                }
                
                query = "UPDATE students SET lastName = %(lastName)s, firstName = %(firstName)s, middleName = %(middleName)s, yearLevel = %(yearLevel)s, gender = %(gender)s, course = %(course)s WHERE id = %(id)s"
                cursor.execute(query, parameters)
                connection.commit()
                
                messagebox.showinfo("Success", "Changes saved successfully.")
                
                edit_student_window.destroy()
                
                if previous_window:
                    previous_window.destroy()  # destroy previous student list window
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        
        return student_list_window(read_students())

    #create new toplevel window for edi student , details are same with add students
    edit_student_window = tk.Toplevel()  
    edit_student_window.geometry("850x531")
    edit_student_window.title("Edit Student")
    edit_student_window.resizable(False, False)

    frame = tk.Frame(edit_student_window, width=933, height=531, bg="#A51D21")
    frame.pack_propagate(False)
    frame.pack()

    input_label = tk.Label(
        frame, 
        text="Edit Student Information", 
        font=("Montserrat", 15,"bold"),
        fg="#FFFFFF", 
        bg="#A51D21"
    )
    input_label.pack()

    labels = [
        "Student ID", 
        "Last Name", 
        "First Name", 
        "Middle Name", 
        "Year Level", 
        "Gender", 
        "Course Code"
    ]

    label_positions: list[tuple[int, int]] = [
        (36, 63), (36, 149), (304, 149), (572, 149), (88, 243), (440, 238), (36, 329)
    ]

    for label_text, (x, y) in zip(labels, label_positions):
        label = tk.Label(frame, text=label_text, font=("Montserrat", 10), bg="#A51D21", fg="white")
        label.place(x=x, y=y) 

    entry_positions: list[tuple[int, int]] = [
        (23, 96), (23, 185), (292, 185), (561, 185), (75, 276)
    ]

    entry_fields: list[tk.Entry] = list()
    for i, (x, y) in enumerate(entry_positions):
        entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9", textvariable=tk.StringVar(value=student[i]))
        
        if i == 0:
            entry.config(state='readonly')
            
        entry.place(x=x, y=y, width=249)
        entry_fields.append(entry)

    gender_options = ["Female", "Male", "Others"]
    gender_var = tk.StringVar(edit_student_window)
    gender_var.set(student[5])  

    gender_label = tk.Label(frame, text="Gender", font=("Montserrat", 10), bg="#A51D21", fg="white")
    gender_label.place(x=440, y=243)

    gender_dropdown = tk.OptionMenu(frame, gender_var, *gender_options)
    gender_dropdown.config(font=("Montserrat", 10), bg="#D9D9D9", width=17)
    gender_dropdown.place(x=440, y=268)

    course_code_label = tk.Label(frame, text="Course Code", font=("Montserrat", 10), bg="#A51D21", fg="white")
    course_code_label.place(x=36, y=329)

    course_code_entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9")
    course_code_entry.insert(0, student[6])  
    course_code_entry.place(x=36, y=360, width=249)

    save_button = tk.Button(frame, text="Save Changes", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=save_student_changes)
    save_button.place(x=650, y=468, width=130, height=38)

    back_button = tk.Button(frame, text="Back", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=back)
    back_button.place(x=510, y=468, width=130, height=38)
    
    edit_student_window.mainloop()

def courses_window(courses: Iterator[list[str]]) -> None:
    def back() -> None:
        courses_window.destroy()
        main_window()

    def add_course_window() -> None:
        def add_course() -> None:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to add this course?")
            
            if confirmation:
                course_code = course_code_entry.get().strip()
                course_name = course_name_entry.get().strip()
                
                try:
                    if course_code and course_name:
                        parameters = {
                            'code': course_code.upper(),
                            'name': course_name.upper()
                        }
                        query = "INSERT INTO courses (code, name) VALUES (%(code)s, %(name)s)"
                        cursor.execute(query, parameters)
                        connection.commit()

                        messagebox.showinfo("Success", "Course added successfully.")
                        
                        add_course_window.destroy()
                        courses_window.destroy()
                    
                    else:
                        messagebox.showerror("Error", "Please enter both Course Code and Course Name")
                
                except connector.Error as e:
                    if e.errno == errorcode.ER_DUP_ENTRY:
                        messagebox.showerror("Error",f"Course with code {course_code} already exists.")

        add_course_window = tk.Toplevel()
        add_course_window.geometry("600x120")
        add_course_window.title("Add Course")
        add_course_window.resizable(False, False)
        add_course_window.config(bg="#A51D21")

        course_code_label = tk.Label(add_course_window, text="Course Code:",font=("Montserrat",10),bg=("#A51D21"),fg=("#FFFFFF"))
        course_code_label.grid(row=0, column=0, padx=5, pady=5)
        course_code_entry = tk.Entry(add_course_window, width=80)
        course_code_entry.grid(row=0, column=1, padx=5, pady=5)

        course_name_label = tk.Label(add_course_window, text="Course Name:",font=("Montserrat",10),bg=("#A51D21"),fg=("#FFFFFF"))
        course_name_label.grid(row=1, column=0, padx=5, pady=5)
        course_name_entry = tk.Entry(add_course_window,width=80)
        course_name_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = tk.Button(add_course_window, text="Add", command=add_course)
        add_button.grid(row=2, columnspan=2, pady=10)

    def edit_course_window() -> None:
        selected_item = tree.selection()
        
        if selected_item:
            try:
                edit_window = tk.Toplevel()
                edit_window.geometry("600x150")
                edit_window.title("Edit Course")
                edit_window.resizable(False, False)
                edit_window.config(bg="#A51D21")

                course_code_label = tk.Label(edit_window, text="Course Code:",font=("Montserrat",10),bg=("#A51D21"),fg=("#FFFFFF"))
                course_code_label.grid(row=0, column=0, padx=5, pady=5)
                course_code_entry = tk.Entry(edit_window, width=80, textvariable=tk.StringVar(value=selected_item[0]))
                course_code_entry.grid(row=0, column=1, padx=5, pady=5)

                course_name_label = tk.Label(edit_window, text="Course Name:",)
                course_name_label.grid(row=1, column=0, padx=5, pady=5)
                course_name_entry = tk.Entry(
                    edit_window, 
                    width=80, 
                    textvariable=tk.StringVar(
                        value=tree.item(selected_item[0], "values")[1]
                    )
                )
                course_name_entry.grid(row=1, column=1, padx=5, pady=5)

                def update_course() -> None:
                    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to update this course?")
                
                    if confirmation:
                        new_course_code = course_code_entry.get().strip().upper()
                        new_course_name = course_name_entry.get().strip().upper()
                        
                        tree.item(selected_item[0], values=[new_course_code, new_course_name])

                        query = "UPDATE courses SET name = %s WHERE code = %s"
                        cursor.execute(query, (new_course_name, ))
                        connection.commit()

                        messagebox.showinfo("Success", "Course updated successfully.")
                        edit_window.destroy()

                update_button = tk.Button(edit_window, text="Update", command=update_course)
                update_button.grid(row=2, columnspan=2, pady=10)
                
            except ValueError:
                messagebox.showerror("Error", "Invalid selection.")
            
        else:
            messagebox.showerror("Error", "No course selected.")

    
    def remove_course() -> None:
        selected_item = tree.selection()
        
        if selected_item:
            try:
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this course?")

                if confirmation:
                    tree.delete(selected_item[0])  # delete course from treeview
                
                    query = "DELETE FROM courses WHERE code = %s"
                    cursor.execute(query, (selected_item[0],))
                    connection.commit()

            except ValueError:
                messagebox.showerror("Error", "Invalid selection.")
        
        else:
            messagebox.showerror("Error", "No course selected.")
                    

    def search_courses() -> None:
        search = search_entry.get().upper()
        
        if not query:
            populate_course_list(read_courses())
            return
        
        query = "SELECT * FROM courses WHERE code LIKE %s OR name LIKE %s"
        cursor.execute(query, (f'%{search}%', f'%{search}%'))
        
        filtered_courses = ([
            course["code"],
            course["name"]
        ] for course in cursor.fetchall())
        
        populate_course_list(filtered_courses)

    def populate_course_list(course_data: Iterator[list[str]]) -> None:
        # Clear the treeview
        for record in tree.get_children():
            tree.delete(record)
        
        # Insert course data into the treeview
        for code, name in course_data:
            tree.insert("", tk.END, iid=code, values=(code, name))
        
    #create window for courses
    courses_window = tk.Tk()
    courses_window.geometry("300x400")
    courses_window.title("Courses")

    frame = tk.Frame(courses_window, width=400, height=300)
    frame.pack(fill=tk.BOTH, expand=True)

    list_label = tk.Label(frame, text="Available Courses", font=("Montserrat", 12), bg="#A51D21", fg="#FFFFFF")
    list_label.pack(fill=tk.X)

    search_frame = tk.Frame(frame, bg="#A51D21")
    search_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

    search_label = tk.Label(search_frame, text="Search:", font=("Montserrat", 10), bg="#A51D21", fg="white")
    search_label.pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, font=("Montserrat", 10), width=50)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Search", font=("Montserrat", 10), command=search_courses)
    search_button.pack(side=tk.LEFT, padx=5)

    # treeview for the courses
    tree = ttk.Treeview(frame, columns=("Course Code", "Course Name"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("Course Code", text="Course Code")
    tree.heading("Course Name", text="Course Name")

    populate_course_list(read_courses())

    add_button = tk.Button(frame,text="Add", font=("Montserrat",10), bg="#1a1515", fg="#FFFFFF", bd=0, command=add_course_window)
    add_button.pack(side=tk.LEFT, padx=5)

    edit_button = tk.Button(frame, text="Edit", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=edit_course_window)
    edit_button.pack(side=tk.LEFT, padx=5)


    remove_button = tk.Button(frame, text="Remove", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=remove_course)
    remove_button.pack(side=tk.LEFT, padx=5)

    back_button = tk.Button(frame, text="Back", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=back)
    back_button.pack(side=tk.LEFT, padx=5) 

    courses_window.protocol("WM_DELETE_WINDOW", back)
    
    courses_window.mainloop()

if __name__ == "__main__": #call main to open main window
    main_window()
