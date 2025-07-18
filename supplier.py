from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # Search Frame
        # Options
        lbl_search = Label(self.root, text="Invoice No.", bg="white", font=("times new roman", 15))
        lbl_search.place(x=700, y=80)
        
        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="#b2d8d8").place(x=800, y=80, width=160)
        btn_search = Button(self.root, text="Search", command=self.search, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=980, y=79, width=100, height=28)

        # Title
        title = Label(self.root, text="Supplier Details", font=("times new roman", 20, "bold"), bg="#008080", fg="white").place(x=50, y=10, width=1000, height=40)

        # Content
        # Row 1
        lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50, y=80)
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("times new roman", 15), bg="#b2d8d8").place(x=180, y=80, width=180)

        # Row 2
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15), bg="white").place(x=50, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15), bg="#b2d8d8").place(x=180, y=120, width=180)

        # Row 3
        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15), bg="white").place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15), bg="#b2d8d8").place(x=180, y=160, width=180)
        
        # Row 4
        lbl_desc = Label(self.root, text="Description", font=("times new roman", 15), bg="white").place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("times new roman", 15), bg="#b2d8d8")
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=180, y=370, width=110, height=35)
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=300, y=370, width=110, height=35)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=420, y=370, width=110, height=35)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=540, y=370, width=110, height=35)

        # Employee Details Frame
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        
        self.supplierTable["show"] = "headings"

        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Backend Functions
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice no. already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice, name, contact, desc) values(?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("Update supplier set name=?, contact=?, desc=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END).strip(),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        con.close()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()
    
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()