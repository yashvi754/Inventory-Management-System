from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from create_db import create_db

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        # Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="#b2d8d8")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        # Title
        title = Label(self.root, text="Employee Details", font=("times new roman", 15), bg="#008080", fg="white")
        title.place(x=50, y=100, width=1000)

        # Content
        # Row 1
        lbl_empid = Label(self.root, text="Emp ID", font=("times new roman", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("times new roman", 15), bg="white").place(x=400, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15), bg="white").place(x=750, y=150)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("times new roman", 15), bg="#b2d8d8").place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15), bg="#b2d8d8").place(x=850, y=150, width=180)

        # Row 2
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("times new roman", 15), bg="white").place(x=400, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("times new roman", 15), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15), bg="#b2d8d8").place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("times new roman", 15), bg="#b2d8d8").place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("times new roman", 15), bg="#b2d8d8").place(x=850, y=190, width=180)

        # Row 3
        lbl_email = Label(self.root, text="Email", font=("times new roman", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("times new roman", 15), bg="white").place(x=400, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("times new roman", 15), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("times new roman", 15), bg="#b2d8d8").place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("times new roman", 15), bg="#b2d8d8").place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)
        
        # Row 4
        lbl_address = Label(self.root, text="Address", font=("times new roman", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("times new roman", 15), bg="white").place(x=750, y=270)

        self.txt_address = Text(self.root, font=("times new roman", 15), bg="#b2d8d8")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("times new roman", 15), bg="#b2d8d8").place(x=850, y=270, width=180)
        
        # Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=500, y=305, width=125, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=635, y=305, width=125, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete,font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=770, y=305, width=125, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=905, y=305, width=125, height=28)
        
        # Employee Details Frame
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        
        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

#========================================================================
    
    # Add new employee record to the database
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()  # make a cursor that used to send SQL commands to SQLite database 
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                # ? is a parameter placeholder here (This is the safest way)
                # (self.var_emp_id.get(),) : here (,) makes it the tuple
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END).strip(),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()

    # Show all employee records in the Treeview
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children()) # deletes the previos entries it had in the treeview
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()

    # Get data from the selected row in the Treeview and populate fields
    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    # Update an existing employee record
    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where eid=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END).strip(),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()

    # Delete an employee record
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from employee where eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()
            
    # Clear all the entry fields
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
    
    # Search for records and display them
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select" and self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                query = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))

                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()